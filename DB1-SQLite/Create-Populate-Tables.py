import sqlite3
import random
from datetime import date, timedelta

def get_spaces(string, max = 21):
    return (max - len(str(string)) - 1) * ' ' + '|' 

def get_random_date(start_date, end_date):
    # Разница между датами
    delta = end_date - start_date
    int_delta = (delta.days * 24 * 60 * 60)
    # Случайная секунда в этом диапазоне
    random_second = random.randrange(int_delta)
    return start_date + timedelta(seconds=random_second)

def generate_number():
    mobile_number = random.choice('123456789') + ''.join(random.choices('0123456789', k=9))
    return(f'+{mobile_number}')

organization =["Google", "Роскосмос", "ВОЗ", "Tesla", "МГУ М.В. Ломоносова"]
#Подключение
connection = sqlite3.connect('base.db')
cursor = connection.cursor()

# Метод cursor.execute используется для выполнения SQLзапросов:
# •SELECT (выборка данных),
# •INSERT (вставка данных),
# •UPDATE (обновление данных),
# •DELETE (удаление данных),
# •CREATE TABLE (создание
# таблиц) и другие

#создание
cursor.execute("""
    CREATE TABLE IF NOT EXISTS 'job_titles' (
    id_job_title integer primary key NOT NULL UNIQUE,
    name TEXT NOT NULL)
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
    `id_employees` integer primary key NOT NULL UNIQUE,
    `surname` TEXT NOT NULL,
    `name` TEXT NOT NULL,
    `id_job_title` INTEGER NOT NULL,
    FOREIGN KEY(`id_job_title`) REFERENCES `job_titles`(`id_job_title`)
)
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS `orders` (
    `id_order` integer primary key NOT NULL UNIQUE,
    `id_client` TEXT NOT NULL,
    `id_employ` TEXT NOT NULL,
    `sum` INTEGER NOT NULL,
    `due_date` TEXT NOT NULL,
    `progress_mark` BOOLEAN NOT NULL,
    FOREIGN KEY(`id_employ`) REFERENCES `employees`(`id_employees`),
    FOREIGN KEY(`id_client`) REFERENCES `clients`(`id_clients`)
)
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS `clients` (
    `id_clients` integer primary key NOT NULL UNIQUE,
    `organization` TEXT NOT NULL,
    `phone_number` TEXT NOT NULL
)
""")

# Заполнение таблицы `job_titles
job_titles_data = [
    (1, 'Менеджер'),
    (2, 'Разработчик'),
    (3, 'Аналитик'),
    (4, 'Дизайнер')
]
cursor.executemany("INSERT OR IGNORE INTO `job_titles` (`id_job_title`, `name`) VALUES (?, ?)", job_titles_data)

# Заполнение таблицы employees
employees_data = [
    (1, 'Иванов', 'Иван', 2),
    (2, 'Петров', 'Петр', 1),
    (3, 'Сидорова', "Мария", 3),
    (4, 'Козлов', "Алексей", 2),
    (5, 'Васильева', 'Ольга', 4)
]
cursor.executemany("INSERT OR IGNORE INTO `employees` (`id_employees`,`surname`,`name`, `id_job_title`) VALUES (?, ?, ?, ?)",employees_data)

orders_data = []
clients_data = []

for i in range(1,6):
    clients_data.append((i, organization[i-1], generate_number()))

for i in range(1,10):
    orders_data.append((i, (random.randint(1, len(clients_data))), random.randint(1, len(employees_data)), 
                       random.randint(1000, 10000), str(get_random_date(date(2000,1,1),date(2026,12,31))), random.choice([True, False])))


cursor.executemany("INSERT OR IGNORE INTO `orders` (`id_order`, `id_client`, `id_employ`,`sum`, `due_date`, `progress_mark`) VALUES (?, ?, ?, ?, ?, ?)",orders_data)
cursor.executemany("INSERT OR IGNORE INTO `clients` (`id_clients`, `organization`, `phone_number`) VALUES (?, ?, ?)", clients_data)

# Сохранение изменений
connection.commit()

#ЗАПРОС Штаб сотрудников
cursor.execute("""
    SELECT j.name, COUNT(e.id_employees) as `count_employees`
    FROM `job_titles` j
    JOIN `employees` e ON j.id_job_title = e.id_job_title
    GROUP BY j.id_job_title
""")
print(f'\nШтаб сотрудников:')
for row in cursor.fetchall():
    print(f"{row[0]} - {row[1]} сотрудников")

cursor.execute ("""
SELECT e.surname, e.name, j.name as job_title FROM employees e
JOIN job_titles j ON e.id_job_title = j.id_job_title""")
employees_with_job_titles = cursor.fetchall()
print ("\nСотрудники и их должности:")
for employee in employees_with_job_titles:
    print(f"{employee[0]} {employee[1]} - {employee[2]}")

cursor.execute("""
    SELECT o.id_order, 
           cl.organization, 
           e.surname || ' ' || e.name AS employee_fio, 
           o.sum, 
           o.due_date, 
           o.progress_mark 
    FROM orders o
    JOIN clients cl ON o.id_client = cl.id_clients
    JOIN employees e ON o.id_employ = e.id_employees
""")

