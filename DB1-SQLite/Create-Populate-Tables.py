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

cursor.execute ("""
SELECT e.surname, e.name, j.name as job_title FROM employees e
JOIN job_titles j ON e.id_job_title = j.id_job_title""")

employees_with_job_titles = cursor.fetchall()
print ("Сотрудники и их должности:")
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