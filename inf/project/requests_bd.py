import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect("sports_league.db")
cursor = conn.cursor()

# --- Параметры запросов ---
LEAGUE_ID = 1
TEAM_ID = 5
PLAYER_ID = 12
DAYS_RANGE = 30

# 1. Список всех лиг
print("\n1. Все лиги:")
cursor.execute("""
    SELECT name, country, founded_year 
    FROM Leagues 
    ORDER BY country, name
""")
for row in cursor.fetchall():
    print(f"{row[0]} ({row[1]}) - Основана в {row[2] or 'неизвестно'}")

# 2. Команды лиги
print(f"\n2. Команды лиги ID={LEAGUE_ID}:")
cursor.execute(
    """
    SELECT team_id, name, city 
    FROM Teams 
    WHERE league_id = ? 
    ORDER BY name
""",
    (LEAGUE_ID,),
)
for row in cursor.fetchall():
    print(f"{row[1]} ({row[2]})")

# 3. Последние матчи команды
print(f"\n3. Последние 5 матчей команды ID={TEAM_ID}:")
cursor.execute(
    """
    SELECT m.match_date, 
           ht.name as home_team,
           at.name as away_team,
           m.home_team_score || '-' || m.away_team_score as score
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
    print(f"{row[0]} | {row[1]} vs {row[2]} | Счет: {row[3]}")

# 4. Топ бомбардиры лиги
print(f"\n4. Топ-5 бомбардиров лиги ID={LEAGUE_ID}:")
cursor.execute(
    """
    SELECT p.first_name || ' ' || p.last_name as player_name,
           t.name as team_name,
           COUNT(g.goal_id) as goals
    FROM Goals g
    JOIN Players p ON g.player_id = p.player_id
    JOIN Teams t ON g.team_id = t.team_id
    JOIN Matches m ON g.match_id = m.match_id
    JOIN Seasons s ON m.season_id = s.season_id
    WHERE s.league_id = ? AND g.is_own_goal = 0
    GROUP BY p.player_id
    ORDER BY goals DESC
    LIMIT 5
""",
    (LEAGUE_ID,),
)
for row in cursor.fetchall():
    print(f"{row[0]} ({row[1]}): {row[2]} голов")

# 5. Игроки команды
print(f"\n5. Игроки команды ID={TEAM_ID}:")
cursor.execute(
    """
    SELECT p.first_name, p.last_name, pos.name as position
    FROM Players p
    LEFT JOIN Positions pos ON p.position_id = pos.position_id
    WHERE p.team_id = ?
    ORDER BY p.jersey_number
""",
    (TEAM_ID,),
)
for row in cursor.fetchall():
    print(f"{row[0]} {row[1]} - {row[2] or 'без позиции'}")

# 6. Турнирная таблица
print(f"\n6. Текущая турнирная таблица лиги ID={LEAGUE_ID}:")
cursor.execute(
    """
    SELECT t.name as team,
           stats.points,
           stats.goal_difference,
           stats.won,
           stats.drawn,
           stats.lost
    FROM Teams t
    JOIN (
        SELECT team_id, 
               SUM(points) as points,
               SUM(goals_for) - SUM(goals_against) as goal_difference,
               SUM(won) as won,
               SUM(drawn) as drawn,
               SUM(lost) as lost
        FROM (
            SELECT home_team_id as team_id,
                   CASE WHEN home_team_score > away_team_score THEN 3
                        WHEN home_team_score = away_team_score THEN 1 
                        ELSE 0 END as points,
                   home_team_score as goals_for,
                   away_team_score as goals_against,
                   CASE WHEN home_team_score > away_team_score THEN 1 ELSE 0 END as won,
                   CASE WHEN home_team_score = away_team_score THEN 1 ELSE 0 END as drawn,
                   CASE WHEN home_team_score < away_team_score THEN 1 ELSE 0 END as lost
            FROM Matches
            WHERE match_status = 'completed'
            UNION ALL
            SELECT away_team_id as team_id,
                   CASE WHEN away_team_score > home_team_score THEN 3
                        WHEN away_team_score = home_team_score THEN 1 
                        ELSE 0 END as points,
                   away_team_score as goals_for,
                   home_team_score as goals_against,
                   CASE WHEN away_team_score > home_team_score THEN 1 ELSE 0 END as won,
                   CASE WHEN away_team_score = home_team_score THEN 1 ELSE 0 END as drawn,
                   CASE WHEN away_team_score < home_team_score THEN 1 ELSE 0 END as lost
            FROM Matches
            WHERE match_status = 'completed'
        )
        GROUP BY team_id
    ) stats ON t.team_id = stats.team_id
    WHERE t.league_id = ?
    ORDER BY stats.points DESC, stats.goal_difference DESC
""",
    (LEAGUE_ID,),
)
for i, row in enumerate(cursor.fetchall(), 1):
    print(f"{i}. {row[0]}: {row[1]} очков (+{row[2]}), {row[3]}-{row[4]}-{row[5]}")

# 7. Трансферная история игрока
print(f"\n7. Трансферная история игрока ID={PLAYER_ID}:")
cursor.execute(
    """
    SELECT t.transfer_date, 
           c_from.name as from_club,
           c_to.name as to_club,
           t.transfer_fee
    FROM Transfers t
    JOIN Teams c_from ON t.from_team_id = c_from.team_id
    JOIN Teams c_to ON t.to_team_id = c_to.team_id
    WHERE t.player_id = ?
    ORDER BY t.transfer_date DESC
""",
    (PLAYER_ID,),
)
for row in cursor.fetchall():
    fee = f"Сумма: {row[3]}" if row[3] else "Свободный агент"
    print(f"{row[0]} | {row[1]} → {row[2]} | {fee}")

# 8. Игроки с истекающими контрактами
end_date = (datetime.now() + timedelta(days=DAYS_RANGE)).strftime("%Y-%m-%d")
print(f"\n8. Игроки с истекающими контрактами в ближайшие {DAYS_RANGE} дней:")
cursor.execute(
    """
    SELECT p.first_name || ' ' || p.last_name as player_name,
           t.name as team_name,
           p.contract_end_date
    FROM Players p
    JOIN Teams t ON p.team_id = t.team_id
    WHERE p.contract_end_date BETWEEN date('now') AND ?
    ORDER BY p.contract_end_date
""",
    (end_date,),
)
for row in cursor.fetchall():
    print(f"{row[0]} ({row[1]}): до {row[2]}")

# 9. Лучшие защитные команды
print("\n9. Топ-10 команд с наименьшим количеством пропущенных голов:")
cursor.execute("""
    SELECT t.name, SUM(m.goals_against) as goals_against
    FROM (
        SELECT home_team_id as team_id, away_team_score as goals_against
        FROM Matches
        UNION ALL
        SELECT away_team_id as team_id, home_team_score as goals_against
        FROM Matches
    ) m
    JOIN Teams t ON m.team_id = t.team_id
    GROUP BY t.team_id
    ORDER BY goals_against ASC
    LIMIT 10
""")
for i, row in enumerate(cursor.fetchall(), 1):
    print(f"{i}. {row[0]}: {row[1]} голов")

conn.close()
