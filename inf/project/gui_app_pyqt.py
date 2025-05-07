# --- START OF FILE gui_app_pyqt.py ---
import sys
import os # Для работы с путями к БД
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QLabel, QTabWidget, QTableWidget,
    QTableWidgetItem, QHeaderView, QSplitter, QTextEdit, QScrollArea, QFrame,
    QMessageBox # Import QMessageBox for error dialog
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QPixmap, QIcon # QPixmap и QIcon для будущей работы с изображениями
from typing import Dict, List, Any, Optional, Tuple # <--- ADD THIS LINE

# Импортируем модуль с функциями запросов к БД
import requests_db

# --- Константы и Настройки ---
WINDOW_TITLE = "Sports League Explorer (PyQt6)"
INITIAL_WIDTH = 1300
INITIAL_HEIGHT = 800
# Определяем путь к БД относительно текущего файла
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DB_PATH = os.path.join(SCRIPT_DIR, 'sports_league.db')

# --- Стили QSS (CSS для PyQt) ---
# (Стили оставлены без изменений, так как они относятся к оформлению)
STYLESHEET = """
QMainWindow {
    background-color: #f0f0f0; /* Светло-серый фон окна */
}

QWidget#mainWidget {
    /* Можно добавить стиль для главного виджета, если нужно */
}

QListWidget {
    background-color: #ffffff;
    border: 1px solid #cccccc;
    border-radius: 4px;
    font-size: 14px;
    padding: 5px;
}

QListWidget::item {
    padding: 6px 4px; /* Отступы внутри элемента списка */
}

QListWidget::item:selected {
    background-color: #d0e4f8; /* Цвет выделения */
    color: #000000;
    border-radius: 3px;
}

QTabWidget::pane { /* Область под вкладками */
    border: 1px solid #cccccc;
    border-top: none;
    background-color: #ffffff;
    border-bottom-left-radius: 4px;
    border-bottom-right-radius: 4px;
}

QTabBar::tab { /* Стиль самой вкладки */
    background-color: #e1e1e1;
    border: 1px solid #c4c4c4;
    border-bottom: none; /* Убрать нижнюю границу у неактивной */
    padding: 8px 20px;
    margin-right: 2px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    font-weight: bold;
    color: #333333;
}

QTabBar::tab:selected { /* Стиль выбранной вкладки */
    background-color: #ffffff; /* Фон совпадает с панелью */
    border-color: #cccccc;
    margin-bottom: -1px; /* Немного поднять выбранную вкладку */
    color: #005a9e;
}

QTabBar::tab:!selected:hover {
    background-color: #ececec; /* Подсветка при наведении */
}


QLabel#headerLabel {
    font-size: 20px;
    font-weight: bold;
    color: #003366; /* Темно-синий */
    padding: 10px 0;
    qproperty-alignment: 'AlignCenter';
}

QLabel#titleLabel {
    font-size: 16px;
    font-weight: bold;
    color: #005a9e; /* Ярко-синий */
    padding-bottom: 5px;
}

QLabel#infoLabel {
    font-size: 14px;
    color: #333333;
    padding-bottom: 3px;
}

QLabel#placeholderLogoLabel {
    border: 2px dashed #aaaaaa; /* Пунктирная рамка */
    background-color: #f8f8f8;
    color: #aaaaaa;
    font-style: italic;
    min-width: 100px; /* Минимальный размер */
    min-height: 100px;
    qproperty-alignment: 'AlignCenter';
}

QTableWidget {
    border: 1px solid #cccccc;
    gridline-color: #e0e0e0; /* Цвет линий сетки */
    font-size: 13px;
    alternate-background-color: #f9f9f9; /* Чередование фона строк */
    selection-background-color: #d0e4f8; /* Цвет выделения */
    selection-color: #000000;
}

QHeaderView::section { /* Стиль заголовков таблицы */
    background-color: #e8e8e8;
    padding: 6px;
    border: none;
    border-bottom: 1px solid #cccccc;
    font-weight: bold;
    font-size: 13px;
    color: #333333;
}

QSplitter::handle {
    background-color: #d0d0d0; /* Цвет разделителя */
}

QSplitter::handle:horizontal {
    width: 3px;
}

QSplitter::handle:vertical {
    height: 3px;
}
"""

