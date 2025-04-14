import sys
import os
from pathlib import Path
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    qml_file = Path(__file__).parent / "./main.qml"
    engine.load(qml_file)

    if not engine.rootObjects():
        print(f"Ошибка: Не удалось загрузить QML файл: {qml_file}")
        sys.exit(-1)

    sys.exit(app.exec())

