# --- START OF FILE read_data.py ---
import sqlite3
import os
import csv

# Порядок загрузки таблиц важен из-за внешних ключей.
# 'Stadiums' убрана.
TABLE_LOAD_ORDER = [
    'leagues',
    'positions',
    'teams',        # Зависит от leagues
    'players',      # Зависит от teams, positions
    'coaches',      # Зависит от teams
    'seasons',      # Зависит от leagues
    'matches',      # Зависит от seasons, teams
    'trophies',     # Зависит от teams
    'goals'         # Зависит от matches, players, teams
]

def seed_from_csv_folder(seeds_dir: str, db_path: str = 'sports_league.db'):
    """Заполняет базу данных данными из CSV файлов в указанной папке."""
    if not os.path.isdir(seeds_dir):
        raise FileNotFoundError(f"Папка с CSV файлами «{seeds_dir}» не найдена")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Получаем существующие таблицы и их колонки из БД
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    existing_tables = {row[0].lower() for row in cursor.fetchall()} # Приводим к нижнему регистру для надежности
    table_columns = {}
    for table_name_db in existing_tables:
        cursor.execute(f'PRAGMA table_info("{table_name_db}")')
        # Сохраняем имена колонок в нижнем регистре
        table_columns[table_name_db] = {row[1].lower() for row in cursor.fetchall()}

    try:
        # Включаем проверку внешних ключей
        cursor.execute("PRAGMA foreign_keys = ON;")
    except sqlite3.Error as e:
         print(f"Warning: Не удалось включить foreign_keys: {e}")

    for table_name_lower in TABLE_LOAD_ORDER:
        # Ищем имя таблицы в БД без учета регистра
        actual_table_name_in_db = next((name for name in existing_tables if name == table_name_lower), None)

        if not actual_table_name_in_db:
             print(f"Предупреждение: Таблица '{table_name_lower}' не найдена в БД. Пропускаем.")
             continue

        csv_filename = f"{table_name_lower}.csv" # Имя файла совпадает с именем таблицы в нижнем регистре
        csv_path = os.path.join(seeds_dir, csv_filename)

        if not os.path.exists(csv_path):
            print(f"Предупреждение: Файл «{csv_path}» не найден. Таблица «{table_name_lower}» будет пропущена.")
            continue

        print(f"Загружаем данные из «{csv_path}» в таблицу «{actual_table_name_in_db}»...")

        try:
            with open(csv_path, mode='r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)

                csv_headers_raw = next(reader, None)
                if csv_headers_raw is None:
                    print(f"  • Файл '{csv_filename}' пустой, пропускаем.")
                    continue

                # Приводим заголовки CSV к нижнему регистру
                csv_headers = [h.lower() for h in csv_headers_raw]

                # Определяем, какие колонки из CSV существуют в таблице БД (сравниваем lower case)
                valid_csv_indices = []
                db_cols_for_table = table_columns.get(actual_table_name_in_db, set())
                actual_db_columns_to_insert = [] # Имена колонок как они есть в БД

                # Получаем реальные имена колонок из БД для SQL запроса
                cursor.execute(f'PRAGMA table_info("{actual_table_name_in_db}")')
                db_column_name_map = {row[1].lower(): row[1] for row in cursor.fetchall()}

                for idx, csv_header_lower in enumerate(csv_headers):
                    if csv_header_lower in db_cols_for_table:
                        valid_csv_indices.append(idx)
                        actual_db_columns_to_insert.append(db_column_name_map[csv_header_lower])
                    else:
                        print(f"  • Предупреждение: Колонка '{csv_headers_raw[idx]}' из CSV отсутствует в таблице '{actual_table_name_in_db}' БД. Игнорируется.")

                if not actual_db_columns_to_insert:
                    print(f"  • Ошибка: В CSV файле '{csv_filename}' нет колонок, соответствующих таблице '{actual_table_name_in_db}'. Пропускаем.")
                    continue

                placeholders = ', '.join('?' for _ in actual_db_columns_to_insert)
                # Используем реальные имена колонок БД в запросе
                columns_str = ', '.join(f'"{h}"' for h in actual_db_columns_to_insert)
                insert_sql = f'INSERT INTO "{actual_table_name_in_db}" ({columns_str}) VALUES ({placeholders})'

                rows_inserted = 0
                rows_skipped = 0
                for i, row in enumerate(reader, 1):
                    # Извлекаем только нужные данные по индексам из оригинальной строки
                    row_data_to_insert = []
                    try:
                        for idx in valid_csv_indices:
                            row_data_to_insert.append(row[idx])
                    except IndexError:
                        print(f"  • Строка {i} файла '{csv_filename}' пропущена (неверное количество столбцов?): {row}")
                        rows_skipped += 1
                        continue

                    # Заменяем пустые строки на None для корректной вставки NULL в БД
                    processed_row = [None if val == '' else val for val in row_data_to_insert]

                    try:
                        cursor.execute(insert_sql, processed_row)
                        rows_inserted += 1
                    except sqlite3.IntegrityError as e:
                         print(f"  • Ошибка целостности данных в строке {i} таблицы {actual_table_name_in_db}: {e}")
                         print(f"    Колонки БД: {actual_db_columns_to_insert}")
                         print(f"    Данные:     {processed_row}")
                         rows_skipped += 1
                    except sqlite3.Error as e:
                         print(f"  • Ошибка SQLite в строке {i} таблицы {actual_table_name_in_db}: {e}")
                         print(f"    Данные:     {processed_row}")
                         rows_skipped += 1

            print(f"  ✓ Вставлено {rows_inserted} строк в '{actual_table_name_in_db}'.")
            if rows_skipped > 0:
                print(f"  ✗ Пропущено {rows_skipped} строк.")

        except FileNotFoundError:
             print(f"  • ОШИБКА: Файл не найден «{csv_path}» во время открытия.")
        except Exception as e:
             print(f"  • ОШИБКА: Непредвиденная ошибка при обработке файла «{csv_path}»: {e}")

    try:
        conn.commit()
        print("✅ Все доступные CSV-данные успешно загружены, изменения зафиксированы в БД.")
    except sqlite3.Error as e:
        print(f"🚨 Ошибка при фиксации изменений (commit): {e}")
        print("  • Возможно, некоторые данные не были сохранены.")
        conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    # Определяем пути относительно текущего скрипта
    script_dir = os.path.dirname(__file__)
    seeds_directory = os.path.join(script_dir, 'sports_league_csv_data')
    database_file = os.path.join(script_dir, 'sports_league.db')

    if not os.path.isdir(seeds_directory):
        print(f"ОШИБКА: Папка с CSV файлами '{seeds_directory}' не найдена.")
        print("Пожалуйста, убедитесь, что папка существует и содержит CSV файлы.")
    else:
        # Проверяем, существует ли файл БД. Если нет, создаем его.
        if not os.path.exists(database_file):
             print(f"Предупреждение: Файл базы данных '{database_file}' не найден.")
             print("Создаем базу данных...")
             # Импортируем и вызываем функцию создания БД
             try:
                 from db import create_database
                 create_database(database_file)
             except ImportError:
                 print("ОШИБКА: Не удалось импортировать 'create_database' из db.py.")
             except Exception as create_e:
                 print(f"ОШИБКА при создании базы данных: {create_e}")


        # Запускаем заполнение данными
        try:
           print("-" * 20)
           print("Начинаем загрузку данных из CSV...")
           seed_from_csv_folder(seeds_directory, database_file)
        except FileNotFoundError as e:
             print(e)
        except Exception as e:
             print(f"Произошла непредвиденная ошибка во время загрузки данных: {e}")
# --- END OF FILE read_data.py ---