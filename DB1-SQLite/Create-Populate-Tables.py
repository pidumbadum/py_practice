import sqlite3
import random

def generate_number():
    mobile_number = random.choice('123456789') + ''.join(random.choices('0123456789', k=9))
    return(f'+{mobile_number}')

organization =["Google", "Роскосмос", "Всемирная организация здравоохранения", "Tesla", "МГУ имени М. В. Ломоносова"]
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

# # Заполнение таблицы `job_titles
# job_titles_data = [
#     (1, 'Менеджер'),
#     (2, 'Разработчик'),
#     (3, 'Аналитик'),
#     (4, 'Дизайнер')
# ]
# cursor.executemany("INSERT OR IGNORE INTO `job_titles` (`id_job_title`, `name`) VALUES (?, ?)", job_titles_data)

# # Заполнение таблицы employees
# employees_data = [
#     (1, 'Иванов', 'Иван', 2),
#     (2, 'Петров', 'Петр', 1),
#     (3, 'Сидорова', "Мария", 3),
#     (4, 'Козлов', "Алексей", 2),
#     (5, 'Васильева', 'Ольга', 4)
# ]
# cursor.executemany("INSERT OR IGNORE INTO `employees` (`id`,`surname`,`name`, `id_job_title`) VALUES (?, ?, ?, ?)",employees_data)

orders_data = []
clients_data = []




# Сохранение изменений
connection.commit()
