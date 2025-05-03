import sqlite3
from datetime import datetime, timedelta


conn = sqlite3.connect("football_league.db")
cursor = conn.cursor()

# --- Настройки для параметрических запросов ---
club_id = 1  # Для запроса 6
club_id_1 = 1  # Для запроса 7
club_id_2 = 2  # Для запроса 7
min_avg_salary = 50000  # Для запроса 9

# 1. Все клубы с лигой и местом
print("\n1. Список всех клубов с их лигой и текущим местом:")
query1 = """
SELECT Club.name AS club_name, League.name AS league_name, Club.table_place
FROM Club
JOIN League ON Club.league_id = League.id
ORDER BY League.name, Club.table_place;
"""
cursor.execute(query1)
for row in cursor.fetchall():
    print(row)

# 2. Лучшие бомбардиры в каждой лиге
print("\n2. Лучшие бомбардиры (игроки с наибольшим количеством голов) в каждой лиге:")
query2 = """
SELECT League.name AS league_name, Player.name, Player.surname, Player_stat.goals
FROM Player_stat
JOIN Player ON Player_stat.player_id = Player.id
JOIN Club ON Player.club_id = Club.id
JOIN League ON Club.league_id = League.id
WHERE Player_stat.goals = (
    SELECT MAX(Player_stat.goals)
    FROM Player_stat
    JOIN Player ON Player_stat.player_id = Player.id
    JOIN Club ON Player.club_id = Club.id
    WHERE Club.league_id = League.id
)
ORDER BY League.name;
"""
cursor.execute(query2)
for row in cursor.fetchall():
    print(row)

# 3. Последние 5 трансферов
print("\n3. Последние 5 трансферов с деталями игрока, клубов и суммы:")
query3 = """
SELECT Player.name, Player.surname, Club_from.name AS club_from, Club_to.name AS club_to, Transfer.price, Transfer.date
FROM Transfer
JOIN Player ON Transfer.player_id = Player.id
JOIN Club AS Club_from ON Transfer.club_from_id = Club_from.id
JOIN Club AS Club_to ON Transfer.club_to_id = Club_to.id
ORDER BY Transfer.date DESC
LIMIT 5;
"""
cursor.execute(query3)
for row in cursor.fetchall():
    print(row)

# 4. Статистика клуба
print("\n4. Статистика клуба: количество побед, поражений и ничьих:")
query4 = """
SELECT Club.name, Club_stat.win, Club_stat.lose, Club_stat.draw
FROM Club_stat
JOIN Club ON Club_stat.club_id = Club.id
ORDER BY Club.name;
"""
cursor.execute(query4)
for row in cursor.fetchall():
    print(row)

# 5. Тренеры клубов с их статистикой
print("\n5. Тренеры клубов с их статистикой побед, поражений и ничьих:")
query5 = """
SELECT Coach.name, Coach.surname, Club.name AS club_name, Coach_stat.win, Coach_stat.lose, Coach_stat.draw
FROM Coach_stat
JOIN Coach ON Coach_stat.coach_id = Coach.id
JOIN Club ON Coach.club_id = Club.id
ORDER BY Club.name, Coach.surname;
"""
cursor.execute(query5)
for row in cursor.fetchall():
    print(row)

# 6. Игроки определенного клуба с их статистикой
print(f"\n6. Список игроков клуба с id={club_id} с их статистикой голов и ассистов:")
query6 = """
SELECT Player.name, Player.surname, Player_stat.goals, Player_stat.assists
FROM Player
JOIN Player_stat ON Player.id = Player_stat.player_id
WHERE Player.club_id = ?
ORDER BY Player.surname, Player.name;
"""
cursor.execute(query6, (club_id,))
for row in cursor.fetchall():
    print(row)

# 7. Все матчи между двумя выбранными клубами
print(f"\n7. Все матчи между клубами с id={club_id_1} и id={club_id_2}:")
query7 = """
SELECT Match.date, Club1.name AS club, Club2.name AS rival, Match.score
FROM Match
JOIN Club AS Club1 ON Match.club_id = Club1.id
JOIN Club AS Club2 ON Match.rival_id = Club2.id
WHERE (Match.club_id = ? AND Match.rival_id = ?) OR (Match.club_id = ? AND Match.rival_id = ?)
ORDER BY Match.date DESC;
"""
cursor.execute(query7, (club_id_1, club_id_2, club_id_2, club_id_1))
for row in cursor.fetchall():
    print(row)

# 8. Информация о контрактах игроков
print("\n8. Информация о контрактах игроков, сроках и зарплате:")
query8 = """
SELECT Player.name, Player.surname, Club.name AS club_name, Contract.date_start, Contract.date_end, Contract.salary
FROM Contract
JOIN Player ON Contract.player_id = Player.id
JOIN Club ON Contract.club_id = Club.id
ORDER BY Player.surname, Player.name;
"""
cursor.execute(query8)
for row in cursor.fetchall():
    print(row)

# 9. Клубы с высокой средней зарплатой игроков
print(f"\n9. Клубы, у которых средняя зарплата игроков выше {min_avg_salary}:")
query9 = """
SELECT Club.name, AVG(Player.salary) AS avg_salary
FROM Player
JOIN Club ON Player.club_id = Club.id
GROUP BY Club.id
HAVING avg_salary > ?
ORDER BY avg_salary DESC;
"""
cursor.execute(query9, (min_avg_salary,))
for row in cursor.fetchall():
    print(row)

# 10. Клубы с наибольшим количеством покупок на трансферном рынке
print("\n10. Клубы, которые совершили больше всего покупок на трансферном рынке:")
query10 = """
SELECT Club.name, COUNT(Transfer.id) AS transfers_count
FROM Transfer
JOIN Club ON Transfer.club_to_id = Club.id
GROUP BY Club.id
ORDER BY transfers_count DESC
LIMIT 10;
"""
cursor.execute(query10)
for row in cursor.fetchall():
    print(row)

# 11. Поиск игроков с истекающими контрактами
# Текущая дата и дата через 30 дней
today = datetime.today().strftime("%Y-%m-%d")
in_30_days = (datetime.today() + timedelta(days=30)).strftime("%Y-%m-%d")

print("\n11. Игроки с истекающими контрактами в ближайшие 30 дней:")
query11 = """
SELECT Player.name, Player.surname, Club.name AS club_name, Contract.date_end
FROM Contract
JOIN Player ON Contract.player_id = Player.id
JOIN Club ON Contract.club_id = Club.id
WHERE Contract.date_end BETWEEN ? AND ?
ORDER BY Contract.date_end;
"""
cursor.execute(query11, (today, in_30_days))
for row in cursor.fetchall():
    print(row)

# 12. Анализ эффективности защиты
print("\n12. Топ-10 клубов с наименьшим количеством поражений (эффективность защиты):")
query12 = """
SELECT Club.name, Club_stat.lose
FROM Club_stat
JOIN Club ON Club_stat.club_id = Club.id
ORDER BY Club_stat.lose ASC
LIMIT 10;
"""

cursor.execute(query12)
for row in cursor.fetchall():
    print(row)

conn.close()
