import sqlite3

conn = sqlite3.connect("confectionery.db")
cursor = conn.cursor()

# Пересоздание таблицы Store
cursor.execute("DROP TABLE IF EXISTS Store")
cursor.execute("""
CREATE TABLE Store (
    store_id INTEGER PRIMARY KEY,
    district TEXT,
    address TEXT
);
""")
cursor.execute(
    "INSERT INTO Store (store_id, district, address) VALUES (1, 'Октябрьский', 'ул. Ленина, 10');"
)
cursor.execute(
    "INSERT INTO Store (store_id, district, address) VALUES (2, 'Прибрежный', 'ул. Морская, 5');"
)

# Пересоздание таблицы Product
cursor.execute("DROP TABLE IF EXISTS Product")
cursor.execute("""
CREATE TABLE Product (
    article INTEGER PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    unit TEXT,
    price REAL
);
""")
cursor.execute(
    "INSERT INTO Product (article, product_name, category, unit, price) VALUES (101, 'Шоколадные зайцы', 'Кондитерские изделия', 'упаковка', 150.0);"
)

# Пересоздание таблицы Product_Movement
cursor.execute("DROP TABLE IF EXISTS Product_Movement")
cursor.execute("""
CREATE TABLE Product_Movement (
    operation_id INTEGER PRIMARY KEY,
    date TEXT,
    store_id INTEGER,
    article INTEGER,
    pack_quantity INTEGER,
    operation_type TEXT,
    FOREIGN KEY (store_id) REFERENCES Store(store_id),
    FOREIGN KEY (article) REFERENCES Product(article)
);
""")
cursor.execute(
    "INSERT INTO Product_Movement (operation_id, date, store_id, article, pack_quantity, operation_type) VALUES (1, '2023-08-02', 1, 101, 200, 'Поступление');"
)
cursor.execute(
    "INSERT INTO Product_Movement (operation_id, date, store_id, article, pack_quantity, operation_type) VALUES (2, '2023-08-02', 2, 101, 200, 'Поступление');"
)
cursor.execute(
    "INSERT INTO Product_Movement (operation_id, date, store_id, article, pack_quantity, operation_type) VALUES (3, '2023-08-05', 1, 101, 200, 'Поступление');"
)
cursor.execute(
    "INSERT INTO Product_Movement (operation_id, date, store_id, article, pack_quantity, operation_type) VALUES (4, '2023-08-10', 2, 101, 200, 'Поступление');"
)
cursor.execute(
    "INSERT INTO Product_Movement (operation_id, date, store_id, article, pack_quantity, operation_type) VALUES (5, '2023-08-15', 1, 101, 200, 'Поступление');"
)
cursor.execute(
    "INSERT INTO Product_Movement (operation_id, date, store_id, article, pack_quantity, operation_type) VALUES (6, '2023-08-20', 2, 101, 200, 'Поступление');"
)

# Проверка данных в таблице Product_Movement
cursor.execute("SELECT * FROM Product_Movement;")
movement_data = cursor.fetchall()
print("Данные в таблице Product_Movement:")
for row in movement_data:
    print(row)

# Выполнение SQL-запроса для подсчёта общего количества упаковок шоколадных зайцев
query = """
SELECT SUM(pm.pack_quantity) AS total_packs
FROM Product_Movement pm
JOIN Store s ON pm.store_id = s.store_id
WHERE pm.article = 101 AND pm.operation_type = 'Поступление' AND s.district IN ('Октябрьский', 'Прибрежный')
AND pm.date BETWEEN '2023-08-02' AND '2023-08-20';
"""
cursor.execute(query)
result = cursor.fetchone()

print(f"Общее количество упаковок шоколадных зайцев: {result[0] if result else 0}")

conn.commit()
conn.close()
