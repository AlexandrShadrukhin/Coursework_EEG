# gui/panels.py
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QComboBox, QSpinBox,
    QDoubleSpinBox, QCheckBox, QGroupBox, QTextEdit,
    QTabWidget, QProgressBar, QSizePolicy, QFrame,
    QAbstractSpinBox
)

from performance.performance_widget import PerformanceWidget


# -----------------------------
# Shared styling helpers
# -----------------------------
_APP_BG = "#0d1117"
_CARD_BG = "#111827"
_CARD_BG_2 = "#0f172a"
_BORDER = "#243244"
_TEXT = "#e5e7eb"
_MUTED = "#9ca3af"
_ACCENT = "#3b82f6"
_GOOD = "#22c55e"
_WARN = "#f59e0b"
_PURPLE = "#8b5cf6"
_CYAN = "#06b6d4"
_DANGER = "#ef4444"



def _card(title: str = "", subtitle: str = "") -> QGroupBox:
    box = QGroupBox(title)
    box.setProperty("card", True)
    if subtitle:
        box.setToolTip(subtitle)
    return box


def _apply_spin_clean(spin):
    """
    Fix: "торчащие стрелки" у spinbox.
    Полностью убираем up/down кнопки и делаем поле как обычный инпут.
    """
    spin.setButtonSymbols(QAbstractSpinBox.NoButtons)
    spin.setAccelerated(True)
    spin.setKeyboardTracking(False)
    spin.setFixedHeight(36)


