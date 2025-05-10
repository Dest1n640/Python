import sys
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, 
                            QHBoxLayout, QTableView, QLabel, QPushButton, QComboBox, 
                            QHeaderView, QMessageBox, QGroupBox, QFormLayout, QLineEdit)
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery, QSqlQueryModel
from PyQt5.QtCore import Qt

class SportsLeagueApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sports League Database")
        self.setGeometry(100, 100, 1200, 800)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs)
        
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("sports_league.db")
        if not self.db.open():
            QMessageBox.critical(self, "Database Error", "Could not open database.")
            sys.exit(1)
            
        self.create_leagues_tab()
        self.create_teams_tab()
        self.create_players_tab()
        self.create_coaches_tab()
        self.create_matches_tab()
        self.create_goals_tab()
        self.create_queries_tab()

    # --- Таблицы ---
    def create_table_tab(self, title, table_name, headers):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        label = QLabel(title)
        label.setStyleSheet("font-size: 16pt; font-weight: bold;")
        layout.addWidget(label)
        model = QSqlTableModel()
        model.setTable(table_name)
        model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        model.select()
        for i, header in enumerate(headers):
            model.setHeaderData(i, Qt.Horizontal, header)
        table_view = QTableView()
        table_view.setModel(model)
        table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(table_view)
        self.tabs.addTab(tab, title)
    def create_leagues_tab(self):
        headers = ["ID", "Name", "Country", "Founded Year"]
        self.create_table_tab("Leagues", "Leagues", headers)
    def create_teams_tab(self):
        headers = ["ID", "League ID", "Name", "City", "Founded Year"]
        self.create_table_tab("Teams", "Teams", headers)
    def create_players_tab(self):
        headers = ["ID", "Team ID", "First Name", "Last Name", "Birth Date", 
                  "Nationality", "Position ID", "Jersey", "Height", "Weight", 
                  "Joined", "Contract End", "Photo"]
        self.create_table_tab("Players", "Players", headers)
    def create_coaches_tab(self):
        headers = ["ID", "Team ID", "First Name", "Last Name", "Birth Date",
                  "Nationality", "Style", "Joined", "Contract End", "Photo"]
        self.create_table_tab("Coaches", "Coaches", headers)
    def create_matches_tab(self):
        headers = ["ID", "Season ID", "Home Team", "Away Team", "Date", 
                  "Home Score", "Away Score", "Status", "Attendance", "Referee"]
        self.create_table_tab("Matches", "Matches", headers)
    def create_goals_tab(self):
        headers = ["ID", "Match ID", "Player ID", "Team ID", "Minute", 
                  "Penalty", "Own Goal"]
        self.create_table_tab("Goals", "Goals", headers)

    # --- Запросы ---
    def create_queries_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        label = QLabel("Запросы")
        label.setStyleSheet("font-size: 16pt; font-weight: bold;")
        layout.addWidget(label)
        params_group = QGroupBox("Параметры")
        params_layout = QFormLayout()
        self.query_combo = QComboBox()
        self.query_combo.addItems([
            "1. Все лиги с командами",
            "2. Топ-5 бомбардиров лиги",
            "3. Статистика команд",
            "4. Тренеры команд",
            "5. Игроки команды",
            "6. Последние матчи команды",
            "7. Контракты игроков",
            "8. Самые результативные матчи",
            "9. Топ команд по трофеям",
            "10. Игроки с истекающими контрактами",
            "11. Топ-10 лучших защит",
            "12. Игроки без клуба"
        ])
        self.league_input = QLineEdit()
        self.league_input.setPlaceholderText("ID лиги (по умолчанию 1)")
        self.team_input = QLineEdit()
        self.team_input.setPlaceholderText("ID команды (по умолчанию 1)")
        self.days_input = QLineEdit()
        self.days_input.setPlaceholderText("Дней до окончания контракта (по умолчанию 30)")
        params_layout.addRow("Запрос:", self.query_combo)
        params_layout.addRow("ID лиги:", self.league_input)
        params_layout.addRow("ID команды:", self.team_input)
        params_layout.addRow("Диапазон дней:", self.days_input)
        params_group.setLayout(params_layout)
        execute_btn = QPushButton("Выполнить")
        execute_btn.clicked.connect(self.execute_query)
        self.result_view = QTableView()
        layout.addWidget(params_group)
        layout.addWidget(execute_btn)
        layout.addWidget(self.result_view)
        self.tabs.addTab(tab, "Запросы")

    def execute_query(self):
        idx = self.query_combo.currentIndex()
        league_id = self.league_input.text() or "1"
        team_id = self.team_input.text() or "1"
        days_range = self.days_input.text() or "30"
        model = QSqlQueryModel()
        # 1. Все лиги с командами
        if idx == 0:
            sql = """
                SELECT l.name AS "Лига", t.name AS "Команда", t.city AS "Город"
                FROM Teams t
                JOIN Leagues l ON t.league_id = l.league_id
                ORDER BY l.name, t.name
            """
            model.setQuery(sql, self.db)
        # 2. Топ-5 бомбардиров лиги
        elif idx == 1:
            sql = f"""
                SELECT p.first_name || ' ' || p.last_name AS "Игрок", COUNT(g.goal_id) AS "Голов"
                FROM Goals g
                JOIN Players p ON g.player_id = p.player_id
                JOIN Teams t ON p.team_id = t.team_id
                WHERE t.league_id = {league_id} AND g.is_own_goal = 0
                GROUP BY p.player_id
                ORDER BY "Голов" DESC
                LIMIT 5
            """
            model.setQuery(sql, self.db)
        # 3. Статистика команд
        elif idx == 2:
            sql = """
                SELECT t.name AS "Команда",
                    SUM(CASE WHEN (m.home_team_id = t.team_id AND m.home_team_score > m.away_team_score)
                              OR (m.away_team_id = t.team_id AND m.away_team_score > m.home_team_score) THEN 1 ELSE 0 END) AS "Побед",
                    SUM(CASE WHEN (m.home_team_id = t.team_id AND m.home_team_score < m.away_team_score)
                              OR (m.away_team_id = t.team_id AND m.away_team_score < m.home_team_score) THEN 1 ELSE 0 END) AS "Поражений",
                    SUM(CASE WHEN m.home_team_score = m.away_team_score THEN 1 ELSE 0 END) AS "Ничьих"
                FROM Teams t
                LEFT JOIN Matches m ON t.team_id = m.home_team_id OR t.team_id = m.away_team_id
                WHERE m.match_status = 'completed'
                GROUP BY t.team_id
                ORDER BY "Побед" DESC
            """
            model.setQuery(sql, self.db)
        # 4. Тренеры команд
        elif idx == 3:
            sql = """
                SELECT c.first_name || ' ' || c.last_name AS "Тренер", t.name AS "Команда", c.nationality AS "Национальность"
                FROM Coaches c
                LEFT JOIN Teams t ON c.team_id = t.team_id
                ORDER BY t.name
            """
            model.setQuery(sql, self.db)
        # 5. Игроки команды
        elif idx == 4:
            sql = f"""
                SELECT p.first_name || ' ' || p.last_name AS "Игрок", p.position_id AS "Позиция", p.jersey_number AS "Номер"
                FROM Players p
                WHERE p.team_id = {team_id}
                ORDER BY p.jersey_number
            """
            model.setQuery(sql, self.db)
        # 6. Последние матчи команды
        elif idx == 5:
            sql = f"""
                SELECT m.match_date AS "Дата",
                       ht.name || ' ' || m.home_team_score || '-' || m.away_team_score || ' ' || at.name AS "Матч",
                       m.match_status AS "Статус"
                FROM Matches m
                JOIN Teams ht ON m.home_team_id = ht.team_id
                JOIN Teams at ON m.away_team_id = at.team_id
                WHERE m.home_team_id = {team_id} OR m.away_team_id = {team_id}
                ORDER BY m.match_date DESC
                LIMIT 5
            """
            model.setQuery(sql, self.db)
        # 7. Контракты игроков
        elif idx == 6:
            sql = """
                SELECT p.first_name || ' ' || p.last_name AS "Игрок", t.name AS "Команда", p.contract_end_date AS "Окончание контракта"
                FROM Players p
                JOIN Teams t ON p.team_id = t.team_id
                ORDER BY p.contract_end_date DESC
            """
            model.setQuery(sql, self.db)
        # 8. Самые результативные матчи
        elif idx == 7:
            sql = """
                SELECT m.match_date AS "Дата",
                       ht.name || ' - ' || at.name AS "Матч",
                       m.home_team_score || ':' || m.away_team_score AS "Счет",
                       (m.home_team_score + m.away_team_score) AS "Всего голов"
                FROM Matches m
                JOIN Teams ht ON m.home_team_id = ht.team_id
                JOIN Teams at ON m.away_team_id = at.team_id
                ORDER BY "Всего голов" DESC
                LIMIT 10
            """
            model.setQuery(sql, self.db)
        # 9. Топ команд по трофеям
        elif idx == 8:
            sql = """
                SELECT t.name AS "Команда", COUNT(tr.trophy_id) as "Трофеев"
                FROM Teams t
                LEFT JOIN Trophies tr ON t.team_id = tr.team_id
                GROUP BY t.team_id
                ORDER BY "Трофеев" DESC
                LIMIT 10
            """
            model.setQuery(sql, self.db)
        # 10. Игроки с истекающими контрактами
        elif idx == 9:
            end_date = (datetime.now() + timedelta(days=int(days_range))).strftime("%Y-%m-%d")
            sql = f"""
                SELECT p.first_name || ' ' || p.last_name AS "Игрок", t.name AS "Команда", p.contract_end_date AS "Окончание контракта"
                FROM Players p
                JOIN Teams t ON p.team_id = t.team_id
                WHERE p.contract_end_date BETWEEN date('now') AND '{end_date}'
                ORDER BY p.contract_end_date
            """
            model.setQuery(sql, self.db)
        # 11. Топ-10 лучших защит (по наименьшему количеству пропущенных голов)
        elif idx == 10:
            sql = """
                SELECT t.name AS "Команда",
                       SUM(CASE WHEN m.home_team_id = t.team_id THEN m.away_team_score ELSE m.home_team_score END) AS "Пропущено"
                FROM Matches m
                JOIN Teams t ON t.team_id IN (m.home_team_id, m.away_team_id)
                GROUP BY t.team_id
                ORDER BY "Пропущено" ASC
                LIMIT 10
            """
            model.setQuery(sql, self.db)
        # 12. Игроки без клуба
        elif idx == 11:
            sql = """
                SELECT first_name || ' ' || last_name AS "Игрок", contract_end_date AS "Окончание контракта"
                FROM Players
                WHERE team_id IS NULL AND contract_end_date > date('now')
                ORDER BY contract_end_date
            """
            model.setQuery(sql, self.db)
        else:
            QMessageBox.warning(self, "Ошибка", "Неизвестный запрос")
            return
        self.result_view.setModel(model)
        self.result_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SportsLeagueApp()
    window.show()
    sys.exit(app.exec_())

