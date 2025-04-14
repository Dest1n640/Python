import sqlite3
import tkinter as tk
from tkinter import messagebox

# Создаем соединение с базой данных
conn = sqlite3.connect("shop.db")
cursor = conn.cursor()

# Создаем таблицы
cursor.execute("""
CREATE TABLE IF NOT EXISTS Product (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price INTEGER NOT NULL,
    amount INTEGER NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Purchase (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS PurchaseDetails (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    purchase_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    amount INTEGER NOT NULL,
    purchase_price INTEGER NOT NULL,
    FOREIGN KEY (purchase_id) REFERENCES Purchase(id),
    FOREIGN KEY (product_id) REFERENCES Product(id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS SalesSummary (
    date TEXT PRIMARY KEY,
    total_amount INTEGER NOT NULL,
    total_revenue INTEGER NOT NULL
);
""")

conn.commit()

# Главное окно
root = tk.Tk()
root.title("Магазин")
root.geometry("600x400")


# Функция для добавления товара в базу данных
def add_product():
    name = entry_name.get()
    category = entry_category.get()
    price = entry_price.get()
    amount = entry_amount.get()

    if name and category and price.isdigit() and amount.isdigit():
        cursor.execute(
            """
        INSERT INTO Product (name, category, price, amount)
        VALUES (?, ?, ?, ?);
        """,
            (name, category, int(price), int(amount)),
        )
        conn.commit()
        messagebox.showinfo("Успех", "Товар добавлен!")
        entry_name.delete(0, tk.END)
        entry_category.delete(0, tk.END)
        entry_price.delete(0, tk.END)
        entry_amount.delete(0, tk.END)
    else:
        messagebox.showwarning("Ошибка", "Некорректные данные!")


# Функция для регистрации покупки
def register_purchase():
    product_id = entry_product_id.get()
    amount = entry_purchase_amount.get()

    if product_id.isdigit() and amount.isdigit():
        cursor.execute("SELECT amount, price FROM Product WHERE id = ?;", (product_id,))
        result = cursor.fetchone()

        if result and result[0] >= int(amount):
            # Создаем чек
            cursor.execute("INSERT INTO Purchase (date) VALUES (date('now'));")
            purchase_id = cursor.lastrowid

            # Обновляем склад и регистрируем покупку
            cursor.execute(
                """
            UPDATE Product SET amount = amount - ? WHERE id = ?;
            """,
                (int(amount), product_id),
            )

            cursor.execute(
                """
            INSERT INTO PurchaseDetails (purchase_id, product_id, amount, purchase_price)
            VALUES (?, ?, ?, ?);
            """,
                (purchase_id, product_id, int(amount), result[1]),
            )

            conn.commit()
            messagebox.showinfo("Успех", "Покупка зарегистрирована!")
            entry_product_id.delete(0, tk.END)
            entry_purchase_amount.delete(0, tk.END)
        else:
            messagebox.showwarning("Ошибка", "Недостаточно товара на складе!")
    else:
        messagebox.showwarning("Ошибка", "Некорректные данные!")


# Функция для отчета о продажах
def sales_report():
    date = entry_date.get()

    if date:
        cursor.execute(
            """
        SELECT SUM(pd.amount) AS total_amount, SUM(pd.amount * pd.purchase_price) AS total_revenue
        FROM Purchase p
        JOIN PurchaseDetails pd ON p.id = pd.purchase_id
        WHERE p.date = ?;
        """,
            (date,),
        )

        result = cursor.fetchone()

        if result and result[0]:
            messagebox.showinfo(
                "Отчет",
                f"Дата: {date}\nПродано товаров: {result[0]}\nВыручка: {result[1]}",
            )
        else:
            messagebox.showinfo("Отчет", "Нет продаж за указанную дату.")
    else:
        messagebox.showwarning("Ошибка", "Введите дату!")


# Интерфейс для добавления товаров
tk.Label(root, text="Добавить товар").grid(row=0, column=0, columnspan=2)

tk.Label(root, text="Название").grid(row=1, column=0)
entry_name = tk.Entry(root)
entry_name.grid(row=1, column=1)

tk.Label(root, text="Категория").grid(row=2, column=0)
entry_category = tk.Entry(root)
entry_category.grid(row=2, column=1)

tk.Label(root, text="Цена").grid(row=3, column=0)
entry_price = tk.Entry(root)
entry_price.grid(row=3, column=1)

tk.Label(root, text="Количество").grid(row=4, column=0)
entry_amount = tk.Entry(root)
entry_amount.grid(row=4, column=1)

tk.Button(root, text="Добавить товар", command=add_product).grid(
    row=5, column=0, columnspan=2
)

# Интерфейс для регистрации покупки
tk.Label(root, text="Регистрация покупки").grid(row=6, column=0, columnspan=2)

tk.Label(root, text="ID товара").grid(row=7, column=0)
entry_product_id = tk.Entry(root)
entry_product_id.grid(row=7, column=1)

tk.Label(root, text="Количество").grid(row=8, column=0)
entry_purchase_amount = tk.Entry(root)
entry_purchase_amount.grid(row=8, column=1)

tk.Button(root, text="Зарегистрировать покупку", command=register_purchase).grid(
    row=9, column=0, columnspan=2
)

# Интерфейс для отчета о продажах
tk.Label(root, text="Отчет о продажах").grid(row=10, column=0, columnspan=2)

tk.Label(root, text="Дата (YYYY-MM-DD)").grid(row=11, column=0)
entry_date = tk.Entry(root)
entry_date.grid(row=11, column=1)

tk.Button(root, text="Получить отчет", command=sales_report).grid(
    row=12, column=0, columnspan=2
)

root.mainloop()
