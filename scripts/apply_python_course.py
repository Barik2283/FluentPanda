import json
from pathlib import Path

root=Path(__file__).resolve().parents[1]
html_path=root/'index.html'
html=html_path.read_text()

# Add Python to the language registry.
marker='LANGS.ja.flag=FLAGS.ja;LANGS.ko.flag=FLAGS.ko;'
lang_patch='''LANGS.ja.flag=FLAGS.ja;LANGS.ko.flag=FLAGS.ko;
// v6: Python course
Object.assign(LANGS,{py:{name:'Python',nameEn:'Python',code:'PY',tts:'en-US'}});
Object.assign(FLAGS,{py:'🐍'});Object.assign(LANG_EN,{py:'Python'});LANGS.py.flag=FLAGS.py;'''
if html.count(marker)!=1:
    raise SystemExit('language marker count mismatch')
html=html.replace(marker,lang_patch,1)

words=[
('py_v1','print()','вывести на экран','output text','py_basics','🖨️','Печатает значение или текст.','Prints a value or text.','print("Привет!")','Выводим приветствие.','Print a greeting.'),
('py_v2','# comment','комментарий','comment','py_basics','💬','Комментарий объясняет код и не выполняется.','A comment explains code and is not executed.','# Это заметка','Оставляем пояснение для себя.','Leave a note for yourself.'),
('py_v3','name = "Mia"','переменная','variable','py_basics','📦','Переменная хранит значение под именем.','A variable stores a value under a name.','name = "Mia"','Сохраняем имя в переменной.','Store a name in a variable.'),
('py_v4','input()','ввод с клавиатуры','keyboard input','py_basics','⌨️','Читает строку, которую ввёл пользователь.','Reads a line typed by the user.','name = input("Имя: ")','Получаем имя пользователя.','Get the user name.'),
('py_v5','import','подключить модуль','import a module','py_basics','🧩','Подключает готовый модуль Python.','Loads a ready-made Python module.','import random','Подключаем модуль случайных чисел.','Load the random module.'),
('py_t1','int','целое число','integer','py_types','🔢','Тип для целых чисел без дробной части.','A type for whole numbers.','age = int("20")','Преобразуем текст в целое число.','Convert text to an integer.'),
('py_t2','float','дробное число','decimal number','py_types','🎯','Тип для чисел с дробной частью.','A type for numbers with a decimal part.','price = 4.5','Цена может быть дробным числом.','A price can be a decimal number.'),
('py_t3','str','строка','string','py_types','🔤','Тип для текста.','A type for text.','city = str("Казань")','Храним город как текст.','Store a city as text.'),
('py_t4','bool','логическое значение','boolean','py_types','✅','Значение True или False.','A True or False value.','is_ready = True','Проверяем, готово ли приложение.','Check whether the app is ready.'),
('py_t5','type()','узнать тип','get a type','py_types','🔎','Показывает тип значения.','Shows the type of a value.','type(42)','Проверяем тип числа.','Check the type of a number.'),
('py_s1','+','сложить или склеить','add or join','py_strings','➕','Складывает числа или соединяет строки.','Adds numbers or joins strings.','"Привет, " + name','Соединяем две строки.','Join two strings.'),
('py_s2','f"..."','f-строка','f-string','py_strings','🧵','Вставляет значения прямо в текст.','Puts values directly into text.','f"Привет, {name}!"','Вставляем имя в строку.','Insert a name into a string.'),
('py_s3','len()','длина','length','py_strings','📏','Возвращает количество символов или элементов.','Returns the number of characters or items.','len("Python")','Считаем символы в слове.','Count characters in a word.'),
('py_s4','int("7")','преобразование','conversion','py_strings','🔄','Превращает значение в другой тип.','Converts a value to another type.','number = int("7")','Делаем число из текста.','Make a number from text.'),
('py_s5','round()','округлить','round a number','py_strings','🔘','Округляет число до нужной точности.','Rounds a number to a chosen precision.','round(3.1415, 2)','Округляем до двух знаков.','Round to two decimal places.'),
('py_c1','if','если','if','py_conditions','❓','Запускает блок, если условие истинно.','Runs a block when a condition is true.','if score >= 60:','Проверяем результат.','Check a result.'),
('py_c2','elif','иначе если','else if','py_conditions','↪️','Проверяет следующее условие.','Checks the next condition.','elif score >= 40:','Добавляем второй вариант.','Add a second option.'),
('py_c3','else','иначе','else','py_conditions','🔀','Запускает запасной вариант.','Runs the fallback branch.','else: print("Попробуй ещё")','Показываем сообщение в остальных случаях.','Show a message otherwise.'),
('py_c4','==','равно','is equal to','py_conditions','⚖️','Сравнивает два значения.','Compares two values.','answer == "да"','Проверяем ответ пользователя.','Check the user answer.'),
('py_c5','and','и','and','py_conditions','🤝','Требует выполнения обоих условий.','Requires both conditions to be true.','age >= 18 and has_id','Проверяем два условия сразу.','Check two conditions at once.'),
('py_c6','or','или','or','py_conditions','🔗','Достаточно выполнения одного условия.','One true condition is enough.','tea or coffee','Выбираем один из вариантов.','Choose one of two options.'),
('py_l1','for','цикл по элементам','loop over items','py_loops','🔁','Повторяет блок для каждого элемента.','Repeats a block for each item.','for word in words:','Перебираем слова.','Loop through words.'),
('py_l2','while','пока','while','py_loops','⏳','Повторяет блок, пока условие истинно.','Repeats while a condition is true.','while tries > 0:','Повторяем попытки.','Repeat attempts.'),
('py_l3','range()','диапазон','range','py_loops','📐','Создаёт последовательность чисел.','Creates a sequence of numbers.','range(3)','Получаем числа 0, 1 и 2.','Get 0, 1, and 2.'),
('py_l4','break','остановить цикл','stop a loop','py_loops','🛑','Немедленно выходит из цикла.','Exits the loop immediately.','if found: break','Останавливаем поиск после успеха.','Stop searching after success.'),
('py_l5','continue','пропустить шаг','skip an iteration','py_loops','⏭️','Переходит к следующей итерации.','Moves to the next iteration.','if empty: continue','Пропускаем пустой элемент.','Skip an empty item.'),
('py_col1','list','список','list','py_collections','📝','Изменяемая последовательность элементов.','A mutable sequence of items.','words = ["hi", "bye"]','Создаём список слов.','Create a list of words.'),
('py_col2','[]','пустой список','empty list','py_collections','📋','Скобки создают пустой список.','Brackets create an empty list.','items = []','Начинаем с пустого списка.','Start with an empty list.'),
('py_col3','.append()','добавить в список','append to a list','py_collections','➕','Добавляет элемент в конец списка.','Adds an item to the end of a list.','items.append("book")','Добавляем книгу в список.','Add a book to the list.'),
('py_col4','dict','словарь','dictionary','py_collections','📖','Хранит пары «ключ — значение».','Stores key-value pairs.','user = {"name": "Mia"}','Храним данные пользователя.','Store user data.'),
('py_col5','{"name": "Mia"}','пара ключ-значение','key-value pair','py_collections','🗝️','Ключ name связан со значением Mia.','The key name maps to the value Mia.','user["name"]','Получаем имя из словаря.','Read a name from a dictionary.'),
('py_col6','tuple','кортеж','tuple','py_collections','📦','Неизменяемая последовательность элементов.','An immutable sequence of items.','point = (10, 20)','Храним координаты точки.','Store point coordinates.'),
('py_f1','def','объявить функцию','define a function','py_functions','🛠️','Начинает объявление функции.','Starts a function definition.','def greet(name):','Создаём функцию приветствия.','Define a greeting function.'),
('py_f2','return','вернуть значение','return a value','py_functions','↩️','Возвращает результат из функции.','Returns a result from a function.','return "Привет, " + name','Возвращаем готовую строку.','Return a ready string.'),
('py_f3','parameter','параметр','parameter','py_functions','🎛️','Имя входного значения внутри функции.','The name of an input inside a function.','def add(a, b):','Описываем два параметра.','Define two parameters.'),
('py_f4','argument','аргумент','argument','py_functions','📨','Конкретное значение при вызове функции.','A concrete value passed to a function.','greet("Mia")','Передаём имя функции.','Pass a name to the function.'),
('py_f5','lambda','короткая функция','short function','py_functions','⚡','Небольшая функция в одном выражении.','A small function written in one expression.','double = lambda x: x * 2','Создаём короткую функцию.','Create a short function.'),
('py_f6','from ... import ...','импортировать часть модуля','import part of a module','py_functions','📥','Импортирует только нужное имя.','Imports only the name you need.','from math import sqrt','Берём sqrt из math.','Import sqrt from math.'),
]