def _base_stylesheet() -> str:
    return f"""
    QWidget {{
        font-family: "Helvetica Neue", Helvetica, Arial;
        color: #e5e7eb;
        font-size: 13px;
    }}
    QMainWindow, QWidget#centralWidget, QWidget#MainWindow, QWidget#root, QWidget {{
        background-color: {_APP_BG};
    }}

    /* Cards */
    QGroupBox[card="true"] {{
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                    stop:0 {_CARD_BG}, stop:1 {_CARD_BG_2});
        border: 1px solid {_BORDER};
        border-radius: 12px;
        margin-top: 12px;
        padding: 28px 14px 14px 14px;
    }}
    QGroupBox[card="true"]::title {{
        subcontrol-origin: padding;
        subcontrol-position: top left;
        left: 16px;
        top: 10px;                           /* ниже/выше */
        padding: 2px 10px;
        border-radius: 8px;
        background: rgba(255,255,255,0.06);  /* лёгкая плашка внутри */
        color: rgba(233,238,247,0.92);
        font-weight: 800;
    }}

    QLabel#muted {{
        color: {_MUTED};
        font-size: 12px;
    }}

    /* Inputs */
    QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit {{
        background-color: #0b1220;
        border: 1px solid {_BORDER};
        border-radius: 10px;
        padding: 7px 10px;
        selection-background-color: {_ACCENT};
        selection-color: white;
    }}
    QComboBox {{
        min-height: 36px;
        padding-right: 26px;
    }}
    QComboBox::drop-down {{
        width: 24px;
        border: none;
    }}
    QComboBox::down-arrow {{
        image: none;
        border: none;
        width: 0px;
        height: 0px;
    }}
    /* ===== ComboBox dropdown (popup list) ===== */
    QComboBox QAbstractItemView {{
        background: #0b1220;
        color: #E5E7EB;

        border: 1px solid rgba(36,50,68,0.9);
        border-radius: 12px;

        padding: 6px;

        outline: 0;
        selection-background-color: rgba(59,130,246,0.25);
        selection-color: #E5E7EB;
    }}

    QComboBox QAbstractItemView::item {{
        padding: 10px 12px;
        margin: 2px 4px;
        border-radius: 10px;
    }}

    QComboBox QAbstractItemView::item:selected {{
        background: rgba(59,130,246,0.22);
        color: #E5E7EB;
    }}

    QComboBox QAbstractItemView {{
        show-decoration-selected: 1;
    }}

    /* ===== Scrollbar внутри dropdown тоже в тему ===== */
    QComboBox QAbstractItemView QScrollBar:vertical {{
        width: 14px;
        background: transparent;
        margin: 6px 4px 6px 4px;
    }}
    QComboBox QAbstractItemView QScrollBar::handle:vertical {{
        background: rgba(229,231,235,0.26);
        border-radius: 7px;
        border: 2px solid transparent;
        background-clip: padding;
        min-height: 28px;
    }}
    QComboBox QAbstractItemView QScrollBar::handle:vertical:hover {{
        background: rgba(229,231,235,0.38);
    }}
    QComboBox QAbstractItemView QScrollBar::add-line:vertical,
    QComboBox QAbstractItemView QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    QComboBox QAbstractItemView QScrollBar::add-page:vertical,
    QComboBox QAbstractItemView QScrollBar::sub-page:vertical {{
        background: transparent;
    }}

    /* Spinbox: no arrows and clean padding */
    QSpinBox, QDoubleSpinBox {{
        min-height: 36px;
        padding-right: 10px;
    }}
    QAbstractSpinBox::up-button, QAbstractSpinBox::down-button {{
        width: 0px;
        border: none;
        background: transparent;
    }}

    /* Checkboxes */
    QCheckBox {{
        background: transparent;
        border: none;
        padding: 6px 6px;
        margin: 0px;
        spacing: 10px;
        color: #e5e7eb;
        font-weight: 700;
    }}
    
    QCheckBox:hover {{
        background: rgba(255,255,255,0.04);
        border-radius: 10px;
    }}
    
    QCheckBox::indicator {{
        width: 18px;
        height: 18px;
        border-radius: 6px;
        border: 1px solid {_BORDER};
        background: #0b1220;
    }}
    
    QCheckBox::indicator:checked {{
        background: {_ACCENT};
        border: 1px solid {_ACCENT};
    }}
    
    QCheckBox::indicator:checked:hover {{
        background: #2563eb;
        border: 1px solid #2563eb;
    }}

    /* Buttons */
    QPushButton {{
        border: 1px solid {_BORDER};
        border-radius: 12px;
        padding: 10px 14px;
        font-weight: 700;
        background: #0b1220;
    }}
    QPushButton:hover {{
        border-color: #36506a;
        background: #0b1528;
    }}
    QPushButton:disabled {{
        background: #0b1220;
        color: #6b7280;
        border-color: #1f2937;
    }}

    QPushButton#primary {{
        background: {_ACCENT};
        border-color: {_ACCENT};
        color: white;
    }}
    QPushButton#primary:hover {{
        background: #2563eb;
        border-color: #2563eb;
    }}

    QPushButton#success {{
        background: {_GOOD};
        border-color: {_GOOD};
        color: #052e16;
    }}
    QPushButton#success:hover {{
        background: #16a34a;
        border-color: #16a34a;
        color: #052e16;
    }}

    QPushButton#warning {{
        background: {_WARN};
        border-color: {_WARN};
        color: #3a2100;
    }}
    QPushButton#warning:hover {{
        background: #d97706;
        border-color: #d97706;
    }}

    QPushButton#purple {{
        background: {_PURPLE};
        border-color: {_PURPLE};
        color: white;
    }}
    QPushButton#purple:hover {{
        background: #7c3aed;
        border-color: #7c3aed;
    }}

    QPushButton#cyan {{
        background: {_CYAN};
        border-color: {_CYAN};
        color: #00323a;
    }}
    QPushButton#cyan:hover {{
        background: #0891b2;
        border-color: #0891b2;
    }}

    QPushButton#danger {{
        background: {_DANGER};
        border-color: {_DANGER};
        color: white;
    }}
    QPushButton#danger:hover {{
        background: #dc2626;
        border-color: #dc2626;
    }}

    /* Tabs */
    QTabWidget::pane {{
        border: 1px solid {_BORDER};
        border-radius: 0px;
        top: -1px;
        background: {_CARD_BG_2};
    }}
    QTabBar::tab {{
        background: #0b1220;
        border: 1px solid {_BORDER};
        border-bottom: none;
        padding: 12px 12px;
        min-width: 120px;
        border-top-left-radius: 10px;
        border-top-right-radius: 10px;
        margin-right: 6px;
        color: {_MUTED};
        font-weight: 700;
    }}
    QTabBar::tab:selected {{
        background: {_CARD_BG_2};
        color: {_TEXT};
        border-color: #36506a;
    }}

    /* GroupBoxes not marked as card */
    QGroupBox {{
        border: none;
        background: transparent;
        margin-top: 10px;
        padding: 10px;
    }}
    
    /* ===== Scrollbars (тонкие, капсула, без стрелок) ===== */
    /* VERTICAL */
    QScrollBar:vertical {{
        width: 17px;                 /* было 16 -> +1px */
        background: transparent;
        margin: 4px 4px 6px 4px;     /* отступы самого скроллбара */
    }}
    
    QScrollBar::handle:vertical {{
        background: rgba(229,231,235,0.30);
        border-radius: 999px;        /* капсула */
        min-height: 34px;
    
        /* ключ: создаём внутренний отступ, чтобы торцы были круглыми */
        border: 3px solid transparent;
        background-clip: padding;
    
        /* ключ: ручка не должна упираться в края */
        margin: 2px 3px 2px 3px;     /* top right bottom left */
    }}
    
    QScrollBar::handle:vertical:hover {{
        background: rgba(229,231,235,0.44);
    }}
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
        background: transparent;
        border: none;
    }}
    
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
        background: transparent;
    }}
    
    
    /* HORIZONTAL */
    QScrollBar:horizontal {{
        height: 15px;                /* можно тоже чуть подправить */
        background: transparent;
        margin: 4px 6px 4px 6px;
    }}
    
    QScrollBar::handle:horizontal {{
        background: rgba(229,231,235,0.30);
        border-radius: 999px;
        min-width: 34px;
    
        border: 3px solid transparent;
        background-clip: padding;
    
        margin: 3px 2px 3px 2px;
    }}
    
    QScrollBar::handle:horizontal:hover {{
        background: rgba(229,231,235,0.44);
    }}
    
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0px;
        background: transparent;
        border: none;
    }}
    
    QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
        background: transparent;
    }}
        QFrame {{
        border: none;
        background: transparent;
    }}
    """


