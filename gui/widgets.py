# gui/widgets.py
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton,
    QSizePolicy, QScrollArea
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


# ---------- helpers (только внутри этого файла) ----------

def _btn_style(bg: str, hover: str, pressed: str, disabled: str = "#2a2f3a") -> str:
    return f"""
    QPushButton {{
        font-size: 12px;
        font-weight: 800;
        padding: 9px 12px;
        background-color: {bg};
        color: #FFFFFF;
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 10px;
    }}
    QPushButton:hover {{
        background-color: {hover};
        border: 1px solid rgba(255,255,255,0.16);
    }}
    QPushButton:pressed {{
        background-color: {pressed};
    }}
    QPushButton:disabled {{
        background-color: {disabled};
        color: rgba(255,255,255,0.45);
        border: 1px solid rgba(255,255,255,0.08);
    }}
    """

def _pill_label_style() -> str:
    return """
    QLabel {
        font-size: 13px;
        font-weight: 900;
        color: #e8edf6;
        padding: 10px 14px;
        background-color: #0f1320;
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 12px;
    }
    """

def _title_style() -> str:
    return """
    QLabel {
        font-size: 15px;
        font-weight: 900;
        color: #e8edf6;
        padding: 10px 12px;
    }
    """

def _card_style() -> str:
    return """
    QWidget {
        background-color: #0b1020;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
    }
    """


# ---------- widgets ----------

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=16, height=8, dpi=120):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        self.setMinimumSize(800, 600)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # легкий темный фон под график (matplotlib сам рисует оси, но белое окно раздражает)
        self.fig.patch.set_facecolor("#0b1020")


class PlotControlWidget(QWidget):
    plot_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_plot_index = 0
        self.plot_titles = ["ИСХОДНЫЙ СИГНАЛ", "ОБРАБОТАННЫЙ СИГНАЛ", "АНАЛИЗ РИТМОВ"]
        self.initUI()

    def initUI(self):
        outer = QVBoxLayout()
        outer.setContentsMargins(12, 10, 12, 10)
        outer.setSpacing(8)

        # "карточка" вокруг контролов
        card = QWidget()
        card.setStyleSheet(_card_style())
        row = QHBoxLayout(card)
        row.setContentsMargins(12, 10, 12, 10)
        row.setSpacing(10)

        self.btn_prev = QPushButton("◀ Назад")
        self.btn_prev.setStyleSheet(_btn_style(
            bg="#1f2430", hover="#2a3040", pressed="#151922"
        ))
        self.btn_prev.clicked.connect(self.show_previous_plot)
        self.btn_prev.setMinimumWidth(120)
        row.addWidget(self.btn_prev)

        self.current_plot_label = QLabel(self.plot_titles[self.current_plot_index])
        self.current_plot_label.setStyleSheet(_pill_label_style())
        self.current_plot_label.setAlignment(Qt.AlignCenter)
        row.addWidget(self.current_plot_label, 1)

        self.btn_next = QPushButton("Вперёд ▶")
        self.btn_next.setStyleSheet(_btn_style(
            bg="#1f2430", hover="#2a3040", pressed="#151922"
        ))
        self.btn_next.clicked.connect(self.show_next_plot)
        self.btn_next.setMinimumWidth(120)
        row.addWidget(self.btn_next)

        outer.addWidget(card)

        # маленькая подсказка-строка снизу (необязательно, но красиво)
        hint = QLabel("Переключайся между графиками: исходный → обработанный → анализ")
        hint.setStyleSheet("QLabel { font-size: 11px; color: rgba(232,237,246,0.65); padding-left: 6px; }")
        outer.addWidget(hint)

        self.setLayout(outer)
        self.update_buttons()

    def show_previous_plot(self):
        if self.current_plot_index > 0:
            self.current_plot_index -= 1
            self.update_display()

    def show_next_plot(self):
        if self.current_plot_index < len(self.plot_titles) - 1:
            self.current_plot_index += 1
            self.update_display()

    def update_display(self):
        self.current_plot_label.setText(self.plot_titles[self.current_plot_index])
        self.update_buttons()
        self.plot_changed.emit(self.current_plot_index)

    def update_buttons(self):
        self.btn_prev.setEnabled(self.current_plot_index > 0)
        self.btn_next.setEnabled(self.current_plot_index < len(self.plot_titles) - 1)

    def get_current_plot_index(self):
        return self.current_plot_index

    def set_current_plot_index(self, index):
        if 0 <= index < len(self.plot_titles):
            self.current_plot_index = index
            self.update_display()


class ScrollablePlotWidget(QWidget):
    def __init__(self, title, canvas, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(8)

        title_label = QLabel(title)
        title_label.setStyleSheet(_title_style())
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setWidget(canvas)
        scroll_area.setMinimumSize(400, 500)

        # темный стиль скролла (чтобы не вылезал светлый прямоугольник)
        # scroll_area.setStyleSheet("""
        #     QScrollArea {
        #         background: #0b1020;
        #         border: 1px solid rgba(255,255,255,0.08);
        #         border-radius: 14px;
        #     }
        #     QScrollBar:vertical, QScrollBar:horizontal {
        #         background: transparent;
        #         width: 10px;
        #         height: 10px;
        #         margin: 2px;
        #     }
        #     QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
        #         background: rgba(255,255,255,0.18);
        #         border-radius: 6px;
        #         min-height: 30px;
        #         min-width: 30px;
        #     }
        #     QScrollBar::handle:hover { background: rgba(255,255,255,0.26); }
        #     QScrollBar::add-line, QScrollBar::sub-line { height: 0px; width: 0px; }
        #     QScrollBar::add-page, QScrollBar::sub-page { background: transparent; }
        # """)

        layout.addWidget(scroll_area)
        self.setLayout(layout)