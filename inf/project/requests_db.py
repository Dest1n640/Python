# --- START OF FILE requests_db.py ---
import sqlite3
from typing import List, Dict, Any, Tuple, Optional
import datetime
import re

DB_PATH = 'sports_league.db'

# --- Вспомогательные функции для выполнения запросов ---
def _execute_query(db_path: str, query: str, params: Tuple = ()) -> List[Dict[str, Any]]:
    """Выполняет SELECT запрос и возвращает результат в виде списка словарей."""
    result = []
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row # Позволяет обращаться к колонкам по имени
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;") # Включаем проверку внешних ключей для сессии
        cursor.execute(query, params)
        result = [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Ошибка выполнения запроса к БД: {e}")
        print(f"Запрос: {query}")
        print(f"Параметры: {params}")
    finally:
         if conn:
             conn.close()
    return result

def _execute_update(db_path: str, query: str, params: Tuple = ()) -> int:
    """Выполняет UPDATE или DELETE запрос и возвращает количество измененных строк."""
    affected_rows = 0
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute(query, params)
        affected_rows = cursor.rowcount
        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка обновления данных в БД: {e}")
        print(f"Запрос: {query}")
        print(f"Параметры: {params}")
        if conn:
            conn.rollback() # Откатываем изменения в случае ошибки
    finally:
        if conn:
            conn.close()
    return affected_rows

def _execute_insert_get_id(db_path: str, query: str, params: Tuple = ()) -> int:
    """Выполняет INSERT запрос и возвращает ID вставленной строки."""
    last_id = -1
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute(query, params)
        last_id = cursor.lastrowid # Получаем ID последней вставленной записи
        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка вставки данных в БД: {e}")
        print(f"Запрос: {query}")
        print(f"Параметры: {params}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()
    return last_id if last_id is not None else -1

# --- Функции запросов ---

# === Запросы для таблицы Leagues ===
def get_all_leagues(db_path: str = DB_PATH) -> List[Dict[str, Any]]:
    """Получает список всех лиг (ID, имя, страна), отсортированный по стране и имени."""
    return _execute_query(db_path, "SELECT league_id, name, country FROM Leagues ORDER BY country, name")

def get_league_by_id(league_id: int, db_path: str = DB_PATH) -> Optional[Dict[str, Any]]:
    """Получает всю информацию о лиге по ее ID."""
    result = _execute_query(db_path, "SELECT * FROM Leagues WHERE league_id = ?", (league_id,))
    return result[0] if result else None

def add_league(name: str, country: str, founded_year: Optional[int] = None, description: Optional[str] = None, logo_url: Optional[str] = None, db_path: str = DB_PATH) -> int:
    """Добавляет новую лигу и возвращает ее ID."""
    query = """
    INSERT INTO Leagues (name, country, founded_year, description, logo_url)
    VALUES (?, ?, ?, ?, ?)
    """
    return _execute_insert_get_id(db_path, query, (name, country, founded_year, description, logo_url))


# === Запросы для таблицы Teams ===
def get_all_teams(db_path: str = DB_PATH) -> List[Dict[str, Any]]:
    """Получает список всех команд (ID, имя, город), отсортированный по имени."""
    return _execute_query(db_path, "SELECT team_id, name, city FROM Teams ORDER BY name")

def get_team_by_id(team_id: int, db_path: str = DB_PATH) -> Optional[Dict[str, Any]]:
    """Получает информацию о команде по ID, включая название лиги."""
    query = """
    SELECT
        t.*,
        l.name as league_name
    FROM Teams t
    LEFT JOIN Leagues l ON t.league_id = l.league_id
    WHERE t.team_id = ?
    """
    result = _execute_query(db_path, query, (team_id,))
    return result[0] if result else None

def get_teams_by_league(league_id: int, db_path: str = DB_PATH) -> List[Dict[str, Any]]:
    """Получает список всех команд в определенной лиге (ID, имя, город), отсортированный по имени."""
    return _execute_query(db_path, "SELECT team_id, name, city FROM Teams WHERE league_id = ? ORDER BY name", (league_id,))


# === Запросы для таблицы Players ===
def get_player_by_id(player_id: int, db_path: str = DB_PATH) -> Optional[Dict[str, Any]]:
    """Получает полную информацию об игроке по ID, включая название команды и позицию."""
    query = """
    SELECT
        p.*,
        t.name as team_name,
        pos.name as position_name,
        pos.abbreviation as position_abbr
    FROM Players p
    LEFT JOIN Teams t ON p.team_id = t.team_id
    LEFT JOIN Positions pos ON p.position_id = pos.position_id
    WHERE p.player_id = ?
    """
    result = _execute_query(db_path, query, (player_id,))
    return result[0] if result else None

def get_players_by_team(team_id: int, db_path: str = DB_PATH) -> List[Dict[str, Any]]:
    """Получает список игроков (ID, имя, фамилия, номер, позиция) для указанной команды."""
    query = """
    SELECT p.player_id, p.first_name, p.last_name, p.jersey_number, pos.name as position_name
    FROM Players p
    LEFT JOIN Positions pos ON p.position_id = pos.position_id
    WHERE p.team_id = ?
    ORDER BY p.jersey_number, p.last_name
    """
    return _execute_query(db_path, query, (team_id,))

def get_players_by_position(position_id: int, db_path: str = DB_PATH) -> List[Dict[str, Any]]:
    """Получает список игроков (ID, имя, фамилия, команда) для указанной позиции."""
    query = """
    SELECT p.player_id, p.first_name, p.last_name, t.name as team_name
    FROM Players p
    JOIN Teams t ON p.team_id = t.team_id
    WHERE p.position_id = ?
    ORDER BY t.name, p.last_name
    """
    return _execute_query(db_path, query, (position_id,))

def get_players_by_nationality(nationality: str, db_path: str = DB_PATH) -> List[Dict[str, Any]]:
    """Получает список игроков (ID, имя, фамилия, команда) для указанной национальности."""
    query = """
    SELECT p.player_id, p.first_name, p.last_name, t.name as team_name
    FROM Players p
    JOIN Teams t ON p.team_id = t.team_id
    WHERE p.nationality = ?
    ORDER BY t.name, p.last_name
    """
    return _execute_query(db_path, query, (nationality,))

def transfer_player(player_id: int, new_team_id: int, joining_date: Optional[str]=None, db_path: str = DB_PATH) -> int:
    """Переводит игрока в новую команду, обновляя team_id и дату присоединения."""
    if joining_date is None:
        joining_date = datetime.date.today().isoformat()
    return _execute_update(db_path, "UPDATE Players SET team_id = ?, joining_date = ? WHERE player_id = ?", (new_team_id, joining_date, player_id))

def find_players_contract_ending_soon(days_limit: int = 180, db_path: str = DB_PATH) -> List[Dict[str, Any]]:
    """Находит игроков, чей контракт заканчивается в ближайшие 'days_limit' дней."""
    limit_date = (datetime.date.today() + datetime.timedelta(days=days_limit)).isoformat()
    today_date = datetime.date.today().isoformat()
    query = """
    SELECT p.player_id, p.first_name, p.last_name, t.name as team_name, p.contract_end_date
    FROM Players p
    JOIN Teams t ON p.team_id = t.team_id
    WHERE p.contract_end_date BETWEEN ? AND ?
    ORDER BY p.contract_end_date
    """
    return _execute_query(db_path, query, (today_date, limit_date))

# === Запросы для таблицы Coaches ===
def get_coach_by_team(team_id: int, db_path: str = DB_PATH) -> Optional[Dict[str, Any]]:
    """Получает информацию о текущем тренере (последнем по дате присоединения) для команды."""
    query = """
    SELECT c.*
    FROM Coaches c
    WHERE c.team_id = ?
    ORDER BY c.joining_date DESC
    LIMIT 1
    """
    result = _execute_query(db_path, query, (team_id,))
    return result[0] if result else None

def get_all_coaches_with_teams(db_path: str = DB_PATH) -> List[Dict[str, Any]]:
    """Получает список всех тренеров с указанием их текущей команды (если есть)."""
    query = """
    SELECT c.coach_id, c.first_name, c.last_name, t.name as current_team_name, c.nationality
    FROM Coaches c
    LEFT JOIN Teams t ON c.team_id = t.team_id
    ORDER BY c.last_name, c.first_name
    """
    return _execute_query(db_path, query)

# === Запросы для таблицы Trophies ===
def get_trophies_by_team(team_id: int, db_path: str = DB_PATH) -> List[Dict[str, Any]]:
    """Получает список трофеев, выигранных командой, отсортированный по году (убывание)."""
    return _execute_query(db_path, "SELECT * FROM Trophies WHERE team_id = ? ORDER BY year DESC", (team_id,))

def get_team_with_most_trophies(db_path: str = DB_PATH) -> Optional[Dict[str, Any]]:
    """Находит команду с наибольшим количеством трофеев."""
    query = """
    SELECT t.team_id, t.name, COUNT(tr.trophy_id) as trophy_count
    FROM Teams t
    JOIN Trophies tr ON t.team_id = tr.team_id
    GROUP BY t.team_id
    ORDER BY trophy_count DESC
    LIMIT 1
    """
    result = _execute_query(db_path, query)
    return result[0] if result else None

# === Запросы для таблицы Seasons ===
def get_seasons_by_league(league_id: int, db_path: str = DB_PATH) -> List[Dict[str, Any]]:
    """Получает список сезонов для лиги, отсортированный по дате начала (убывание)."""
    return _execute_query(db_path, "SELECT * FROM Seasons WHERE league_id = ? ORDER BY start_date DESC", (league_id,))

def get_seasons_by_status(status: str, db_path: str = DB_PATH) -> List[Dict[str, Any]]:
    """Получает список сезонов с указанным статусом ('upcoming', 'ongoing', 'completed'), включая название лиги."""
    return _execute_query(db_path, "SELECT s.*, l.name as league_name FROM Seasons s JOIN Leagues l ON s.league_id = l.league_id WHERE s.status = ? ORDER BY l.name, s.start_date DESC", (status,))

# === Запросы для таблицы Matches ===
def get_matches_by_season(season_id: int, db_path: str = DB_PATH) -> List[Dict[str, Any]]:
    """Получает список матчей для сезона, включая названия команд."""
    # Запрос изменен, убрана информация о стадионе
    query = """
    SELECT
        m.match_id,
        m.match_date,
        ht.name as home_team,
        at.name as away_team,
        m.home_team_score,
        m.away_team_score,
        m.match_status
    FROM Matches m
    JOIN Teams ht ON m.home_team_id = ht.team_id
    JOIN Teams at ON m.away_team_id = at.team_id
    WHERE m.season_id = ?
    ORDER BY m.match_date
    """
    return _execute_query(db_path, query, (season_id,))

def get_matches_by_team(team_id: int, limit: int = 20, db_path: str = DB_PATH) -> List[Dict[str, Any]]:
    """Получает последние 'limit' сыгранных матчей для команды."""
    query = """
    SELECT
        m.match_id,
        m.match_date,
        ht.name as home_team,
        at.name as away_team,
        m.home_team_score,
        m.away_team_score,
        m.match_status
    FROM Matches m
    JOIN Teams ht ON m.home_team_id = ht.team_id
    JOIN Teams at ON m.away_team_id = at.team_id
    WHERE (m.home_team_id = ? OR m.away_team_id = ?)
          AND m.match_status != 'scheduled'
    ORDER BY m.match_date DESC
    LIMIT ?
    """
    return _execute_query(db_path, query, (team_id, team_id, limit))

def get_matches_in_date_range(start_date: str, end_date: str, db_path: str = DB_PATH) -> List[Dict[str, Any]]:
    """Получает список матчей, сыгранных в указанном диапазоне дат, включая название лиги."""
    query = """
    SELECT
        m.match_id,
        m.match_date,
        ht.name as home_team,
        at.name as away_team,
        m.home_team_score,
        m.away_team_score,
        m.match_status,
        l.name as league_name
    FROM Matches m
    JOIN Teams ht ON m.home_team_id = ht.team_id
    JOIN Teams at ON m.away_team_id = at.team_id
    JOIN Seasons s ON m.season_id = s.season_id
    JOIN Leagues l ON s.league_id = l.league_id
    WHERE DATE(m.match_date) BETWEEN ? AND ?
    ORDER BY m.match_date
    """
    return _execute_query(db_path, query, (start_date, end_date))

def find_matches_by_scoreline(home_score: int, away_score: int, db_path: str = DB_PATH) -> List[Dict[str, Any]]:
     """Находит завершенные матчи с указанным счетом."""
     query = """
     SELECT
         m.match_id,
         m.match_date,
         ht.name as home_team,
         at.name as away_team
     FROM Matches m
     JOIN Teams ht ON m.home_team_id = ht.team_id
     JOIN Teams at ON m.away_team_id = at.team_id
     WHERE m.home_team_score = ? AND m.away_team_score = ? AND m.match_status = 'completed'
     ORDER BY m.match_date DESC
     """
     return _execute_query(db_path, query, (home_score, away_score))

# === Запросы для таблицы Goals ===
def get_goals_by_match(match_id: int, db_path: str = DB_PATH) -> List[Dict[str, Any]]:
    """Получает информацию о голах, забитых в конкретном матче."""
    query = """
    SELECT
        g.goal_id,
        g.minute,
        p.first_name,
        p.last_name,
        t.name as team_scored_for,
        g.is_penalty,
        g.is_own_goal
    FROM Goals g
    JOIN Players p ON g.player_id = p.player_id
    JOIN Teams t ON g.team_id = t.team_id
    WHERE g.match_id = ?
    ORDER BY g.minute
    """
    return _execute_query(db_path, query, (match_id,))

# === Сложные/Агрегированные запросы ===
def get_league_top_scorers(league_id: int, limit: int = 10, db_path: str = DB_PATH) -> List[Dict[str, Any]]:
    """Получает топ 'limit' бомбардиров лиги (без учета автоголов)."""
    query = """
    SELECT
        p.player_id,
        p.first_name,
        p.last_name,
        t.name as team_name,
        COUNT(g.goal_id) as goals_count
    FROM Goals g
    JOIN Players p ON g.player_id = p.player_id
    JOIN Teams t ON g.team_id = t.team_id
    JOIN Matches m ON g.match_id = m.match_id -- Присоединяем матчи
    JOIN Seasons s ON m.season_id = s.season_id -- Присоединяем сезоны
    WHERE s.league_id = ? AND g.is_own_goal = 0 -- Фильтруем по лиге и автоголам
    GROUP BY p.player_id, p.first_name, p.last_name, t.name
    ORDER BY goals_count DESC
    LIMIT ?
    """
    # Важно: Этот запрос считает голы за ВСЕ сезоны лиги в БД.
    # Для подсчета за конкретный сезон, нужно добавить фильтр по season_id.
    # Пока оставлено так для простоты, но для реального приложения может потребоваться доработка.
    return _execute_query(db_path, query, (league_id, limit))


def get_league_standings(league_id: int, season_id: Optional[int] = None, db_path: str = DB_PATH) -> List[Dict[str, Any]]:
    """
    Рассчитывает турнирную таблицу для лиги.
    Если season_id не указан, пытается найти последний 'ongoing' или 'completed' сезон для этой лиги.
    """
    if season_id is None:
        # Запрос для поиска ID последнего активного или завершенного сезона
        find_season_query = """
        SELECT season_id
        FROM Seasons
        WHERE league_id = ? AND status IN ('ongoing', 'completed')
        ORDER BY start_date DESC
        LIMIT 1
        """
        season_res = _execute_query(db_path, find_season_query, (league_id,))
        if not season_res:
            print(f"Не найдены активные или завершенные сезоны для лиги ID={league_id}")
            return []
        season_id = season_res[0]['season_id']
        print(f"Автоматически выбран сезон ID={season_id} для таблицы лиги ID={league_id}")

    # Основной запрос для расчета таблицы, использующий Common Table Expressions (CTE)
    query = """
    WITH MatchPoints AS (
        -- Очки и статистика для домашних матчей
        SELECT
            m.home_team_id as team_id,
            1 as played,
            CASE WHEN m.home_team_score > m.away_team_score THEN 3
                 WHEN m.home_team_score = m.away_team_score THEN 1
                 ELSE 0 END as points,
            CASE WHEN m.home_team_score > m.away_team_score THEN 1 ELSE 0 END as won,
            CASE WHEN m.home_team_score = m.away_team_score THEN 1 ELSE 0 END as drawn,
            CASE WHEN m.home_team_score < m.away_team_score THEN 1 ELSE 0 END as lost,
            m.home_team_score as goals_for,
            m.away_team_score as goals_against
        FROM Matches m
        WHERE m.season_id = ? AND m.match_status = 'completed'

        UNION ALL

        -- Очки и статистика для гостевых матчей
        SELECT
            m.away_team_id as team_id,
            1 as played,
            CASE WHEN m.away_team_score > m.home_team_score THEN 3
                 WHEN m.away_team_score = m.home_team_score THEN 1
                 ELSE 0 END as points,
            CASE WHEN m.away_team_score > m.home_team_score THEN 1 ELSE 0 END as won,
            CASE WHEN m.away_team_score = m.home_team_score THEN 1 ELSE 0 END as drawn,
            CASE WHEN m.away_team_score < m.home_team_score THEN 1 ELSE 0 END as lost,
            m.away_team_score as goals_for,
            m.home_team_score as goals_against
        FROM Matches m
        WHERE m.season_id = ? AND m.match_status = 'completed'
    ),
    TeamStats AS (
        -- Агрегация статистики по командам
        SELECT
            team_id,
            COUNT(team_id) as played,
            SUM(points) as points,
            SUM(won) as won,
            SUM(drawn) as drawn,
            SUM(lost) as lost,
            SUM(goals_for) as goals_for,
            SUM(goals_against) as goals_against,
            SUM(goals_for) - SUM(goals_against) as goal_difference
        FROM MatchPoints
        GROUP BY team_id
    )
    -- Финальный SELECT для формирования таблицы
    SELECT
        t.name as team_name,
        COALESCE(ts.played, 0) as played,
        COALESCE(ts.won, 0) as won,
        COALESCE(ts.drawn, 0) as drawn,
        COALESCE(ts.lost, 0) as lost,
        COALESCE(ts.goals_for, 0) as goals_for,
        COALESCE(ts.goals_against, 0) as goals_against,
        COALESCE(ts.goal_difference, 0) as goal_difference,
        COALESCE(ts.points, 0) as points
    FROM Teams t
    LEFT JOIN TeamStats ts ON t.team_id = ts.team_id
    WHERE t.league_id = ?  -- Выбираем команды только из нужной лиги
    ORDER BY points DESC, goal_difference DESC, goals_for DESC, team_name ASC -- Правила сортировки
    """
    return _execute_query(db_path, query, (season_id, season_id, league_id))

def get_league_average_attendance(league_id: int, season_id: Optional[int] = None, db_path: str = DB_PATH) -> Optional[float]:
    """Рассчитывает среднюю посещаемость для лиги в указанном сезоне (или последнем)."""
    if season_id is None:
         find_season_query = "SELECT season_id FROM Seasons WHERE league_id = ? AND status IN ('ongoing', 'completed') ORDER BY start_date DESC LIMIT 1"
         season_res = _execute_query(db_path, find_season_query, (league_id,))
         if not season_res: return None
         season_id = season_res[0]['season_id']

    query = """
    SELECT AVG(attendance) as average_attendance
    FROM Matches
    WHERE season_id = ? AND match_status = 'completed' AND attendance IS NOT NULL AND attendance > 0
    """
    result = _execute_query(db_path, query, (season_id,))
    # Проверяем, что результат не пустой и содержит не None значение
    return result[0]['average_attendance'] if result and result[0]['average_attendance'] is not None else None

def get_player_goal_stats(player_id: int, db_path: str = DB_PATH) -> Dict[str, Any]:
    """Получает статистику голов (всего, пенальти, автоголы) для игрока."""
    query = """
    SELECT
        COUNT(goal_id) as total_goals,
        SUM(CASE WHEN is_penalty = 1 AND is_own_goal = 0 THEN 1 ELSE 0 END) as penalty_goals,
        SUM(CASE WHEN is_own_goal = 1 THEN 1 ELSE 0 END) as own_goals
    FROM Goals
    WHERE player_id = ?
    """
    result = _execute_query(db_path, query, (player_id,))
    if result and result[0]['total_goals'] is not None:
        # Используем .get() с default=0 для надежности, если SUM вернет NULL
        stats = {
            'total_goals': result[0].get('total_goals', 0) or 0,
            'penalty_goals': result[0].get('penalty_goals', 0) or 0,
            'own_goals': result[0].get('own_goals', 0) or 0
        }
        return stats
    else:
        # Возвращаем словарь с нулями, если игрок не найден или не забивал
        return {'total_goals': 0, 'penalty_goals': 0, 'own_goals': 0}


# === Функции Поиска ===

def search_all(search_term: str, limit_per_type: int = 10, db_path: str = DB_PATH) -> List[Dict[str, Any]]:
    """
    Ищет сущности (лиги, команды, игроки) по текстовому запросу.
    Возвращает список словарей с типом, ID, отображаемым именем и деталями.
    """
    results = []
    if not search_term or not search_term.strip():
        return results # Возвращаем пустой список, если строка поиска пустая

    search_term_like = f"%{search_term.lower().strip()}%" # Готовим строку для LIKE

    # 1. Поиск Лиг
    league_query = """
        SELECT league_id, name, country FROM Leagues
        WHERE LOWER(name) LIKE ? OR LOWER(country) LIKE ?
        LIMIT ?
        """
    leagues = _execute_query(db_path, league_query, (search_term_like, search_term_like, limit_per_type))
    for league in leagues:
        results.append({
            'id': league['league_id'],
            'type': 'league',
            'display_name': f"{league['name']} ({league['country']})",
            'details': league
        })

    # 2. Поиск Команд
    team_query = """
        SELECT t.team_id, t.name, t.city, l.name as league_name
        FROM Teams t LEFT JOIN Leagues l ON t.league_id = l.league_id
        WHERE LOWER(t.name) LIKE ? OR LOWER(t.city) LIKE ?
        LIMIT ?
    """
    teams = _execute_query(db_path, team_query, (search_term_like, search_term_like, limit_per_type))
    for team in teams:
        # Формируем контекст (Город - Лига)
        context_parts = [part for part in [team.get('city'), team.get('league_name')] if part]
        context = " - ".join(context_parts)
        results.append({
            'id': team['team_id'],
            'type': 'team',
            'display_name': f"{team['name']} ({context})" if context else team['name'],
            'details': team
        })

    # 3. Поиск Игроков (Имя, Фамилия, Имя+Фамилия)
    player_query = """
        SELECT p.player_id, p.first_name, p.last_name, t.name as team_name
        FROM Players p LEFT JOIN Teams t ON p.team_id = t.team_id
        WHERE LOWER(p.first_name) LIKE ?
           OR LOWER(p.last_name) LIKE ?
           OR LOWER(p.first_name || ' ' || p.last_name) LIKE ?
        LIMIT ?
    """
    players = _execute_query(db_path, player_query, (search_term_like, search_term_like, search_term_like, limit_per_type))
    for player in players:
        team_context = player.get('team_name', 'Без команды')
        results.append({
            'id': player['player_id'],
            'type': 'player',
            'display_name': f"{player['first_name']} {player['last_name']} ({team_context})",
            'details': player
        })

    # Сортировка результатов: сначала лиги, потом команды, потом игроки, затем по имени
    results.sort(key=lambda x: (
        0 if x['type'] == 'league' else 1 if x['type'] == 'team' else 2,
        x['display_name'].lower()
    ))

    return results
# --- END OF FILE requests_db.py ---