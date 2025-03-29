import sqlite3

# Подключение к базе данных
connection = sqlite3.connect("baza.db")
cursor = connection.cursor()

# Создание таблиц
cursor.execute("""
CREATE TABLE IF NOT EXISTS `Clients` (
    `organization` TEXT NOT NULL,
    `phone_number` TEXT NOT NULL,
    `client_id` integer primary key NOT NULL UNIQUE
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS `Positions` (
    `position_id` integer primary key NOT NULL UNIQUE,
    `name` TEXT NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS `Employees` (
    `employee_id` integer primary key NOT NULL UNIQUE,
    `last_name` TEXT NOT NULL,
    `first_name` TEXT NOT NULL,
    `phone` TEXT NOT NULL,
    `position_id` INTEGER NOT NULL,
    FOREIGN KEY(`position_id`) REFERENCES `Positions`(`position_id`)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS `Orders` (
    `order_id` integer primary key NOT NULL UNIQUE,
    `client_id` INTEGER NOT NULL,
    `employee_id` INTEGER NOT NULL,
    `amount` REAL NOT NULL,
    `completion_date` TEXT NOT NULL,
    `completion_status` TEXT NOT NULL,
    FOREIGN KEY(`client_id`) REFERENCES `Clients`(`client_id`),
    FOREIGN KEY(`employee_id`) REFERENCES `Employees`(`employee_id`)
);
""")

# Добавление данных в таблицы
positions_data = [
    (1, "Менеджер"),
    (2, "Разработчик"),
    (3, "Аналитик"),
    (4, "Дизайнер"),
]
cursor.executemany(
    "INSERT OR IGNORE INTO Positions (position_id, name) VALUES (?, ?)", positions_data
)

employees_data = [
    (1, "Иванов", "Иван", "+79001112233", 2),
    (2, "Петров", "Петр", "+79004445566", 1),
    (3, "Сидорова", "Мария", "+79007778899", 3),
    (4, "Козлов", "Алексей", "+79001234567", 2),
    (5, "Васильева", "Ольга", "+79009876543", 4),
]
cursor.executemany(
    "INSERT OR IGNORE INTO Employees (employee_id, last_name, first_name, phone, position_id) VALUES (?, ?, ?, ?, ?)",
    employees_data,
)

clients_data = [
    (1, "ООО Ромашка", "+79161112233"),
    (2, "АО Техно", "+79162223344"),
    (3, "ЗАО Альфа", "+79163334455"),
]
cursor.executemany(
    "INSERT OR IGNORE INTO Clients (client_id, organization, phone_number) VALUES (?, ?, ?)",
    clients_data,
)

orders_data = [
    (1, 1, 2, 15000.50, "2024-05-01", "Завершен"),
    (2, 2, 3, 20000.00, "2024-06-15", "В процессе"),
    (3, 3, 1, 5000.75, "2024-07-10", "Ожидание"),
]
cursor.executemany(
    """
INSERT OR IGNORE INTO Orders (order_id, client_id, employee_id, amount, completion_date, completion_status)
VALUES (?, ?, ?, ?, ?, ?)
""",
    orders_data,
)

# Простые запросы COUNT / SUM / AVG / MIN / MAX

# COUNT запрос
print("Реализация запроса COUNT:")
cursor.execute("""
SELECT first_name || ' ' || last_name AS full_name, COUNT(*) AS amount_of_employees
FROM Employees
GROUP BY first_name;
""")
for row in cursor.fetchall():
    print(row)

# SUM запрос
print("Реализация запроса SUM:")
cursor.execute("""
SELECT SUM(amount) AS total_amount_of_orders
FROM Orders;
""")
result = cursor.fetchone()
print(f"Общая сумма заказов: {result[0]}")

# MIN запрос
print("Реализация запроса MIN:")
cursor.execute("""
SELECT MIN(amount) AS min_value 
FROM Orders;
""")
result = cursor.fetchone()
print(f"Минимальная цена за заказ - {result[0]}")

# MAX запрос
print("Реализация запроса MAX:")
cursor.execute("""
SELECT MAX(amount) AS max_value 
FROM Orders;
""")
result = cursor.fetchone()
print(f"Максимальная цена за заказ - {result[0]}")

# Агрегационные запросы

# COUNT заказов по статусу выполнения
print("COUNT заказов по статусу выполнения:")
cursor.execute("""
SELECT completion_status, COUNT(*) AS count_orders 
FROM Orders 
GROUP BY completion_status;
""")
for row in cursor.fetchall():
    print(row)

# AVG суммы заказов по клиентам:
print("AVG суммы заказов по клиентам:")
cursor.execute("""
SELECT Orders.client_id || ' (' || Clients.organization || ')' AS client_info,
       AVG(Orders.amount) AS average_amount 
FROM Orders 
JOIN Clients ON Orders.client_id = Clients.client_id 
GROUP BY Orders.client_id;
""")
for row in cursor.fetchall():
    print(row)

# SUM суммы заказов по сотрудникам:
print("SUM суммы заказов по сотрудникам:")
cursor.execute("""
SELECT Orders.employee_id || ' (' || Employees.first_name || ' ' || Employees.last_name || ')' AS employee_info,
       SUM(Orders.amount) AS total_amount 
FROM Orders 
JOIN Employees ON Orders.employee_id = Employees.employee_id 
GROUP BY Orders.employee_id;
""")
for row in cursor.fetchall():
    print(row)

# Объединение данных

# Сотрудники и их должности:
print("Сотрудники и их должности:")
cursor.execute("""
SELECT Employees.first_name || ' ' || Employees.last_name AS full_name,
       Positions.name AS position_name 
FROM Employees 
JOIN Positions ON Employees.position_id = Positions.position_id;
""")
for row in cursor.fetchall():
    print(row)

# Заказы и информация о клиентах:
print("Заказы и информация о клиентах:")
cursor.execute("""
SELECT Orders.order_id || ' (' || Clients.organization || ')' AS order_info,
       Orders.amount || ' (' || Orders.completion_status || ')' as order_details 
FROM Orders 
JOIN Clients ON Clients.client_ID=Orders.client_ID;
""")
for row in cursor.fetchall():
    print(row)

# Сотрудники и обработанные ими заказы:
print("Сотрудники и обработанные ими заказы:")
cursor.execute("""
SELECT Employees.first_name || ' ' || Employees.last_name AS full_name,
       Employees.phone AS phone_number,
       SUM(Orders.amount) AS total_orders_handled 
FROM Employees 
JOIN Orders ON Employees.employee_ID=Orders.employee_ID 
GROUP BY Employees.employee_ID;
""")
for row in cursor.fetchall():
    print(row)

connection.commit()
connection.close()
