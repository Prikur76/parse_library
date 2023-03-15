# Библиотека для дедушки
С помощью **`parse_library`** можно собрать свою собственную электронную 
библиотеку научной фантастики, используя онлайн-библиотеку [tululu.org](https://tululu.org/)  

## Как работает
Используя **`parse_library`**, получаем информацию о книгах для их бесплатного скачивания, включая  
название книги, автора, обложку (если есть), комментарии, ссылку для скачивания текста - 
как по любому ID книги или диапазону IDs книг, так и по страницам из раздела 'научная фантастика' библиотеки.\
Информация о скачанных книгах выводится в консоль.\
Результат помещается в файл **`books.json`** для последующего использования, например, в базе данных. 

### Как установить
* Python3 должен уже быть установлен.
* Для изоляции проекта рекомендуется использовать [virtualenv/venv](https://docs.python.org/3/library/venv.html).
* Чтобы развернуть зависимости, используйте **`pip`** (или **`pip3`**, если есть конфликт с Python2):

```bash
pip install -r requirements.txt
```
### Авторизация
Не требуется.

### Примеры
Для получения справки используйте аргумент ```-h``` или ```--help```.
Чтобы собрать свою электронную библиотеку нужно выполнить несколько шагов.

1. Парсинг книг по id:
- скачиваем данный репозиторий
- устанавливаем зависимости
- создаем виртуальное окружение проекта
- следующей командой запускаем скрипт для наполнения библиотеки:
```bash
$ python parse_tululu.py -h
```
Вывод:
```
usage: parse_tululu.py [-h] [start_id] [end_id]

Скачивание книг из библиотеки tululu.org

positional arguments:
  start_id    Ввести номер первой книги
  end_id      Ввести номер последней книги

options:
  -h, --help  show this help message and exit
```
По умолчанию значение **`start_id`** и **`end_id`** равно 1.

Для получения информации для определенного диапазона книг необходимо в запросе 
указать параметры **`start_id`** и **`end_id`**: 
```bash
$ python parse_tululu.py 6 10
```
- выбранные файлы скачиваются в папки **`book`** и **`image`**.
- информация о скачанных книгах будет выведена в консоль:
```
Всего получено 4 книг:

   Книга № 1.
   Название: Бархатная революция в рекламе.
   Автор: Зимен Сержио
   Комментарии:
    - Книга для настоящий рекламщиков!
    - Это просто история жизни одного рекламщика. А где он "предланает свой 
    революционный взгляд" так и не понятно!
    - Очень познавательная книга, расскрывающая глаза на многие вещи.
    - Интересная книга.
    - Все вокруг да около! Ни слова о сути!

   Книга № 2.
   Название: Бизнес-разведка.
   Автор: Доронин Алекcандр Иванович

   Книга № 3.
   Название: Бизнес путь: Джек Уэлч. 10 секретов величайшего в мире короля менеджмента.
   Автор: Крейнер Стюарт
   Комментарии:
    - Рекомендую.
    - Прочитал от корки до корки... Книга отличная, рекомендую прочитать, особенно 
    бизнесменам..
    - Мне понравилось.
    - Очень познавательная и интересная книга. Очень советую тем кто руководит или 
    пытается это делать.
    - Отличная книга.
    - Книга очень интересная, всем советую.

   Книга № 4.
   Название: Бизнес путь: Amazon.com.
   Автор: Саундерс Ребекка
   Комментарии:
    - Отличная книга!
    - Interesno.
```

2. Собираем библиотеку из книг категории "научная фантастика", по выбранным страницам сайта [tululu.org](https://tululu.org/l55/).
- в виртуальном окружении запускаем файл **`parse_tululu_category.py`**:
```bash
$ python parse_tululu_category.py -h
```
Вывод:
```bash
usage: parse_tululu_category.py [-h] [--start_page START_PAGE] [--end_page END_PAGE] 
                                [--dest_folder DEST_FOLDER] [--json_path JSON_PATH] 
                                [--skip_imgs] [--skip_txt]

Скачивание книг из раздела научной фантастики библиотеки tululu.org

options:
  -h, --help            show this help message and exit
  --start_page START_PAGE
                        Ввести номер первой страницы
  --end_page END_PAGE   Ввести номер последней страницы
  --dest_folder DEST_FOLDER
                        Указать путь к каталогу с результатами парсинга
  --json_path JSON_PATH
                        Указать свой путь к *.json файлу с результатами
  --skip_imgs           Hе скачивать картинки
  --skip_txt            Не скачивать книги
```
- для получения информации для определенного диапазона книг в запросе необходимо 
указать параметры:\
**`start_page`** — страница для скачинвания (по умолчанию значение 1)\
**`end_page`** —  последняя страница для скачивания. Если данный параметр не указан, либо указан, но равен или менее
start_page, то парсер скачает все страницы сайта данной категории, начиная со **`start_page`**.\
**`dest_folder`** — путь к каталогу с результатами парсинга: картинкам, книгам, JSON.\
**`json_path`** — путь к *.json файлу с результатами\
**`skip_imgs`** — не скачивать картинки\
**`skip_txt`** — не скачивать книги

При парсинге в консоль выводятся url-адреса скачиваемых книг.\
Ввод следующих команд:
```bash
$ python parse_tululu_category.py --start_page 700 --end_page 699
```
или 
```bash
$ python parse_tululu_category.py --start_page 700
```
-> cкачает все книги, находящиеся на страницах 700, 701 (последняя).
- для создания необходимых для сайта страниц **'index.html'** и отладки кода запустите файл
**`render_website.py`**:
```bash
$ python render_website.py
```
или 
```bash
$ python render_website.py -bs /путь/к/файлу/<имя файла>.json
```
где **`-bs`** (**`--books_source`**) - опциональный аргумент для пути к файлу с описанием книг 
(по умолчанию - 'books.json') 

- проверьте правильность вывода макета сайта:
```bash
[I 230310 00:21:39 server:335] Serving on http://127.0.0.1:5500
[I 230310 00:21:39 handlers:62] Start watching changes
[I 230310 00:21:39 handlers:64] Start detecting changes
```
- чтобы открыть онлайн-библиотеку перейдите по ссылке [http://127.0.0.1:5500](http://127.0.0.1:5500) 
или [http://localhost:5500/](http://localhost:5500/), либо введите одну из указанных ссылок в браузере на 
вашем локальном копьютере.

Пример:

![image](https://i.paste.pics/MF0DY.png)

- при необходимости внесите изменения в [шаблон](templates/template.html).


3. Для запуска библиотеки **оффлайн** выполните следующие действия:
- создайте на компьютере отдельную папку под библиотеку; 
- скачайте из репозитория и сохраните в данной папке директории [html_pages](html_pages), [media](media), 
[static](static), а также файл [index.html](index.html);
- запустите файл [index.html](index.html) и пользуйтесь собственной электронной библиотекой.

Пример сайта:  [https://prikur76.github.io/parse_library/index.html](https://prikur76.github.io/parse_library/index.html)

![screenshot](https://i.paste.pics/ME7GM.png)

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org).

### Лицензия

Этот проект лицензирован по лицензии MIT - подробности см. в файле [ЛИЦЕНЗИЯ](LICENSE).
