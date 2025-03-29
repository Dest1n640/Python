import sqlite3

conn = sqlite3.connect("store_database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Store (
    store_id INTEGER PRIMARY KEY,
    district TEXT,
    address TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Product (
    article INTEGER PRIMARY KEY,
    department TEXT,
    product_name TEXT,
    unit TEXT,
    quantity_per_pack INTEGER,
    price_per_pack REAL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Product_Movement (
    operation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    store_id INTEGER,
    article INTEGER,
    pack_quantity INTEGER,
    operation_type TEXT,
    FOREIGN KEY (store_id) REFERENCES Store(store_id),
    FOREIGN KEY (article) REFERENCES Product(article)
);
""")


def load_csv(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        next(file)
        for line in file:
            values = line.strip().split(",")

            store_data = (
                values[0],
                values[1],
                values[2],
            )  # store_id, district, address
            product_data = (
                values[3],
                values[4],
                values[5],
                values[6],
                values[7],
                values[8],
            )  # article и т.д.
            movement_data = (
                values[9],
                values[0],
                values[3],
                values[10],
                values[11],
            )  # date и т.д.

            # Вставка данных в таблицу Store (если запись уже существует - пропустить)
            cursor.execute(
                """
                INSERT OR IGNORE INTO Store (store_id, district, address)
                VALUES (?, ?, ?)
            """,
                store_data,
            )

            # Вставка данных в таблицу Product (если запись уже существует - пропустить)
            cursor.execute(
                """
                INSERT OR IGNORE INTO Product (article, department, product_name, unit, quantity_per_pack, price_per_pack)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                product_data,
            )

            # Вставка данных в таблицу Product_Movement
            cursor.execute(
                """
                INSERT INTO Product_Movement (date, store_id, article, pack_quantity, operation_type)
                VALUES (?, ?, ?, ?, ?)
            """,
                movement_data,
            )


# Загрузка данных из CSV-файла
load_csv("./3_19229.csv")

# SQL-запрос для получения результата
query = """
SELECT SUM(pm.pack_quantity) AS total_packs
FROM Product_Movement pm
JOIN Product p ON pm.article = p.article
JOIN Store s ON pm.store_id = s.store_id
WHERE 
    pm.operation_type = 'Поступление'
    AND pm.date BETWEEN '2023-08-02' AND '2023-08-20'
    AND p.product_name = 'Зайцы шоколадные'
    AND s.district IN ('Октябрьский', 'Прибрежный');
"""

cursor.execute(query)
result = cursor.fetchone()

# Проверка результата
if result is None or result[0] is None:
    print("Общее количество упаковок: 0")
else:
    print(f"Общее количество упаковок: {result[0]}")

conn.commit()
conn.close()
