import os
import string
from math import log10

from django.conf import settings
from django.core.cache import cache
from django.core.files import File as F
from django.core.paginator import Page, Paginator

from .models import File, Word, WordFile


def get_page_obj(request, obj_set) -> Page:
    """Получение page_obj с паджинатором."""
    cache.clear()
    paginator = Paginator(obj_set, settings.RECORDS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def handle_file(file_obj) -> int:
    """
    Обработчик текстовых файлов. Обновляет таблицу слов и возвращает
    кол-во слов в файле.
    """
    with open(os.path.join(
        settings.MEDIA_ROOT, f'files/{file_obj.name}'
    ), 'r') as myfile:
        file = F(myfile)
        rows = file.readlines()
        clear_rows = [row.strip().translate(str.maketrans(
            '', '', (string.punctuation + '—')
        )) for row in rows]
        freq = dict()
        word_counter = 0
        for row in clear_rows:
            for word in row.split():
                word_counter += 1
                word = word.lower()
                if word in freq:
                    freq[word] += 1
                else:
                    freq[word] = 1
        for req in freq:
            word, _ = Word.objects.get_or_create(word=req)
            tf = float(freq.get(req) / word_counter)
            WordFile.objects.create(word=word, file=file_obj, tf=tf)
        return word_counter


def set_idf(word) -> None:
    """Рассчитывает для слова IDF."""
    docs_qty = File.objects.all().count()
    word_docs_qty = WordFile.objects.filter(word_id=word.id).count()
    idf_value = log10(docs_qty / word_docs_qty)
    word.idf = idf_value
    word.save()
