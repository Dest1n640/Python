import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableView,
    QTabWidget,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QComboBox,
)
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery, QSqlQueryModel


class SportsLeagueDB(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Спортивная База Данных")
        self.setGeometry(100, 100, 800, 600)

        # Подключение к базе данных
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("sports_league.db")

        if not self.db.open():
            print("Ошибка подключения к базе данных!")
            return

        # Создание интерфейса
        self.setup_ui()

    def setup_ui(self):
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Создание вкладок
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # Добавление вкладок с таблицами
        self.add_table_tabs()

        # Добавление вкладки с запросами
        self.add_query_tab()

    def add_table_tabs(self):
        """Добавляет вкладки для основных таблиц базы данных"""
        tables = {
            "Лиги": "Leagues",
            "Команды": "Teams",
            "Игроки": "Players",
            "Тренеры": "Coaches",
            "Матчи": "Matches",
        }

        for tab_name, table_name in tables.items():
            tab = QWidget()
            layout = QVBoxLayout(tab)

            # Таблица для отображения данных
            table_view = QTableView()
            table_view.setAlternatingRowColors(True)
            table_view.setSortingEnabled(True)

            # Модель для данных
            model = QSqlTableModel()
            model.setTable(table_name)
            model.setEditStrategy(QSqlTableModel.OnManualSubmit)
            model.select()

            table_view.setModel(model)
            layout.addWidget(table_view)

            # Кнопки для управления
            button_layout = QHBoxLayout()
            refresh_btn = QPushButton("Обновить")
            refresh_btn.clicked.connect(model.select)

            save_btn = QPushButton("Сохранить")
            save_btn.clicked.connect(model.submitAll)

            cancel_btn = QPushButton("Отменить")
            cancel_btn.clicked.connect(model.revertAll)

            button_layout.addWidget(refresh_btn)
            button_layout.addWidget(save_btn)
            button_layout.addWidget(cancel_btn)

            layout.addLayout(button_layout)

            self.tabs.addTab(tab, tab_name)

    def add_query_tab(self):
        """Добавляет вкладку с предустановленными запросами"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Выбор запроса
        layout.addWidget(QLabel("Выберите статистический запрос:"))
        query_combo = QComboBox()
        query_combo.addItems(
            [
                "Выберите запрос...",
                "Топ-5 бомбардиров",
                "Статистика команд",
                "Тренеры команд",
                "Игроки с истекающими контрактами",
                "Команды с лучшей защитой (топ-10)",
            ]
        )
        layout.addWidget(query_combo)

        # Таблица для результатов
        result_view = QTableView()
        result_view.setAlternatingRowColors(True)
        layout.addWidget(result_view)

        # SQL запросы
        queries = {
            1: """
                SELECT 
                    p.first_name || ' ' || p.last_name AS Игрок,
                    COUNT(g.goal_id) AS Голы
                FROM Goals g
                JOIN Players p ON g.player_id = p.player_id
                WHERE g.is_own_goal = 0
                GROUP BY p.player_id
                ORDER BY Голы DESC
                LIMIT 5
            """,
            2: """
                SELECT
                    t.name AS Команда,
                    SUM(CASE WHEN (m.home_team_id = t.team_id AND m.home_team_score > m.away_team_score) 
                              OR (m.away_team_id = t.team_id AND m.away_team_score > m.home_team_score) THEN 1 ELSE 0 END) AS Победы,
                    SUM(CASE WHEN (m.home_team_id = t.team_id AND m.home_team_score < m.away_team_score) 
                              OR (m.away_team_id = t.team_id AND m.away_team_score < m.home_team_score) THEN 1 ELSE 0 END) AS Поражения,
                    SUM(CASE WHEN m.home_team_score = m.away_team_score THEN 1 ELSE 0 END) AS Ничьи
                FROM Teams t
                LEFT JOIN Matches m ON t.team_id = m.home_team_id OR t.team_id = m.away_team_id
                WHERE m.match_status = 'completed'
                GROUP BY t.team_id
                ORDER BY Победы DESC
            """,
            3: """
                SELECT 
                    c.first_name || ' ' || c.last_name AS Тренер,
                    t.name AS Команда,
                    c.nationality AS Национальность
                FROM Coaches c
                LEFT JOIN Teams t ON c.team_id = t.team_id
                ORDER BY t.name
            """,
            4: """
                SELECT 
                    p.first_name || ' ' || p.last_name AS Игрок,
                    t.name AS Команда,
                    p.contract_end_date AS 'Дата окончания контракта'
                FROM Players p
                JOIN Teams t ON p.team_id = t.team_id
                WHERE p.contract_end_date BETWEEN date('now') AND date('now', '+30 days')
                ORDER BY p.contract_end_date
            """,
            5: """
                SELECT 
                    t.name AS Команда,
                    SUM(CASE WHEN m.home_team_id = t.team_id THEN m.away_team_score ELSE m.home_team_score END) AS 'Пропущено голов'
                FROM Matches m
                JOIN Teams t ON t.team_id IN (m.home_team_id, m.away_team_id)
                GROUP BY t.team_id
                ORDER BY 'Пропущено голов' ASC
                LIMIT 10
            """,
        }

        # Обработка выбора запроса
        def execute_query(index):
            if index == 0:
                return

            model = QSqlQueryModel()
            model.setQuery(queries[index])
            result_view.setModel(model)

        query_combo.currentIndexChanged.connect(execute_query)

        self.tabs.addTab(tab, "Статистика")


def main():
    app = QApplication(sys.argv)
    window = SportsLeagueDB()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