# --- Главное Окно ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        self.setGeometry(100, 100, INITIAL_WIDTH, INITIAL_HEIGHT)
        self.setStyleSheet(STYLESHEET)

        self.current_league_id = None
        self.db_path = DEFAULT_DB_PATH # Используем путь к БД

        self.init_ui()
        self.load_initial_data()

    def init_ui(self):
        """Инициализирует пользовательский интерфейс окна."""
        self.main_widget = QWidget()
        self.main_widget.setObjectName("mainWidget")
        self.setCentralWidget(self.main_widget)

        # Основной разделитель окна
        self.splitter = QSplitter(Qt.Orientation.Horizontal)

        # --- Левая панель (Список лиг) ---
        self.left_widget = QWidget()
        self.left_layout = QVBoxLayout(self.left_widget)
        self.left_layout.setContentsMargins(10, 10, 5, 10)

        left_title = QLabel("Лиги")
        left_title.setObjectName("titleLabel")
        self.left_layout.addWidget(left_title)

        self.leagues_list_widget = QListWidget()
        # Подключаем обработчик смены выбранного элемента
        self.leagues_list_widget.currentItemChanged.connect(self.on_league_selected)
        self.left_layout.addWidget(self.leagues_list_widget)

        self.splitter.addWidget(self.left_widget)
        self.splitter.setStretchFactor(0, 1) # Левая панель занимает 1 часть

        # --- Правая панель (Информация и вкладки) ---
        self.right_widget = QWidget()
        self.right_layout = QVBoxLayout(self.right_widget)
        self.right_layout.setContentsMargins(5, 10, 10, 10)

        self.header_label = QLabel("Выберите лигу для просмотра информации")
        self.header_label.setObjectName("headerLabel")
        # Устанавливаем перенос слов для длинных сообщений об ошибках
        self.header_label.setWordWrap(True)
        self.right_layout.addWidget(self.header_label)

        # Создаем виджет вкладок
        self.tab_widget = QTabWidget()
        self.right_layout.addWidget(self.tab_widget)

        # Создаем сами вкладки
        self.create_info_tab()
        self.create_teams_tab()
        self.create_standings_tab()
        self.create_scorers_tab()
        # При необходимости можно добавить другие вкладки здесь

        self.splitter.addWidget(self.right_widget)
        self.splitter.setStretchFactor(1, 3) # Правая панель занимает 3 части

        # Устанавливаем Splitter как основной layout
        main_layout = QHBoxLayout(self.main_widget)
        main_layout.addWidget(self.splitter)
        self.main_widget.setLayout(main_layout)

    def create_info_tab(self):
        """Создает содержимое вкладки 'Информация о лиге'."""
        self.info_tab = QWidget()
        layout = QVBoxLayout(self.info_tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        # Верхний фрейм для лого и основной информации
        top_frame = QFrame()
        top_layout = QHBoxLayout(top_frame)
        top_layout.setContentsMargins(0,0,0,0)

        # --- Виджет для логотипа лиги (пока заглушка) ---
        self.league_logo_label = QLabel("[ Логотип Лиги ]")
        self.league_logo_label.setObjectName("placeholderLogoLabel")
        self.league_logo_label.setFixedSize(120, 120)
        top_layout.addWidget(self.league_logo_label)
        # --- Конец виджета для логотипа ---

        # Фрейм для текстовой информации справа от лого
        info_details_frame = QFrame()
        info_details_layout = QVBoxLayout(info_details_frame)
        info_details_layout.setContentsMargins(10, 0, 0, 0)

        self.league_country_label = QLabel("Страна: ")
        self.league_country_label.setObjectName("infoLabel")
        info_details_layout.addWidget(self.league_country_label)

        self.league_founded_label = QLabel("Основана: ")
        self.league_founded_label.setObjectName("infoLabel")
        info_details_layout.addWidget(self.league_founded_label)

        info_details_layout.addStretch() # Прижимает информацию вверх
        top_layout.addWidget(info_details_frame, 1) # Растягивает фрейм с текстом
        layout.addWidget(top_frame)

        # Описание лиги (в области прокрутки)
        desc_title = QLabel("Описание:")
        desc_title.setObjectName("titleLabel")
        layout.addWidget(desc_title)

        self.league_desc_area = QScrollArea()
        self.league_desc_area.setWidgetResizable(True) # Авто-изменение размера содержимого
        self.league_desc_area.setStyleSheet("QScrollArea { border: none; background-color: transparent; }") # Убираем рамку
        self.league_desc_label = QLabel("Нет описания.")
        self.league_desc_label.setObjectName("infoLabel")
        self.league_desc_label.setWordWrap(True) # Включаем перенос слов
        self.league_desc_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft) # Выравнивание по верху и левому краю
        self.league_desc_area.setWidget(self.league_desc_label)
        layout.addWidget(self.league_desc_area, 1) # Растягиваем область описания

        self.tab_widget.addTab(self.info_tab, " Информация ")

    def create_teams_tab(self):
        """Создает содержимое вкладки 'Команды'."""
        self.teams_tab = QWidget()
        layout = QVBoxLayout(self.teams_tab)
        layout.setContentsMargins(10, 10, 10, 10)

        self.teams_table = QTableWidget()
        self.teams_table.setColumnCount(3)
        self.teams_table.setHorizontalHeaderLabels(["ID", "Название команды", "Город"])
        self.teams_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers) # Запрет редактирования
        self.teams_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows) # Выделение строк
        self.teams_table.setAlternatingRowColors(True) # Чередование фона строк
        self.teams_table.verticalHeader().setVisible(False) # Скрытие номеров строк

        header = self.teams_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents) # ID по содержимому
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch) # Название растягивается
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents) # Город по содержимому

        layout.addWidget(self.teams_table)
        self.tab_widget.addTab(self.teams_tab, " Команды ")

    def create_standings_tab(self):
        """Создает содержимое вкладки 'Таблица' (Турнирная таблица)."""
        self.standings_tab = QWidget()
        layout = QVBoxLayout(self.standings_tab)
        layout.setContentsMargins(10, 10, 10, 10)

        self.standings_table = QTableWidget()
        col_names = ['#', 'Команда', 'И', 'В', 'Н', 'П', 'ЗМ', 'ПМ', 'РМ', 'Очки']
        self.standings_table.setColumnCount(len(col_names))
        self.standings_table.setHorizontalHeaderLabels(col_names)
        self.standings_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.standings_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.standings_table.setAlternatingRowColors(True)
        self.standings_table.verticalHeader().setVisible(False)

        header = self.standings_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents) # Позиция #
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch) # Команда
        for i in range(2, len(col_names)): # Остальные колонки по содержимому
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)

        layout.addWidget(self.standings_table)
        self.tab_widget.addTab(self.standings_tab, " Таблица ")

    def create_scorers_tab(self):
        """Создает содержимое вкладки 'Бомбардиры'."""
        self.scorers_tab = QWidget()
        layout = QVBoxLayout(self.scorers_tab)
        layout.setContentsMargins(10, 10, 10, 10)

        self.scorers_table = QTableWidget()
        col_names = ['#', 'Игрок', 'Команда', 'Голы']
        self.scorers_table.setColumnCount(len(col_names))
        self.scorers_table.setHorizontalHeaderLabels(col_names)
        self.scorers_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.scorers_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.scorers_table.setAlternatingRowColors(True)
        self.scorers_table.verticalHeader().setVisible(False)

        header = self.scorers_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents) # Ранг #
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch) # Игрок
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch) # Команда
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents) # Голы

        layout.addWidget(self.scorers_table)
        self.tab_widget.addTab(self.scorers_tab, " Бомбардиры ")

    def load_initial_data(self):
        """Загружает список лиг из БД при запуске приложения."""
        if not os.path.exists(self.db_path):
            error_message = f"ОШИБКА: Файл базы данных не найден!\nПуть: {self.db_path}\n\nУбедитесь, что скрипты db.py и read_data.py были успешно запущены."
            self.header_label.setText(error_message)
            self.header_label.setStyleSheet("color: red; font-weight: bold;")
            QMessageBox.critical(self, "Ошибка базы данных", error_message)
            # Блокируем интерфейс, если БД нет
            self.leagues_list_widget.setEnabled(False)
            self.tab_widget.setEnabled(False)
            return

        # Сбрасываем стиль header_label на случай, если ранее была ошибка
        self.header_label.setStyleSheet("")
        self.header_label.setText("Выберите лигу для просмотра информации")

        try:
            leagues = requests_db.get_all_leagues(db_path=self.db_path)
            self.leagues_list_widget.clear()
            if not leagues:
                self.leagues_list_widget.addItem("Лиги не найдены в базе данных.")
                self.leagues_list_widget.setEnabled(False)
                self.tab_widget.setEnabled(False) # Блокируем и вкладки
                return

            self.leagues_list_widget.setEnabled(True)
            self.tab_widget.setEnabled(True) # Разблокируем вкладки
            for league in leagues:
                item = QListWidgetItem(f"{league['name']} ({league['country']})")
                # Сохраняем ID лиги внутри элемента списка для последующего использования
                item.setData(Qt.ItemDataRole.UserRole, league['league_id'])
                self.leagues_list_widget.addItem(item)
        except Exception as e:
             error_message = f"Ошибка при загрузке лиг из БД:\n{e}"
             self.header_label.setText(error_message)
             self.header_label.setStyleSheet("color: red; font-weight: bold;")
             QMessageBox.critical(self, "Ошибка чтения БД", error_message)
             self.leagues_list_widget.setEnabled(False)
             self.tab_widget.setEnabled(False)


    def on_league_selected(self, current_item: Optional[QListWidgetItem], previous_item: Optional[QListWidgetItem]):
        """Обработчик события выбора лиги в списке."""
        if current_item is None:
            self.current_league_id = None
            self.header_label.setText("Выберите лигу для просмотра информации")
            self.clear_details() # Очищаем правую панель
            return

        league_id = current_item.data(Qt.ItemDataRole.UserRole)
        if league_id is None: # Дополнительная проверка
            print("Warning: Выбранный элемент списка не содержит league_id.")
            return

        self.current_league_id = league_id
        try:
            league_data = requests_db.get_league_by_id(self.current_league_id, db_path=self.db_path)

            if league_data:
                self.header_label.setText(league_data.get('name', 'Неизвестная Лига'))
                # Обновляем все вкладки для выбранной лиги
                self.update_info_tab(league_data)
                self.update_teams_tab(self.current_league_id)
                self.update_standings_tab(self.current_league_id)
                self.update_scorers_tab(self.current_league_id)
            else:
                self.header_label.setText(f"Информация для лиги ID={self.current_league_id} не найдена")
                self.clear_details()
        except Exception as e:
            error_message = f"Ошибка при загрузке данных лиги ID={self.current_league_id}:\n{e}"
            self.header_label.setText(error_message)
            self.header_label.setStyleSheet("color: red; font-weight: bold;")
            QMessageBox.warning(self, "Ошибка чтения данных", error_message)
            self.clear_details()


    def clear_details(self):
        """Очищает все поля и таблицы на правой панели при смене лиги или ошибке."""
        # Вкладка Информация
        self.league_logo_label.setText("[ Логотип Лиги ]")
        # self.league_logo_label.clear() # Если используется QPixmap
        self.league_country_label.setText("Страна: ")
        self.league_founded_label.setText("Основана: ")
        self.league_desc_label.setText("Нет данных.")
        # Очистка таблиц
        self.teams_table.setRowCount(0)
        self.standings_table.setRowCount(0)
        self.scorers_table.setRowCount(0)

    def update_info_tab(self, league_data: Dict[str, Any]):
        """Обновляет содержимое вкладки 'Информация' данными о лиге."""
        self.league_country_label.setText(f"Страна: {league_data.get('country', 'N/A')}")
        founded = league_data.get('founded_year')
        self.league_founded_label.setText(f"Основана: {founded if founded else 'N/A'}")
        description = league_data.get('description')
        # Отображаем "Нет описания", если поле пустое или None
        self.league_desc_label.setText(description if description and description.strip() else 'Нет описания.')

        # --- ЗАГЛУШКА: Загрузка логотипа лиги ---
        logo_url = league_data.get('logo_url')
        if logo_url:
            # TODO: Реализовать асинхронную загрузку и отображение изображения
            self.league_logo_label.setText("[ Лого URL есть ]")
        else:
             self.league_logo_label.setText("[ Нет Лого ]")
        # --- Конец заглушки ---

    def _populate_table(self, table: QTableWidget, data: List[Dict[str, Any]], columns: List[Tuple[str, str, Qt.AlignmentFlag]]):
        """Вспомогательный метод для заполнения таблицы данными."""
        try:
            table.setRowCount(0) # Очищаем перед заполнением
            table.setRowCount(len(data))
            if not data:
                # Показываем сообщение об отсутствии данных
                table.setRowCount(1)
                no_data_item = QTableWidgetItem("Нет данных")
                no_data_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                table.setItem(0, 0, no_data_item)
                # Объединяем ячейки для сообщения
                if table.columnCount() > 1:
                    table.setSpan(0, 0, 1, table.columnCount())
                return

            # Сбрасываем объединение ячеек, если оно было
            table.clearSpans()

            for row_idx, row_data in enumerate(data):
                for col_idx, (key, default_value, alignment) in enumerate(columns):
                    # Используем default_value если ключ отсутствует
                    value = row_data.get(key, default_value)
                    # Преобразуем в строку, обрабатывая None
                    item_text = str(value) if value is not None else str(default_value)
                    item = QTableWidgetItem(item_text)
                    item.setTextAlignment(alignment)
                    table.setItem(row_idx, col_idx, item)
        except Exception as e:
             print(f"Ошибка при заполнении таблицы {table.objectName()}: {e}")
             # Отображаем ошибку в таблице
             table.setRowCount(1)
             error_item = QTableWidgetItem(f"Ошибка: {e}")
             error_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
             error_item.setForeground(Qt.GlobalColor.red)
             table.setItem(0, 0, error_item)
             if table.columnCount() > 1:
                 table.setSpan(0, 0, 1, table.columnCount())


    def update_teams_tab(self, league_id: int):
        """Обновляет содержимое вкладки 'Команды'."""
        try:
            teams = requests_db.get_teams_by_league(league_id, db_path=self.db_path)
            columns = [
                ('team_id', 'N/A', Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter),
                ('name', 'N/A', Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter),
                ('city', 'N/A', Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            ]
            self._populate_table(self.teams_table, teams, columns)
        except Exception as e:
            print(f"Ошибка при обновлении вкладки команд: {e}")
            self._populate_table(self.teams_table, [], []) # Показать "Нет данных" или ошибку

    def update_standings_tab(self, league_id: int):
        """Обновляет содержимое вкладки 'Таблица'."""
        try:
            standings = requests_db.get_league_standings(league_id, db_path=self.db_path)

            standings_with_rank = []
            for i, team_data in enumerate(standings):
                team_data['rank'] = i + 1
                standings_with_rank.append(team_data)

            columns = [
                ('rank', '#', Qt.AlignmentFlag.AlignCenter),
                ('team_name', 'Команда', Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter),
                ('played', '0', Qt.AlignmentFlag.AlignCenter),
                ('won', '0', Qt.AlignmentFlag.AlignCenter),
                ('drawn', '0', Qt.AlignmentFlag.AlignCenter),
                ('lost', '0', Qt.AlignmentFlag.AlignCenter),
                ('goals_for', '0', Qt.AlignmentFlag.AlignCenter),
                ('goals_against', '0', Qt.AlignmentFlag.AlignCenter),
                ('goal_difference', '0', Qt.AlignmentFlag.AlignCenter),
                ('points', '0', Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
            ]
            self._populate_table(self.standings_table, standings_with_rank, columns)
        except Exception as e:
            print(f"Ошибка при обновлении вкладки таблицы: {e}")
            self._populate_table(self.standings_table, [], [])

    def update_scorers_tab(self, league_id: int):
        """Обновляет содержимое вкладки 'Бомбардиры'."""
        try:
            scorers = requests_db.get_league_top_scorers(league_id, limit=50, db_path=self.db_path)

            scorers_processed = []
            for i, scorer in enumerate(scorers):
                 scorer['rank'] = i + 1
                 scorer['full_name'] = f"{scorer.get('first_name', '')} {scorer.get('last_name', '')}".strip()
                 scorers_processed.append(scorer)

            columns = [
                ('rank', '#', Qt.AlignmentFlag.AlignCenter),
                ('full_name', 'N/A', Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter),
                ('team_name', 'N/A', Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter),
                ('goals_count', '0', Qt.AlignmentFlag.AlignCenter)
            ]
            self._populate_table(self.scorers_table, scorers_processed, columns)
        except Exception as e:
            print(f"Ошибка при обновлении вкладки бомбардиров: {e}")
            self._populate_table(self.scorers_table, [], [])


# --- Запуск приложения ---
if __name__ == '__main__':
    # Проверка существования БД перед запуском GUI
    if not os.path.exists(DEFAULT_DB_PATH):
        # Используем QMessageBox для уведомления пользователя, если PyQt уже импортирован
        app_temp = QApplication.instance() # Проверяем, существует ли уже экземпляр
        if app_temp is None:
            app_temp = QApplication(sys.argv) # Создаем временный для QMessageBox

        error_message = f"ОШИБКА: Файл базы данных не найден!\nПуть: {DEFAULT_DB_PATH}\n\nПожалуйста, запустите сначала 'db.py', а затем 'read_data.py'."
        QMessageBox.critical(None, "Ошибка базы данных", error_message)
        print(error_message) # Также выводим в консоль
        sys.exit(1) # Выход с кодом ошибки

    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
# --- END OF FILE gui_app_pyqt.py ---