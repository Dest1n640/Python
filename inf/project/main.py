import sqlite3
import os


def read_txt_file(filename):
    """Чтение данных из текстового файла в список кортежей"""
    with open(filename, "r", encoding="utf-8") as file:
        return [tuple(line.strip().split(",")) for line in file if line.strip()]


conn = sqlite3.connect("football_league.db")
cursor = conn.cursor()

# Словарь соответствия файлов и таблиц с полями
tables = {
    "League": ("seeds/leagues.txt", ["id", "name"]),
    "Club": ("seeds/clubs.txt", ["id", "league_id", "name", "table_place"]),
    "Club_stat": (
        "seeds/clubs_statistics.txt",
        ["id", "club_id", "win", "lose", "draw"],
    ),
    "Coach": ("seeds/coaches.txt", ["id", "club_id", "name", "surname", "salary"]),
    "Coach_stat": (
        "seeds/coache_statistics.txt",
        ["id", "coach_id", "win", "lose", "draw"],
    ),
    "Player": ("seeds/playes.txt", ["id", "club_id", "name", "surname", "salary"]),
    "Player_stat": (
        "seeds/player_statistics.txt",
        ["id", "player_id", "goals", "assists"],
    ),
    "Match": ("seeds/matches.txt", ["id", "club_id", "rival_id", "date", "score"]),
    "Transfer": (
        "seeds/transfers.txt",
        ["id", "player_id", "club_from_id", "club_to_id", "date", "price"],
    ),
    "Contract": (
        "seeds/contracts.txt",
        ["id", "player_id", "club_id", "date_start", "date_end", "salary"],
    ),
}

for table, (file, columns) in tables.items():
    try:
        print(f"Загрузка данных из {file} в таблицу {table}...")
        data = read_txt_file(file)
        placeholders = ",".join(["?"] * len(columns))
        query = f"INSERT OR IGNORE INTO {table} ({','.join(columns)}) VALUES ({placeholders})"

        for row in data:
            try:
                # Преобразование числовых полей
                converted_row = []
                for item, column in zip(row, columns):
                    if column in [
                        "id",
                        "club_id",
                        "league_id",
                        "table_place",
                        "win",
                        "lose",
                        "draw",
                        "salary",
                        "goals",
                        "assists",
                        "player_id",
                        "coach_id",
                        "rival_id",
                        "club_from_id",
                        "club_to_id",
                        "price",
                    ]:
                        converted_row.append(int(item))
                    else:
                        converted_row.append(item.strip())

                cursor.execute(query, converted_row)
            except Exception as e:
                print(f"⚠️ Ошибка при обработке строки в {table}: {row}")
                print(f"  Детали: {str(e)}")
    except FileNotFoundError as e:
        print(f"❌ Файл не найден: {file}")
    except Exception as e:
        print(f"❌ Ошибка при обработке таблицы {table}: {str(e)}")

conn.commit()
conn.close()
print("✅ Импорт данных завершен")
