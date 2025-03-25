import sqlite3

connection = sqlite3.connect("baza.db")
cursor = connection.cursor()

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
    `completion_date` REAL NOT NULL,
    `completion_status` REAL NOT NULL,
    FOREIGN KEY(`client_id`) REFERENCES `Clients`(`client_id`),
    FOREIGN KEY(`employee_id`) REFERENCES `Employees`(`employee_id`)
);
""")

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

# Преобразование completion_date и completion_status в строковый тип, так как в SQL они REAL, но по смыслу должны быть строками
orders_data_fixed = []
for order in orders_data:
    order_list = list(order)  # Преобразуем кортеж в список для изменения
    order_list[4] = str(order_list[4])  # completion_date делаем строкой
    order_list[5] = str(order_list[5])  # completion_status делаем строкой
    orders_data_fixed.append(tuple(order_list))  # Преобразуем обратно в кортеж
orders_data = orders_data_fixed


cursor.executemany(
    "INSERT OR IGNORE INTO Orders (order_id, client_id, employee_id, amount, completion_date, completion_status) VALUES (?, ?, ?, ?, ?, ?)",
    orders_data,
)

connection.commit()

cursor.execute(
    """
    SELECT o.order_id, c.organization, e.last_name, e.first_name, o.amount, o.completion_date, o.completion_status
    FROM Orders o
    JOIN Clients c ON o.client_id = c.client_id
    JOIN Employees e ON o.employee_id = e.employee_id
    """
)
orders = cursor.fetchall()

print("Заказы:")
for order in orders:
    print(
        f"ID: {order[0]}, Клиент: {order[1]}, Сотрудник: {order[2]} {order[3]}, Сумма: {order[4]}, Дата: {order[5]}, Статус: {order[6]}"
    )

connection.close()
