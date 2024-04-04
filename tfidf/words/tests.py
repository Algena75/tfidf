import shutil
import tempfile
from http import HTTPStatus

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from .models import File, Word

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


class URLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_homepage(self):
        """Стартовая страница возвращает статус 200."""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, HTTPStatus.OK.value)
        self.assertTemplateUsed(response, 'index.html')

    def test_nonexistent_page_uses_template_404(self):
        """Несуществующая страница использует шаблон 404.html"""
        response = self.guest_client.get('/nonexistent_page/')
        self.assertTemplateUsed(response, '404.html')

    def test_add_file_url_redirects_to_index(self):
        """Страница добавления файла пересылает на страницу index."""
        response = self.guest_client.get('/add_file/', follow=True)
        self.assertRedirects(
            response,
            f"{reverse('words:index')}"
        )


class FileModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.file = File.objects.create(
            file='files/test.txt',
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у модели File корректно работают __str__ и save()"""
        file = FileModelTest.file
        expected_file_name = 'files/test.txt'
        self.assertEqual(expected_file_name, file.__str__())
        self.assertEqual(expected_file_name, file.name)
        self.assertEqual(file.words_qty, 0)


class ViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.file = File.objects.create(
            file='files/test.txt',
        )

    def setUp(self):
        self.guest_client = Client()

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response_1 = self.guest_client.get(reverse('words:index'))
        response_2 = self.guest_client.get(
            reverse('words:file_details', kwargs={'pk': 1})
        )
        self.assertContains(response_1, 'Список файлов')
        self.assertContains(response_2, 'Список слов в файле')
        self.assertContains(response_1, 'Добавить текстовый файл')
        self.assertContains(response_2, 'Добавить текстовый файл')


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class FormsFileTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.loading_client = Client()
        cls.small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.uploaded_gif = SimpleUploadedFile(
            name='small.gif',
            content=cls.small_gif,
            content_type='image/gif'
        )
        cls.small_txt = (
            bytes('one two three four five', 'utf-8')
        )
        cls.uploaded_txt = SimpleUploadedFile(
            name='small.txt',
            content=cls.small_txt,
            content_type='text/plain'
        )
        cls.post = cls.loading_client.post(
            reverse('words:add_file'),
            {'file': cls.uploaded_txt}
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.guest_client = Client()

    def test_DB_content(self):
        """
        Проверяет заполнение базы данных:
        1. При предустановке добавлен текстовый файл с 5 словами;
        2. Нетекстовый файл в базу не добавляется.
        3. При добавлении дубликата текстового файла количество файлов
           увеличивается, а количество слов не изменяется.
        """
        files_count = File.objects.count()
        words_count = Word.objects.count()
        self.assertEqual(files_count, 1)
        self.assertEqual(words_count, 5)
        self.guest_client.post(
            reverse('words:add_file'),
            {'file': FormsFileTest.uploaded_gif}
        )
        files_count_2 = File.objects.count()
        self.assertEqual(files_count_2, 1)
        self.guest_client.post(
            reverse('words:add_file'),
            {'file': FormsFileTest.uploaded_txt}
        )
        files_count_3 = File.objects.count()
        self.assertEqual(files_count_3, 2)
        words_count_2 = Word.objects.count()
        self.assertEqual(words_count_2, 5)
