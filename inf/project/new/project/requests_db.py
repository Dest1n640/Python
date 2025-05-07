import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect("sports_league.db")
cursor = conn.cursor()

# --- Параметры запросов ---
LEAGUE_ID = 1
TEAM_ID = 5
PLAYER_ID = 12
MIN_AVG_SALARY = 50000
DAYS_RANGE = 30

# 1. Все лиги с командами и позициями
print("\n1. Список всех лиг с командами:")
cursor.execute("""
    SELECT 
        l.name AS league_name,
        t.name AS team_name,
        t.city
    FROM Teams t
    JOIN Leagues l ON t.league_id = l.league_id
    ORDER BY l.name, t.name
""")
for row in cursor.fetchall():
    print(f"{row[0]} | {row[1]} ({row[2]})")

# 2. Лучшие бомбардиры в лиге
print(f"\n2. Топ-5 бомбардиров лиги ID={LEAGUE_ID}:")
cursor.execute(
    """
    SELECT 
        p.first_name || ' ' || p.last_name AS player,
        COUNT(g.goal_id) AS goals
    FROM Goals g
    JOIN Players p ON g.player_id = p.player_id
    JOIN Teams t ON p.team_id = t.team_id
    JOIN Seasons s ON t.league_id = ?
    WHERE g.is_own_goal = 0
    GROUP BY p.player_id
    ORDER BY goals DESC
    LIMIT 5
""",
    (LEAGUE_ID,),
)
for row in cursor.fetchall():
    print(f"{row[0]}: {row[1]} голов")

# 3. Последние трансферы

# 4. Статистика команд
print("\n4. Статистика команд:")
cursor.execute("""
    SELECT
        t.name,
        SUM(CASE WHEN (m.home_team_id = t.team_id AND m.home_team_score > m.away_team_score) 
                  OR (m.away_team_id = t.team_id AND m.away_team_score > m.home_team_score) THEN 1 ELSE 0 END) AS wins,
        SUM(CASE WHEN (m.home_team_id = t.team_id AND m.home_team_score < m.away_team_score) 
                  OR (m.away_team_id = t.team_id AND m.away_team_score < m.home_team_score) THEN 1 ELSE 0 END) AS losses,
        SUM(CASE WHEN m.home_team_score = m.away_team_score THEN 1 ELSE 0 END) AS draws
    FROM Teams t
    LEFT JOIN Matches m ON t.team_id = m.home_team_id OR t.team_id = m.away_team_id
    WHERE m.match_status = 'completed'
    GROUP BY t.team_id
    ORDER BY wins DESC
""")
for row in cursor.fetchall():
    print(f"{row[0]}: {row[1]} побед, {row[2]} поражений, {row[3]} ничьих")

# 5. Тренеры команд
print("\n5. Тренеры команд:")
cursor.execute("""
    SELECT 
        c.first_name || ' ' || c.last_name AS coach,
        t.name AS team,
        c.nationality
    FROM Coaches c
    LEFT JOIN Teams t ON c.team_id = t.team_id
    ORDER BY t.name
""")
for row in cursor.fetchall():
    print(f"{row[0]} | {row[1]} ({row[2]})")

# 6. Игроки команды
print(f"\n6. Игроки команды ID={TEAM_ID}:")
cursor.execute(
    """
    SELECT 
        p.first_name || ' ' || p.last_name AS player,
        pos.name AS position,
        p.jersey_number
    FROM Players p
    LEFT JOIN Positions pos ON p.position_id = pos.position_id
    WHERE p.team_id = ?
    ORDER BY p.jersey_number
""",
    (TEAM_ID,),
)
for row in cursor.fetchall():
    print(f"№{row[2]} | {row[0]} ({row[1]})")

# 7. Матчи между командами
print(f"\n7. Последние матчи команды ID={TEAM_ID}:")
cursor.execute(
    """
    SELECT 
        m.match_date,
        ht.name || ' ' || m.home_team_score || '-' || m.away_team_score || ' ' || at.name AS match,
        m.match_status
    FROM Matches m
    JOIN Teams ht ON m.home_team_id = ht.team_id
    JOIN Teams at ON m.away_team_id = at.team_id
    WHERE (m.home_team_id = ? OR m.away_team_id = ?)
    ORDER BY m.match_date DESC
    LIMIT 5
""",
    (TEAM_ID, TEAM_ID),
)
for row in cursor.fetchall():
    print(f"{row[0]} | {row[1]} | {row[2]}")

# 8. Контракты игроков
print("\n8. Контракты игроков:")
cursor.execute("""
    SELECT 
        p.first_name || ' ' || p.last_name AS player,
        t.name AS team,
        p.contract_end_date
    FROM Players p
    JOIN Teams t ON p.team_id = t.team_id
    ORDER BY p.contract_end_date DESC
""")
for row in cursor.fetchall():
    print(f"{row[0]} ({row[1]}): до {row[2]}")


# 9. Клубы с высокой зарплатой
# 10. Трансферная активность


# 11. Истекающие контракты
end_date = (datetime.now() + timedelta(days=DAYS_RANGE)).strftime("%Y-%m-%d")
print(f"\n11. Игроки с истекающими контрактами ({DAYS_RANGE} дней):")
cursor.execute(
    """
    SELECT 
        p.first_name || ' ' || p.last_name AS player,
        t.name AS team,
        p.contract_end_date
    FROM Players p
    JOIN Teams t ON p.team_id = t.team_id
    WHERE p.contract_end_date BETWEEN date('now') AND ?
    ORDER BY p.contract_end_date
""",
    (end_date,),
)
for row in cursor.fetchall():
    print(f"{row[0]} ({row[1]}): {row[2]}")

# 12. Лучшие защиты
print("\n12. Топ-10 защит:")
cursor.execute("""
    SELECT 
        t.name,
        SUM(CASE WHEN m.home_team_id = t.team_id THEN m.away_team_score ELSE m.home_team_score END) AS conceded
    FROM Matches m
    JOIN Teams t ON t.team_id IN (m.home_team_id, m.away_team_id)
    GROUP BY t.team_id
    ORDER BY conceded ASC
    LIMIT 10
""")
for i, row in enumerate(cursor.fetchall(), 1):
    print(f"{i}. {row[0]}: {row[1]} пропущено")

conn.close()
