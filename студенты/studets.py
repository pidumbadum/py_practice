import csv
import sqlite3
from pathlib import Path

def get_spaces(string, max = 21):
    return (max - len(str(string)) - 1) * ' ' + '|' 

BASE_DIR = Path(__file__).parent #Получаем путь к папке, в которой файл
db_path = BASE_DIR / 'students.db' #Путь к дб
#Пути к ссвшкам
csv_level_path = BASE_DIR / 'уровень_обучения.csv'
csv_type_path = BASE_DIR / 'типы_обучения.csv'
csv_naprav_path = BASE_DIR / 'направления.csv'
csv_students_path = BASE_DIR / 'студенты.csv'
paths_csv = [csv_level_path, csv_type_path, csv_naprav_path, csv_students_path]
# study_level = pd.read_csv('уровень_обучения.csv')
# study_type = pd.read_csv('типы_обучения.csv')
# naprav = pd.read_csv('направления.csv')
# sudents = pd.read_csv('студенты.csv')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS `study_level`(
               id_st_level INTEGER PRIMARY KEY,
               name TEXT)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS `study_type`(
               id_st_type INTEGER PRIMARY KEY,
               name TEXT)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS `naprav`(
               id_naprav INTEGER PRIMARY KEY,
               name TEXT)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS `students`(
               id_student INTEGER PRIMARY KEY,
               id_st_level INTEGER,
               id_naprav INTEGER,
               id_st_type INTEGER,
               student_name TEXT,
               student_surname TEXT,
               student_patronymic TEXT,
               average_score INTEGER,
               FOREIGN KEY (id_st_level) REFERENCES `study_level`(id_st_level),
               FOREIGN KEY (id_naprav) REFERENCES `naprav`(id_naprav),
               FOREIGN KEY (id_st_type) REFERENCES `study_type`(id_st_type))
               """)
# paths_csv = [csv_level_path, csv_type_path, csv_naprav_path, csv_students_path]
for i in range(len(paths_csv)):
    with open(paths_csv[i], 'r') as file:
        reader = csv.reader(file)
        next(reader)
        match i:
            case 0:
                cursor.executemany('INSERT OR REPLACE INTO `study_level` (id_st_level, name) VALUES (?, ?)', reader)
            case 1:
                cursor.executemany('INSERT OR REPLACE INTO `study_type` (id_st_type, name) VALUES (?, ?)', reader)
            case 2:
                cursor.executemany('INSERT OR REPLACE INTO `naprav` (id_naprav, name) VALUES (?, ?)', reader)
            case 3:
                cursor.executemany('''INSERT OR REPLACE INTO `students` (id_student, id_st_level, id_naprav, 
                                   id_st_type, student_name, student_surname, student_patronymic, average_score) VALUES (?, ?,?, ?,?, ?,?, ? )''', reader)
                  
conn.commit()

#Далее запросы по порядку
cursor.execute("""SELECT st.student_name, st.student_surname, st.student_patronymic
               FROM `students` as st""")

i = 1
students_names = cursor.fetchall()
print(f"Количество студентов: {len(students_names)}\nСписок студентов: ")
for row in students_names:
    print(f"{i} {row[0]} {row[2]} {row[2]}")
    i+=1
i = None

cursor.execute("""SELECT n.name, COUNT (st.id_naprav) as count_students 
               FROM `naprav` as n
               JOIN students as st ON n.id_naprav = st.id_naprav
               GROUP BY n.id_naprav""")

print(f"\nКоличество студентов по направлениям")
print(f"кол-во студентов {get_spaces('кол-во студентов', len('кол-во студентов') + 1)} Направление")
for row in cursor.fetchall():
    print(f"{row[1]}{get_spaces(row[1], len('кол-во студентов') + 2)} {row[0]}")

print(f"\nСтатистика по баллам:")
cursor.execute("""SELECT n.name, MAX(st.average_score), 
               MIN(st.average_score), 
               ROUND(AVG(st.average_score), 2) FROM `students` as st
               JOIN `naprav` as n ON st.id_naprav = n.id_naprav
               GROUP BY st.id_naprav, n.name
               """)
for row in cursor.fetchall():
    print('_'*15)
    print(f"\n{row[0]} \nМакс. балл: {row[1]}\nMин. балл: {row[2]}\nСредний балл: {row[3]}")

cursor.execute("""SELECT t.name, COUNT(s.id_student)
               FROM `study_type` as t
               JOIN `students` as s ON t.id_st_type = s.id_st_type
               GROUP BY t.id_st_type""")
print(f"\nКоличество студентов по формам обучения:")
print(f"кол-во студентов {get_spaces('кол-во студентов', len('кол-во студентов') + 1)} Форма обучения")
for row in cursor.fetchall():
    print(f"{row[1]}{get_spaces(row[1], len('кол-во студентов') + 2)} {row[0]}")

cursor.execute("""SELECT n.name, l.name, t.name, ROUND(AVG(s.average_score), 2)
               FROM `students` as s
               JOIN `naprav` as n ON s.id_naprav = n.id_naprav
               JOIN `study_level` as l ON s.id_st_level = l.id_st_level
               JOIN `study_type` as t ON s.id_st_type = t.id_st_type
               GROUP BY n.id_naprav, l.id_st_level, t.id_st_type""")
print(f"\nСредний балл по направлениям, уровням и формам обучения:")
print(f"Направление{get_spaces('Направление', len('Направление') + 5)} Уровень{get_spaces('Уровень', len('Уровень') + 5)}Форма{get_spaces('Форма', len('Форма') + 5)} Средний балл")
for row in cursor.fetchall():
    print(f"{row[0]}{get_spaces(row[0], len('Направление') + 5)} {row[1]}{get_spaces(row[1], len('Уровень') + 5)} {row[2]}{get_spaces(row[2], len('Форма') + 5)} {row[3]}")

cursor.execute("""SELECT s.student_name, s.student_patronymic, s.student_surname, s.average_score
               FROM `students` as s
               JOIN `naprav` as n ON s.id_naprav = n.id_naprav
               JOIN `study_type` as t ON s.id_st_type = t.id_st_type
               WHERE n.name = 'Информатика' 
                 AND t.name = 'очная'
               ORDER BY s.average_score DESC 
               LIMIT 5""")
print(f"\nСтуденты для приказа о повышенной стипендии (Информатика, очная):")
for i, row in enumerate(cursor.fetchall(), 1):
    print(f"{i}. {row[0]} {row[2]} {row[1]} — {row[3]} баллов")

cursor.execute("""SELECT student_surname, COUNT(*) as cnt
               FROM `students`
               GROUP BY student_surname
               HAVING COUNT(*) > 1
               ORDER BY cnt DESC""")
dupes = cursor.fetchall()

print(f"\nОднофамильцы в базе (уникальных фамилий с дублями: {len(dupes)}):")
if dupes:
    print(f"Фамилия{' '*10}| Носителей")
    for row in dupes:
        print(f"{row[0]}{get_spaces(row[0], 18)} {row[1]}")
else:
    print("Однофамильцев не найдено.")

cursor.execute("""SELECT student_name, student_surname, student_patronymic, COUNT(*) as cnt
               FROM `students`
               GROUP BY student_name, student_surname, student_patronymic
               HAVING COUNT(*) > 1""")

thezki = cursor.fetchall()
if thezki:
    print(f"\nПолные тезки найдены ({len(thezki)} совпадений):")
    for row in thezki:
        print(f"{row[0]} {row[1]} {row[2]} — встречается {row[3]} раз(а)")
else:
    print(f"\nПолных тезок в базе не обнаружено.")

conn.close()