word_js=[]
for wid,code,ru,en,topic,emo,use_ru,use_en,ex,ex_ru,ex_en in words:
    word_js.append({'id':wid,'code':code,'ru':ru,'en':en,'topic':topic,'emo':emo,'use_ru':use_ru,'use_en':use_en,'ex':ex,'ex_ru':ex_ru,'ex_en':ex_en})
word_json=json.dumps(word_js,ensure_ascii=False,separators=(',',':'))
word_patch=f'''\nconst PY_WORD_DEFS={word_json};\nWORDS.py=PY_WORD_DEFS.map(d=>{{const w=W(d.id,d.code,d.ru,d.topic);w.en=d.en;return w;}});\nPY_WORD_DEFS.forEach(d=>{{WX[d.id]=['',d.emo,d.use_ru,d.ex,d.ex_ru];WXE[d.id]={{use:d.use_en,exTr:d.ex_en}};}});\nconst PY_LESSON_DEFS=[\n  {{title:'Печатаем первый код',titleEn:'Your first code',ids:['py_v1','py_v2','py_v3','py_v4','py_v5']}},\n  {{title:'Типы данных',titleEn:'Data types',ids:['py_t1','py_t2','py_t3','py_t4','py_t5']}},\n  {{title:'Строки и числа',titleEn:'Strings and numbers',ids:['py_s1','py_s2','py_s3','py_s4','py_s5']}},\n  {{title:'Условия',titleEn:'Conditions',ids:['py_c1','py_c2','py_c3','py_c4','py_c5','py_c6']}},\n  {{title:'Циклы',titleEn:'Loops',ids:['py_l1','py_l2','py_l3','py_l4','py_l5']}},\n  {{title:'Списки и словари',titleEn:'Lists and dictionaries',ids:['py_col1','py_col2','py_col3','py_col4','py_col5','py_col6']}},\n  {{title:'Функции',titleEn:'Functions',ids:['py_f1','py_f2','py_f3','py_f4','py_f5','py_f6']}}\n];\n'''
marker='for(const l of [\'ja\',\'ko\'])addLangX(l,BASIC_NEW[l].map((r,i)=>[\'b\'+(i+1),r[0],r[1],r[2],r[3],r[4],\'\',\'\',\'\',\'\',\'\']));'
if html.count(marker)!=1:
    raise SystemExit('word marker count mismatch')
