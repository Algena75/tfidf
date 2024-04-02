# Сервис расчёта TF/IDF
Реализация сервиса загрузки текстового файла с расчётом индексов TF-IDF (от англ. TF — term frequency, IDF — inverse document frequency)
## Автор:
Алексей Наумов ( algena75@yandex.ru )
## Используемые технолологии:
* Django
* SQLite
* Bootstrap

## Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:


```
git clone git@github.com:Algena75/tfidf.git
```

```
cd tfidf
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```
## Как запустить проект локально:
    - Перейти в директорию `tfidf` и выполнить миграции 
    ```
    cd tfidf/ && python3 manage.py migrate
    ```
    - запустить проект 
    ```
    python3 manage.py runserver
    ```
    открыть в браузере http://127.0.0.1:8000/
## Подготовка:
Загрузить текстовые файлы.  В корне проекта помещены для тестирования файлы `'test.txt'`, `onemore.txt` и `bigtest.txt`.
