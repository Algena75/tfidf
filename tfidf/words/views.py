from pathlib import Path

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import FileForm
from .models import File
from .utils import get_page_obj, handle_file, set_idf


def index(request: HttpRequest) -> HttpResponse:
    """
    Представление стартовой страницы. Возвращает список файлов из коллекции.
    """
    template = 'index.html'
    form = FileForm(request.POST or None)
    files = File.objects.all()
    page_obj = get_page_obj(request, files)
    context = {
        'form': form,
        'is_index': True,
        'page_obj': page_obj
    }
    return render(request, template, context)


def file_details(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Представление для анализа файла. Возвращает список из 50 слов с индексами
    TF / IDF.
    """
    template = 'index.html'
    file = get_object_or_404(File, pk=pk)
    words = file.words.all()
    for word in words:
        set_idf(word.word)
    words = words.order_by('-word__idf')[:50]
    page_obj = get_page_obj(request, words)
    context = {
        'form': FileForm(),
        'is_index': False,
        'page_obj': page_obj,
        'file': file.name
    }
    return render(request, template, context)


def add_file(request: HttpRequest) -> HttpResponse:
    """
    Функция добавления текстового файла в коллекцию. Если файл текстовый -
    запускает обработку файла. В противном случае возвращает ошибку.
    """
    if request.method == 'POST' and request.FILES:
        file = request.FILES['file']
        ext = Path(file.name).suffix[1:]
        if ext == 'txt':
            file_obj = File.objects.create(file=file)
            words_qty = handle_file(file_obj)
            file_obj.words_qty = words_qty
            file_obj.save()
            return redirect('words:file_details', pk=file_obj.id)
        else:
            messages.error(request, 'Только текстовые файлы')
    return redirect('words:index')


def page_not_found(request: HttpRequest, exception) -> HttpResponse:
    """Кастомная страница 404."""
    return render(request, '404.html')


def csrf_failure(request: HttpRequest, reason: str = '') -> HttpResponse:
    """Кастомная страница 403."""
    return render(request, '403.html')


def server_error(request: HttpRequest, exception=None) -> HttpResponse:
    """Кастомная страница 500."""
    return render(request, '500.html')