html=html.replace(marker,marker+word_patch,1)

# Make lesson path use the custom Python grouping.
old="function lessonsFor(lang){\n  const ws=words(lang),out=[];"
new="function lessonsFor(lang){\n  if(lang==='py')return PY_LESSON_DEFS.map((d,i)=>({id:'py_l'+(i+1),n:i+1,title:uiL()==='en'?d.titleEn:d.title,words:d.ids.map(id=>WORDS.py.find(w=>w.id===id)).filter(Boolean)}));\n  const ws=words(lang),out=[];"
if html.count(old)!=1:
    raise SystemExit('lessons marker count mismatch')
html=html.replace(old,new,1)

# Add translated topic labels.
topics_marker="const TOPICS_EN={basics:'Basic words',food:'Food & drinks',travel:'Travel',city:'City',family:'Family',verbs:'Verbs',spell:'Spelling',stress:'Word stress',vocab:'Vocabulary'};"
topics_patch=topics_marker+"\nObject.assign(TOPICS,{py_basics:'Основы Python',py_types:'Типы данных',py_strings:'Строки и числа',py_conditions:'Условия',py_loops:'Циклы',py_collections:'Коллекции',py_functions:'Функции'});\nObject.assign(TOPICS_EN,{py_basics:'Python basics',py_types:'Data types',py_strings:'Strings & numbers',py_conditions:'Conditions',py_loops:'Loops',py_collections:'Collections',py_functions:'Functions'});"
if html.count(topics_marker)!=1:
    raise SystemExit('topics marker count mismatch')
html=html.replace(topics_marker,topics_patch,1)