# -----------------------------
# TOP BAR (Data controls)
# -----------------------------
class TopControlPanel(QWidget):
    """
    Раньше это была одна горизонтальная колбаса.
    Теперь: "toolbar" + "control card" внутри.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_app = parent
        self.initUI()

    def initUI(self):
        self.setStyleSheet(_base_stylesheet())

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(10)

        # Toolbar-like row
        toolbar = QFrame()
        toolbar.setProperty("card", True)
        toolbar.setStyleSheet("""
            QFrame[card="true"]{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #0b1220, stop:1 #0f172a);
                border: 1px solid #243244;
                border-radius: 14px;
                padding: 10px;
            }
        """)
        tb = QHBoxLayout(toolbar)
        tb.setContentsMargins(12, 10, 12, 10)
        tb.setSpacing(12)

        # Left actions
        left = QVBoxLayout()
        left.setSpacing(6)
        title = QLabel("Анализ ЭЭГ")
        title.setStyleSheet("font-size: 14px; font-weight: 800;")
        subtitle = QLabel("Загрузка файлов и выбор режима визуализации")
        subtitle.setObjectName("muted")
        left.addWidget(title)
        left.addWidget(subtitle)
        tb.addLayout(left, 2)

        # Buttons cluster
        btns = QHBoxLayout()
        btns.setSpacing(10)

        self.btn_load = QPushButton("Загрузить ЭЭГ")
        self.btn_load.setObjectName("success")
        self.btn_load.setMinimumWidth(160)

        self.btn_test = QPushButton("Тестовые данные")
        self.btn_test.setObjectName("primary")
        self.btn_test.setMinimumWidth(170)

        btns.addWidget(self.btn_load)
        btns.addWidget(self.btn_test)
        tb.addLayout(btns, 1)

        # Right selectors (compact)
        right = QGridLayout()
        right.setHorizontalSpacing(10)
        right.setVerticalSpacing(8)

        lbl_ch = QLabel("Канал")
        lbl_ch.setObjectName("muted")
        self.channel_combo = QComboBox()

        lbl_viz = QLabel("Визуализация")
        lbl_viz.setObjectName("muted")
        self.viz_combo = QComboBox()
        self.viz_combo.addItems(["Временной ряд", "Спектр мощности", "Все каналы", "Спектрограмма"])

        right.addWidget(lbl_ch, 0, 0)
        right.addWidget(self.channel_combo, 1, 0)
        right.addWidget(lbl_viz, 0, 1)
        right.addWidget(self.viz_combo, 1, 1)

        tb.addLayout(right, 2)

        root.addWidget(toolbar)


# -----------------------------
# PROCESSING (Filters + Run)
# -----------------------------
class ProcessingPanel(QWidget):
    """
    Полностью другой вид:
    - слева карточка "Фильтры"
    - справа карточка "Быстрые опции"
    - внизу крупная кнопка "Обработать"
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_app = parent
        self.initUI()

    def initUI(self):
        self.setStyleSheet(_base_stylesheet())

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(10)

        row = QHBoxLayout()
        row.setSpacing(10)

        # Card 1: filters
        card_filters = _card("Обработка сигнала", "Фильтрация + анти-артефакты")
        gf = QGridLayout()
        gf.setHorizontalSpacing(12)
        gf.setVerticalSpacing(10)

        # Inputs
        self.low_freq_spin = QDoubleSpinBox()
        self.low_freq_spin.setRange(0.1, 100.0)
        self.low_freq_spin.setSingleStep(0.5)
        self.low_freq_spin.setValue(1.0)
        _apply_spin_clean(self.low_freq_spin)

        self.high_freq_spin = QDoubleSpinBox()
        self.high_freq_spin.setRange(0.1, 100.0)
        self.high_freq_spin.setSingleStep(0.5)
        self.high_freq_spin.setValue(40.0)
        _apply_spin_clean(self.high_freq_spin)

        self.notch_freq_spin = QSpinBox()
        self.notch_freq_spin.setRange(0, 60)
        self.notch_freq_spin.setSingleStep(1)
        self.notch_freq_spin.setValue(50)
        _apply_spin_clean(self.notch_freq_spin)

        self.threshold_spin = QDoubleSpinBox()
        self.threshold_spin.setRange(1.0, 10.0)
        self.threshold_spin.setSingleStep(0.5)
        self.threshold_spin.setValue(3.0)
        _apply_spin_clean(self.threshold_spin)

        # Labels above inputs (modern)
        def head(text):
            l = QLabel(text)
            l.setObjectName("muted")
            return l

        gf.addWidget(head("HPF (низкая, Гц)"), 0, 0)
        gf.addWidget(self.low_freq_spin, 1, 0)

        gf.addWidget(head("LPF (высокая, Гц)"), 0, 1)
        gf.addWidget(self.high_freq_spin, 1, 1)

        gf.addWidget(head("Notch (Гц)"), 0, 2)
        gf.addWidget(self.notch_freq_spin, 1, 2)

        gf.addWidget(head("Порог артефактов (σ)"), 0, 3)
        gf.addWidget(self.threshold_spin, 1, 3)

        # Card 2: options
        card_opts = _card("Опции", "Быстрые переключатели препроцессинга")
        go = QVBoxLayout()
        go.setSpacing(8)

        self.detrend_check = QCheckBox("Детренд (убрать линейный тренд)")
        self.detrend_check.setChecked(True)

        self.remove_dc_check = QCheckBox("Удалить DC offset (смещение)")
        self.remove_dc_check.setChecked(True)

        self.artifacts_check = QCheckBox("Удалять артефакты (по порогу)")
        self.artifacts_check.setChecked(True)

        go.addWidget(self.detrend_check)
        go.addWidget(self.remove_dc_check)
        go.addWidget(self.artifacts_check)

        hint = QLabel("Совет: сначала HPF/LPF, потом Detrend/DC, затем артефакты.")
        hint.setObjectName("muted")
        hint.setWordWrap(True)
        go.addWidget(hint)

        card_filters.setLayout(gf)
        card_opts.setLayout(go)

        row.addWidget(card_filters, 3)
        row.addWidget(card_opts, 2)

        outer.addLayout(row)

        # Primary action bar
        action_bar = QFrame()
        action_bar.setStyleSheet("""
            QFrame{
                background: #0b1220;
                border: 1px solid #243244;
                border-radius: 14px;
                padding: 10px;
            }
        """)
        ab = QHBoxLayout(action_bar)
        ab.setContentsMargins(12, 10, 12, 10)
        ab.setSpacing(12)

        left_info = QLabel("Готово? Запусти обработку — справа обновится отфильтрованный сигнал.")
        left_info.setObjectName("muted")
        left_info.setWordWrap(True)

        self.btn_process = QPushButton("ОБРАБОТАТЬ")
        self.btn_process.setObjectName("primary")
        self.btn_process.setMinimumHeight(44)
        self.btn_process.setMinimumWidth(220)
        self.btn_process.setEnabled(False)

        ab.addWidget(left_info, 1)
        ab.addWidget(self.btn_process, 0, Qt.AlignRight)

        outer.addWidget(action_bar)