orders_with_details = cursor.fetchall()
print("\nЗаказы:")
print(f"Код заказа{get_spaces('Код заказа')} Клиент{get_spaces('Клиент')} Сотрудник{get_spaces('Сотрудник')} Сумма{get_spaces('Сумма')} Срок{get_spaces('Срок')} Статус{get_spaces('Статус')}")

for order in orders_with_details:
    status = " Выполнен" if order[5] else " В работе"
    
    print(f"{order[0]}{get_spaces(order[0])} "
          f"{order[1]}{get_spaces(order[1])} "
          f"{order[2]}{get_spaces(order[2])} "
          f"{order[3]}{get_spaces(order[3])} "
          f"{order[4]}{get_spaces(order[4])} "
          f"{status}{get_spaces(status)}")
    
#А теперь запросики
# Всего заказов в базе
cursor.execute("SELECT COUNT(*) FROM `orders`")
total_orders = cursor.fetchone()[0]
print(f"\nВсего заказов: {total_orders}")

# Сколько заказов у каждого сотрудника
cursor.execute("""
    SELECT e.surname, e.name, COUNT(o.id_order) as order_count
    FROM employees e
    LEFT JOIN `orders` o ON e.id_employees = o.id_employ
    GROUP BY e.id_employees
    ORDER BY order_count DESC
""")
for row in cursor.fetchall():
    print(f"{row[0]} {row[1]} — {row[2]} заказов")

#выручка
cursor.execute("SELECT SUM(`sum`) FROM `orders`")
total_revenue=cursor.fetchone()[0] or 0
print(f'\nОбщая выручка: {total_revenue}')
#Самый дорогой клиент
cursor.execute("""
    SELECT c.organization, SUM(o.sum) as client_revenue
    FROM clients c
    JOIN `orders` o ON c.id_clients = o.id_client
    GROUP BY c.id_clients
    ORDER BY client_revenue DESC
""")
favorite_clien =[0, 0]
for row in cursor.fetchall():
    if row[1] > favorite_clien[1]:
        favorite_clien = row
    print(f'{row[0]} заказали на {row[1]} руб.')
print(f'\nСамый прибыльный клиент: {favorite_clien[0]}')

# Средняя сумма заказа
cursor.execute("SELECT AVG(`sum`) FROM `orders`")
avg_sum = cursor.fetchone()[0]
print(f"\nСредняя сумма заказа: {avg_sum:.2f} руб.")

# Самый дорогой и самый дешёвый заказ
cursor.execute("SELECT MAX(`sum`), MIN(`sum`) FROM `orders`")
max_s, min_s = cursor.fetchone()
print(f"Макс. заказ: {max_s} руб. | Мин. заказ: {min_s} руб.")

# Дата самого раннего и позднего заказа
cursor.execute("SELECT MIN(due_date), MAX(due_date) FROM `orders`")
min_date, max_date = cursor.fetchone()
print(f"Заказы с {min_date} по {max_date}")

#Сложные запросы
#Дорогие и выполненные заказы
cursor.execute("""
    SELECT o.id_order, cl.organization, e.name, o.sum 
    FROM orders o
    JOIN clients cl ON o.id_client = cl.id_clients
    JOIN employees e ON o.id_employ = e.id_employees
    WHERE o.progress_mark = 1 AND o.sum > ?
    ORDER BY o.sum DESC
""", (avg_sum,))

result = cursor.fetchall()
print("\nПрибыльные выполненные заказы:")
for row in result:
    print(f"Заказ {row[0]}: Клиент - {row[1]}; Сотрудник - {row[2]}; Сумма: {row[3]}")

#Отчет по сотрудникам
id_otchet= input('\nВведите код должности для получения отчета: ')
cursor.execute("""
    SELECT e.surname, e.name, j.name, COUNT(o.id_order) as total_orders
    FROM employees e
    JOIN job_titles j ON e.id_job_title = j.id_job_title
    LEFT JOIN orders o ON e.id_employees = o.id_employ
    WHERE j.id_job_title = ?
    GROUP BY e.id_employees
""", (id_otchet,))

result = cursor.fetchall()
if not result:
    print("Сотрудников с таким кодом должности не найдено.")
else:
    job_name = result[0][2] 
    print(f"\nОтчет по должности: {job_name}")
    for row in result:
        print(f"Сотрудник {row[0]} {row[1]} выполнил(a) заказов: {row[3]}")

#НАКОНЕЦ история заказов для конкретного клиента
id_client= input('\nВведите код заказчика для получения отчета: ')
cursor.execute("""
    SELECT o.due_date, cl.organization, e.surname, o.progress_mark
    FROM clients cl
    JOIN orders o ON cl.id_clients = o.id_client
    JOIN employees e ON o.id_employ = e.id_employees
    WHERE cl.id_clients = ?
    ORDER BY o.due_date ASC
""",(id_client))

result = cursor.fetchall()
if not result:
    print("Клиентов с таким кодом должности не найдено.")
else:
    client = result[0][1]
    print(f"\nЗаказы от {client}")
    for row in result:
        status = "Готово" if row[3] else "В процессе"
        print(f"Срок: {row[0]}, Ответственный: {row[2]}, Статус: {status}")