# Add Python learning stories after the common story extensions.
stories_marker="Object.keys(EXTRA_STORIES).forEach(l=>{STORIES[l]=(STORIES[l]||[]).concat(EXTRA_STORIES[l]);});"
stories=[
 {'id':'py_story1','title':'Первый скрипт','titleEn':'The first script','sub':'print() и переменные','diff':'easy','lines':[
  ['Панда','name = "Mia"','Создаём переменную name и сохраняем в ней имя.','Create a variable called name and store a name in it.'],
  ['Панда','print("Привет, " + name)','Склеиваем строки и выводим приветствие.','Join strings and print a greeting.'],
  ['Панда','print("Готово!")','Запускаем код и видим результат.','Run the code and see the result.']]},
 {'id':'py_story2','title':'Угадай число','titleEn':'Guess the number','sub':'Условия и ввод','diff':'medium','lines':[
  ['Игрок','answer = input("Число: ")','Получаем ответ игрока как строку.','Read the player answer as a string.'],
  ['Программа','if answer == "7":','Проверяем, совпал ли ответ с семёркой.','Check whether the answer is seven.'],
  ['Программа','    print("Верно!")','Сообщаем об успехе внутри условия.','Report success inside the condition.'],
  ['Программа','else: print("Попробуй ещё")','В остальных случаях предлагаем повторить.','Offer another try in other cases.']]},
 {'id':'py_story3','title':'Список покупок','titleEn':'Shopping list','sub':'Списки и цикл for','diff':'medium','lines':[
  ['Мия','items = ["чай", "хлеб"]','Создаём список покупок.','Create a shopping list.'],
  ['Мия','items.append("яблоко")','Добавляем ещё один элемент.','Append one more item.'],
  ['Мия','for item in items:','Берём элементы списка по одному.','Take list items one by one.'],
  ['Мия','    print(item)','Печатаем каждый товар отдельной строкой.','Print each item on its own line.']]},
 {'id':'py_story4','title':'Функция приветствия','titleEn':'A greeting function','sub':'def и return','diff':'hard','lines':[
  ['Мия','def greet(name):','Объявляем функцию с параметром name.','Define a function with a name parameter.'],
  ['Мия','    return f"Привет, {name}!"','Возвращаем f-строку с именем.','Return an f-string containing the name.'],
  ['Мия','message = greet("Алекс")','Вызываем функцию и сохраняем результат.','Call the function and store the result.'],
  ['Мия','print(message)','Показываем готовое приветствие.','Display the finished greeting.']]}
]
stories_json=json.dumps(stories,ensure_ascii=False,separators=(',',':'))
stories_patch=stories_marker+f"\nSTORIES.py={stories_json};"
if html.count(stories_marker)!=1:
    raise SystemExit('stories marker count mismatch')
html=html.replace(stories_marker,stories_patch,1)

html_path.write_text(html)


# Documentation.
readme_path=root/'README.md'
readme=readme_path.read_text()
readme_marker='## Premium и промокоды'
readme_patch='''## Курс Python\n\nВ приложение добавлен отдельный курс Python для новичков: 7 последовательных уроков — первый код, типы данных, строки и числа, условия, циклы, списки и словари, функции. В каждом уроке есть карточки и проверка знаний; прогресс сохраняется тем же способом, что и у языковых курсов. Во вкладке историй доступны 4 учебных мини-сюжета с фрагментами кода и пояснениями.\n\n'''+readme_marker
if readme.count(readme_marker)!=1: raise SystemExit('README marker mismatch')
readme_path.write_text(readme.replace(readme_marker,readme_patch,1))

changes_path=root/'CHANGES.md'
changes=changes_path.read_text()
changes_marker='# Fluent Panda — что изменено\n'
changes_patch=changes_marker+'''\n## v6 — курс Python\n- Добавлен отдельный курс Python для новичков в мини-приложение.\n- 7 уроков: первый код, типы данных, строки и числа, условия, циклы, коллекции и функции.\n- Добавлены 36 терминов с примерами, подсказками и проверкой знаний.\n- Добавлены 4 учебные истории с фрагментами Python-кода и пояснениями.\n- Прогресс курса использует существующее сохранение уроков и не затрагивает прогресс языковых курсов.\n'''
if changes.count(changes_marker)!=1: raise SystemExit('CHANGES marker mismatch')
changes_path.write_text(changes.replace(changes_marker,changes_patch,1))