# -----------------------------
# ANALYSIS (Rhythms)
# -----------------------------
class AnalysisPanel(QWidget):
    """
    Новый расклад:
    - карточка выбора канала/ритма
    - ниже — кнопки действий сгруппированы и выровнены
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_app = parent
        self.initUI()

    def initUI(self):
        self.setStyleSheet(_base_stylesheet())

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(10)

        top = QHBoxLayout()
        top.setSpacing(10)

        card_sel = _card("Анализ ритмов", "PSD, полосы δ/θ/α/β/γ и рекомендации")
        g = QGridLayout()
        g.setHorizontalSpacing(12)
        g.setVerticalSpacing(10)

        def head(text):
            l = QLabel(text)
            l.setObjectName("muted")
            return l

        g.addWidget(head("Канал для анализа"), 0, 0)
        self.analysis_channel_combo = QComboBox()
        self.analysis_channel_combo.setMinimumWidth(220)
        g.addWidget(self.analysis_channel_combo, 1, 0)

        g.addWidget(head("Режим анализа"), 0, 1)
        self.rhythm_combo = QComboBox()
        self.rhythm_combo.addItems(["Все ритмы", "дельта", "тета", "альфа", "бета", "гамма"])
        self.rhythm_combo.setMinimumWidth(220)
        g.addWidget(self.rhythm_combo, 1, 1)

        note = QLabel("Если выбран конкретный ритм — будет рассчитана его мощность и пик частоты.")
        note.setObjectName("muted")
        note.setWordWrap(True)
        g.addWidget(note, 2, 0, 1, 2)

        card_sel.setLayout(g)
        top.addWidget(card_sel, 3)

        # Action card (buttons)
        card_actions = _card("Действия", "Запуск анализа, отчёт, валидация")
        vb = QVBoxLayout()
        vb.setSpacing(10)


        self.btn_analyze = QPushButton("АНАЛИЗ  ВСЕХ РИТМОВ")
        self.btn_analyze.setObjectName("purple")
        self.btn_analyze.setMinimumHeight(44)
        self.btn_analyze.setEnabled(False)

        self.btn_analyze_single = QPushButton("АНАЛИЗИРОВАТЬ  ВЫБРАННЫЙ РИТМ")
        self.btn_analyze_single.setObjectName("success")
        self.btn_analyze_single.setMinimumHeight(44)
        self.btn_analyze_single.setEnabled(False)

        row2 = QHBoxLayout()
        row2.setSpacing(10)

        self.btn_save_report = QPushButton("СОХРАНИТЬ ОТЧЁТ")
        self.btn_save_report.setObjectName("warning")
        self.btn_save_report.setMinimumHeight(42)
        self.btn_save_report.setEnabled(False)

        self.btn_validate = QPushButton("ВАЛИДАЦИЯ (MNE)")
        self.btn_validate.setObjectName("cyan")
        self.btn_validate.setMinimumHeight(42)
        self.btn_validate.setEnabled(False)

        row2.addWidget(self.btn_save_report)
        row2.addWidget(self.btn_validate)

        vb.addWidget(self.btn_analyze)
        vb.addWidget(self.btn_analyze_single)
        vb.addLayout(row2)

        hint = QLabel("Рекомендация: сначала обработай сигнал, потом запускай анализ.")
        hint.setObjectName("muted")
        hint.setWordWrap(True)
        vb.addWidget(hint)

        card_actions.setLayout(vb)
        top.addWidget(card_actions, 2)

        outer.addLayout(top)


# -----------------------------
# RECORDING PANELS
# -----------------------------
class RecordingSettingsPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_app = parent
        self.initUI()

    def initUI(self):
        self.setStyleSheet(_base_stylesheet())

        settings_group = _card("Настройки записи", "Источник данных + порт + частота")
        settings_layout = QGridLayout()
        settings_layout.setHorizontalSpacing(12)
        settings_layout.setVerticalSpacing(10)

        def head(text):
            l = QLabel(text)
            l.setObjectName("muted")
            return l

        settings_layout.addWidget(head("Источник данных"), 0, 0)
        self.data_source_combo = QComboBox()
        self.data_source_combo.addItems(["Serial порт (Arduino/EEG)"])
        settings_layout.addWidget(self.data_source_combo, 1, 0, 1, 2)

        settings_layout.addWidget(head("COM порт"), 2, 0)
        self.com_port_combo = QComboBox()
        settings_layout.addWidget(self.com_port_combo, 3, 0)

        self.btn_refresh_ports = QPushButton("Обновить")
        self.btn_refresh_ports.setObjectName("primary")
        self.btn_refresh_ports.setFixedHeight(36)
        settings_layout.addWidget(self.btn_refresh_ports, 3, 1)

        settings_layout.addWidget(head("Baudrate"), 2, 2)
        self.baudrate_combo = QComboBox()
        self.baudrate_combo.addItems(["9600", "19200", "38400", "57600", "115200", "230400"])
        self.baudrate_combo.setCurrentText("115200")
        settings_layout.addWidget(self.baudrate_combo, 3, 2)

        settings_layout.addWidget(head("Частота дискретизации (Гц)"), 4, 0)
        self.recording_sampling_spin = QSpinBox()
        self.recording_sampling_spin.setRange(1, 2000)
        self.recording_sampling_spin.setValue(250)
        _apply_spin_clean(self.recording_sampling_spin)
        settings_layout.addWidget(self.recording_sampling_spin, 5, 0)

        settings_group.setLayout(settings_layout)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(settings_group)


class RecordingControlPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_app = parent
        self.initUI()

    def initUI(self):
        self.setStyleSheet(_base_stylesheet())

        control_group = _card("Управление записью", "Старт/стоп + сохранить + отправить в анализ")
        control_layout = QHBoxLayout()
        control_layout.setSpacing(10)

        self.btn_start_recording = QPushButton("НАЧАТЬ")
        self.btn_start_recording.setObjectName("danger")
        self.btn_start_recording.setMinimumHeight(46)
        self.btn_start_recording.setMinimumWidth(170)
        control_layout.addWidget(self.btn_start_recording)

        self.btn_stop_recording = QPushButton("ОСТАНОВИТЬ")
        self.btn_stop_recording.setObjectName("primary")
        self.btn_stop_recording.setMinimumHeight(46)
        self.btn_stop_recording.setMinimumWidth(170)
        self.btn_stop_recording.setEnabled(False)
        control_layout.addWidget(self.btn_stop_recording)

        self.btn_save_recorded = QPushButton("СОХРАНИТЬ")
        self.btn_save_recorded.setObjectName("warning")
        self.btn_save_recorded.setMinimumHeight(46)
        self.btn_save_recorded.setEnabled(False)
        control_layout.addWidget(self.btn_save_recorded)

        self.btn_use_recorded = QPushButton("ОТПРАВИТЬ В АНАЛИЗ")
        self.btn_use_recorded.setObjectName("success")
        self.btn_use_recorded.setMinimumHeight(46)
        self.btn_use_recorded.setEnabled(False)
        control_layout.addWidget(self.btn_use_recorded)

        control_group.setLayout(control_layout)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(control_group)


class InfoPanel(QWidget):
    def __init__(self, performance_monitor, parent=None):
        super().__init__(parent)
        self.performance_monitor = performance_monitor
        self.initUI()

    def initUI(self):
        self.setStyleSheet(_base_stylesheet())

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.info_tabs = QTabWidget()
        self.info_tabs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.info_text = QTextEdit()
        self.info_text.setMinimumHeight(520)
        self.info_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.info_text.setPlaceholderText("Системные сообщения, статус загрузки и параметры данных…")
        self.info_text.setStyleSheet("""
            QTextEdit {
                font-size: 13px;
                line-height: 1.6;
                color: #e5e7eb;
                background-color: #0b1220;
                border: 1px solid #243244;
                border-radius: 0px;
                padding: 14px;
                selection-background-color: #3b82f6;
                selection-color: white;
            }
        """)

        self.recommendations_text = QTextEdit()
        self.recommendations_text.setPlaceholderText("Рекомендации по ритмам и состоянию будут здесь…")
        self.recommendations_text.setStyleSheet("""
            QTextEdit {
                font-size: 13px;
                line-height: 1.6;
                color: #e5e7eb;
                background-color: #0b1220;
                border: 1px solid #243244;
                border-radius: 0px;
                padding: 14px;
                selection-background-color: #3b82f6;
                selection-color: white;
            }
        """)

        self.performance_text = QTextEdit()
        self.performance_text.setReadOnly(True)
        self.performance_text.setStyleSheet("""
            QTextEdit {
                font-size: 13px;
                line-height: 1.6;
                color: #e5e7eb;
                background-color: #0b1220;
                border: 1px solid #243244;
                border-radius: 0px;
                padding: 14px;
                selection-background-color: #3b82f6;
                selection-color: white;
            }
        """)

        self.performance_widget = PerformanceWidget(self.performance_monitor)

        self.info_tabs.addTab(self.info_text, "Инфо")
        self.info_tabs.addTab(self.recommendations_text, "Рекомендации")
        self.info_tabs.addTab(self.performance_widget, "Мониторинг")
        self.info_tabs.addTab(self.performance_text, "Отчет")

        layout.addWidget(self.info_tabs)


class RecordingStatusPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setStyleSheet(_base_stylesheet())

        status_group = _card("Статус записи", "Состояние процесса и прогресс")
        status_layout = QVBoxLayout()
        status_layout.setSpacing(8)

        self.recording_status = QLabel("Готов к записи")
        self.recording_status.setStyleSheet("font-size: 13px; font-weight: 700; padding: 4px;")
        status_layout.addWidget(self.recording_status)

        self.recording_progress = QProgressBar()
        self.recording_progress.setVisible(False)
        self.recording_progress.setFixedHeight(14)
        self.recording_progress.setStyleSheet("""
            QProgressBar {
                border: 1px solid #243244;
                border-radius: 7px;
                background: #0b1220;
                text-align: center;
                color: #9ca3af;
            }
            QProgressBar::chunk {
                border-radius: 7px;
                background: #3b82f6;
            }
        """)
        status_layout.addWidget(self.recording_progress)

        status_group.setLayout(status_layout)

        info_group = _card("Лог записи", "Техническая информация (COM, частота, ошибки)")
        info_layout = QVBoxLayout()

        self.recording_info = QTextEdit()
        self.recording_info.setMaximumHeight(140)
        self.recording_info.setStyleSheet("""
            QTextEdit {
                font-size: 12px;
                line-height: 1.5;
                color: #e5e7eb;
                background-color: #0b1220;
                border: 1px solid #243244;
                border-radius: 12px;
                padding: 12px;
            }
        """)
        info_layout.addWidget(self.recording_info)

        info_group.setLayout(info_layout)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        layout.addWidget(status_group)
        layout.addWidget(info_group)