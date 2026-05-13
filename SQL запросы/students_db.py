import csv
import sqlite3
from pathlib import Path

#Вспомогательная функция для красивого вывода результатов
def run_query(title, query):
    print(f"\n{title}")
    cursor.execute(query)
    columns = [desc[0] for desc in cursor.description]
    print(" | ".join(columns))
    for row in cursor.fetchall():
        print(" | ".join(str(val) for val in row))

BASE_DIR = Path(__file__).parent #Получаем путь к папке, в которой файл
db_path = BASE_DIR / 'students.db' #Путь к дб
#Пути к ссвшкам
csv_level_path = BASE_DIR / 'уровень_обучения.csv'
csv_type_path = BASE_DIR / 'типы_обучения.csv'
csv_naprav_path = BASE_DIR / 'направления.csv'
csv_students_path = BASE_DIR / 'студенты.csv'
paths_csv = [csv_level_path, csv_type_path, csv_naprav_path, csv_students_path]

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


#Выполнение запросов
#1
query_case = """
SELECT 
    student_surname,
    student_name,
    average_score,
    CASE
        WHEN average_score >= 90 THEN 'Отличник'
        WHEN average_score >= 75 THEN 'Хорошист'
        WHEN average_score >= 63 THEN 'Троечник'
        ELSE 'Неудовлетворительно'
    END AS успеваемость
FROM students
ORDER BY average_score DESC;
"""
run_query("CASE: Категоризация студентов по баллу", query_case)

#2
query_sub = """
SELECT 
    student_surname,
    student_name,
    average_score,
    id_naprav
FROM students
WHERE average_score > (
    SELECT AVG(average_score) 
    FROM students
)
ORDER BY average_score DESC;
"""
run_query("Подзапрос: студенты выше среднего балла", query_sub)

#3
query_cte = """
WITH рейтинг_студентов AS (
    SELECT 
        s.id_student,
        s.student_surname,
        s.student_name,
        s.average_score,
        n.name AS направление,
        ROW_NUMBER() OVER (
            PARTITION BY s.id_naprav 
            ORDER BY s.average_score DESC
        ) AS место_в_направлении
    FROM students s
    JOIN naprav n ON s.id_naprav = n.id_naprav
)
SELECT 
    направление,
    student_surname,
    student_name,
    average_score,
    место_в_направлении
FROM рейтинг_студентов
WHERE место_в_направлении <= 2
ORDER BY направление, место_в_направлении;
"""
run_query("CTE: Топ-2 студента в каждом направлении", query_cte)

#Закрытие соединения
conn.close()