# gui/menu_bar.py
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QAction, QMessageBox


class EEGMenuBar:
    def __init__(self, parent):
        self.parent = parent
        self.create_menu_bar()

    def create_menu_bar(self):
        menubar = self.parent.menuBar()

        # ---- Dark UI styling for native menubar/menu ----
        # Важно: стили применяем к QMenuBar/QMenu, логика экшенов не меняется.
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: #0b1020;
                color: #e8edf6;
                border-bottom: 1px solid rgba(255,255,255,0.08);
                padding: 4px 8px;
            }
            QMenuBar::item {
                background: transparent;
                padding: 6px 10px;
                border-radius: 8px;
                margin: 2px 2px;
            }
            QMenuBar::item:selected {
                background-color: rgba(255,255,255,0.10);
            }
            QMenuBar::item:pressed {
                background-color: rgba(255,255,255,0.14);
            }

            QMenu {
                background-color: #0f1320;
                color: #e8edf6;
                border: 1px solid rgba(255,255,255,0.10);
                border-radius: 10px;
                padding: 6px;
            }
            QMenu::item {
                padding: 8px 14px;
                border-radius: 8px;
            }
            QMenu::item:selected {
                background-color: rgba(77, 163, 255, 0.22);
                border: 1px solid rgba(77, 163, 255, 0.20);
            }
            QMenu::separator {
                height: 1px;
                background: rgba(255,255,255,0.10);
                margin: 6px 6px;
            }
        """)

        self.create_file_menu(menubar)
        self.create_processing_menu(menubar)
        self.create_analysis_menu(menubar)
        self.create_help_menu(menubar)

    def create_file_menu(self, menubar):
        file_menu = menubar.addMenu('&Файл')

        open_action = QAction('📂 &Открыть...', self.parent)
        open_action.setShortcut(QKeySequence.Open)
        open_action.triggered.connect(self.parent.load_data)
        file_menu.addAction(open_action)

        test_action = QAction('🧪 &Тестовые данные', self.parent)
        test_action.setShortcut('Ctrl+T')
        test_action.triggered.connect(self.parent.generate_test_data)
        file_menu.addAction(test_action)

        file_menu.addSeparator()

        exit_action = QAction('⏻ В&ыход', self.parent)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.parent.close)
        file_menu.addAction(exit_action)

    def create_processing_menu(self, menubar):
        processing_menu = menubar.addMenu('&Обработка')

        process_action = QAction('⚙️ &Обработать сигнал', self.parent)
        process_action.setShortcut('Ctrl+P')
        process_action.triggered.connect(self.parent.process_data)
        processing_menu.addAction(process_action)

    def create_analysis_menu(self, menubar):
        analysis_menu = menubar.addMenu('&Анализ')

        analyze_action = QAction('🧠 &Анализ ритмов', self.parent)
        analyze_action.setShortcut('Ctrl+A')
        analyze_action.triggered.connect(self.parent.analyze_rhythms)
        analysis_menu.addAction(analyze_action)

    def create_help_menu(self, menubar):
        help_menu = menubar.addMenu('&Справка')

        about_action = QAction('ℹ️ &О программе', self.parent)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def show_about(self):
        about_text = """
<h2 style="margin-bottom:6px;">EEG Analyzer</h2>
<p><b>Профессиональный анализатор ЭЭГ</b></p>
<p>Версия: 2.0.0 (Оптимизированная)</p>
<p>Комплексная система для анализа электроэнцефалограмм</p>
        """
        # Можно также задать темный стиль самому QMessageBox, но это опционально — не лезу в системные окна.
        QMessageBox.about(self.parent, "О программе", about_text)