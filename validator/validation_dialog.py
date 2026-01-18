"""
Диалоговое окно для отображения результатов валидации
"""
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTextEdit,
                             QPushButton, QTabWidget, QWidget, QTableWidget,
                             QTableWidgetItem, QLabel, QProgressBar, QHeaderView, QAbstractItemView)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class ValidationThread(QThread):
    """Поток для валидации с MNE"""
    progress_signal = pyqtSignal(int)
    result_signal = pyqtSignal(dict)
    error_signal = pyqtSignal(str)

    def __init__(self, validator, data, sampling_rate, channel_names, our_filtered):
        super().__init__()
        self.validator = validator
        self.data = data
        self.sampling_rate = sampling_rate
        self.channel_names = channel_names
        self.our_filtered = our_filtered

    def run(self):
        try:
            self.progress_signal.emit(20)

            # Получаем результаты MNE
            mne_result = self.validator.compare_with_mne(
                self.data,
                self.sampling_rate,
                self.channel_names
            )

            if not mne_result['available']:
                self.error_signal.emit(mne_result['message'])
                return

            self.progress_signal.emit(50)

            # Сравниваем фильтрацию
            comparison = self.validator.compare_filtering(
                self.our_filtered,
                mne_result['mne_data']
            )

            self.progress_signal.emit(80)

            # Генерируем отчёт
            report = self.validator.generate_comparison_report(
                self.data,
                mne_result['mne_data'],
                self.our_filtered,
                mne_result['mne_data']
            )

            self.progress_signal.emit(100)

            result = {
                'comparison': comparison,
                'report': report,
                'mne_data': mne_result['mne_data'],
                'our_data': self.our_filtered
            }

            self.result_signal.emit(result)

        except Exception as e:
            self.error_signal.emit(f"Ошибка валидации: {str(e)}")


class ValidationDialog(QDialog):
    """Диалог для отображения результатов валидации"""

    def _apply_dark_matplotlib(self):
        # Тема под твой UI (#0b1220 / #243244 / #e5e7eb)
        self.figure.patch.set_facecolor("#0b1220")  # фон всей фигуры

        for ax in self.figure.get_axes():
            ax.set_facecolor("#0b1220")

            # оси/подписи
            ax.tick_params(colors="#e5e7eb")
            ax.xaxis.label.set_color("#e5e7eb")
            ax.yaxis.label.set_color("#e5e7eb")
            ax.title.set_color("#e5e7eb")

            # рамки
            for s in ax.spines.values():
                s.set_color("#475569")

            # сетка
            ax.grid(True, color="#334155", alpha=0.45, linewidth=0.8)

            # легенда
            leg = ax.get_legend()
            if leg:
                leg.get_frame().set_facecolor("#0b1220")
                leg.get_frame().set_edgecolor("#475569")
                leg.get_frame().set_alpha(0.92)
                for t in leg.get_texts():
                    t.set_color("#e5e7eb")

    def build_pretty_report(self, result: dict) -> str:
        comp = result.get("comparison", {})
        channels = comp.get("channels", [])

        if not channels:
            return "Нет данных сравнения."

        # агрегаты
        corr = [c.get("correlation", 0) for c in channels]
        r2 = [c.get("r_squared", 0) for c in channels]
        rmse = [c.get("rmse", 0) for c in channels]
        mae = [c.get("mae", 0) for c in channels]
        nrmse = [c.get("nrmse", 0) for c in channels]

        def avg(x):
            return float(np.mean(x)) if len(x) else 0.0

        def verdict(avg_corr, avg_nrmse):
            # грубо и понятно
            if avg_corr >= 0.98 and avg_nrmse <= 5:
                return "ОТЛИЧНО: наш фильтр практически совпадает с MNE."
            if avg_corr >= 0.95 and avg_nrmse <= 10:
                return "ХОРОШО: расхождения небольшие, результат валиден."
            if avg_corr >= 0.90:
                return "СРЕДНЕ: заметные отличия, проверь параметры фильтра."
            return "ПЛОХО: сильные отличия, вероятно ошибка в фильтрации/данных."

        avg_corr = avg(corr)
        avg_nrmse = avg(nrmse)

        lines = []
        lines.append("VALIDATION REPORT (MNE-Python)")
        lines.append("=" * 34)
        lines.append(f"Каналов (показано): {len(channels)}")
        lines.append(f"Fs: {self.sampling_rate} Hz")
        lines.append("")
        lines.append("СВОДКА")
        lines.append("-" * 34)
        lines.append(f"Средняя корреляция: {avg_corr:.4f}")
        lines.append(f"Средний R²:         {avg(r2):.4f}")
        lines.append(f"Средний RMSE:       {avg(rmse):.6f}")
        lines.append(f"Средний MAE:        {avg(mae):.6f}")
        lines.append(f"Средний NRMSE:      {avg_nrmse:.2f} %")
        lines.append("")
        lines.append("ИТОГ")
        lines.append("-" * 34)
        lines.append(verdict(avg_corr, avg_nrmse))
        lines.append("")
        lines.append("ДЕТАЛИ ПО КАНАЛАМ")
        lines.append("-" * 34)

        # табличный вид текстом
        header = f"{'Канал':<10}{'Corr':>10}{'R2':>10}{'RMSE':>12}{'MAE':>12}{'NRMSE%':>10}"
        lines.append(header)
        lines.append("-" * len(header))

        for c in channels:
            idx = c.get("channel", "?")
            name = self.channel_names[idx] if isinstance(idx, int) and idx < len(self.channel_names) else f"Ch {idx}"
            lines.append(
                f"{name:<10}"
                f"{c.get('correlation', 0):>10.4f}"
                f"{c.get('r_squared', 0):>10.4f}"
                f"{c.get('rmse', 0):>12.6f}"
                f"{c.get('mae', 0):>12.6f}"
                f"{c.get('nrmse', 0):>10.2f}"
            )

        lines.append("")
        lines.append("РЕКОМЕНДАЦИИ")
        lines.append("-" * 34)
        lines.append("• Если корреляция низкая — проверь HPF/LPF, порядок операций и notch.")
        lines.append("• Если RMSE/NRMSE высокие — проверь масштабирование (мкВ), DC offset и detrend.")
        lines.append("• Если графики расходятся фазой — проверь filtfilt vs lfilter и порядок фильтрации.")
        lines.append("")
        lines.append("Примечание: это сравнение с MNE не является медицинским заключением.")

        return "\n".join(lines)

    def __init__(self, validator, data, sampling_rate, channel_names, our_filtered, parent=None):
        super().__init__(parent)
        self.validator = validator
        self.data = data
        self.sampling_rate = sampling_rate
        self.channel_names = channel_names
        self.our_filtered = our_filtered
        self.validation_result = None

        self.initUI()
        self.start_validation()

    def initUI(self):
        self.setWindowTitle("Валидация результатов с MNE-Python")
        self.setGeometry(100, 100, 1000, 700)

        layout = QVBoxLayout()

        # Прогресс бар
        self.progress_bar = QProgressBar()
        self.progress_label = QLabel("Инициализация валидации...")
        layout.addWidget(self.progress_label)
        layout.addWidget(self.progress_bar)

        # Табы
        self.tabs = QTabWidget()

        # Таб с отчётом
        self.report_tab = QWidget()
        report_layout = QVBoxLayout()
        self.report_text = QTextEdit()
        self.report_text.setReadOnly(True)
        self.report_text.setFont(QFont("Courier New", 10))
        report_layout.addWidget(self.report_text)
        self.report_tab.setLayout(report_layout)

        # Таб с таблицей
        self.table_tab = QWidget()
        table_layout = QVBoxLayout()
        self.comparison_table = QTableWidget()

        # Поведение
        self.comparison_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.comparison_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.comparison_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.comparison_table.setAlternatingRowColors(True)
        self.comparison_table.setShowGrid(False)
        self.comparison_table.verticalHeader().setVisible(False)

        # Хедер
        hh = self.comparison_table.horizontalHeader()
        hh.setHighlightSections(False)
        hh.setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        hh.setStretchLastSection(True)
        hh.setSectionResizeMode(QHeaderView.ResizeToContents)  # авто по контенту

        # Чуть воздуха
        self.comparison_table.setWordWrap(False)
        self.comparison_table.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.comparison_table.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)

        # Стиль под твою тему
        self.comparison_table.setStyleSheet("""
        QTableWidget {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                        stop:0 #0b1220, stop:1 #0f172a);
            border: 1px solid rgba(36,50,68,0.9);
            border-radius: 14px;              /* круглая карточка */
            padding: 6px;
            color: #E5E7EB;
            font-size: 13px;
            selection-background-color: rgba(59,130,246,0.22);
            gridline-color: rgba(36,50,68,0.45);
        }

        /* ВНУТРИ — прямоугольники */
        QTableWidget::item {
            padding: 10px 12px;
            border-radius: 0px;               /* <- убрали скругления */
        }

        QTableWidget::item:selected {
            background: rgba(59,130,246,0.22);
            color: #E5E7EB;
        }

        /* Header */
        QHeaderView {
            background: transparent;
        }

        QHeaderView::section {
            background: rgba(255,255,255,0.06);
            color: #E5E7EB;
            border: none;

            border-bottom: 1px solid rgba(36,50,68,0.9);
            border-right: 1px solid rgba(36,50,68,0.55);

            padding: 10px 12px;
            font-weight: 900;
            font-size: 13px;

            border-radius: 0px;               /* по умолчанию прямоугольная */
        }

        /* Скругление у шапки только по краям карточки */
        QHeaderView::section:first {
            border-left: 1px solid rgba(36,50,68,0.55);
            border-top-left-radius: 12px;
        }
        QHeaderView::section:last {
            border-top-right-radius: 12px;
        }

        /* Уголок слева сверху */
        QTableCornerButton::section {
            background: rgba(255,255,255,0.06);
            border: none;
            border-bottom: 1px solid rgba(36,50,68,0.9);
            border-right: 1px solid rgba(36,50,68,0.55);
            border-top-left-radius: 12px;
        }

        /* Полосатость строк */
        QTableWidget {
            alternate-background-color: rgba(255,255,255,0.03);
        }

        /* Скролл */
        QScrollBar:vertical {
            width: 14px;
            background: transparent;
            margin: 6px 4px 6px 4px;
        }
        QScrollBar::handle:vertical {
            background: rgba(229,231,235,0.26);
            border-radius: 7px;
            border: 2px solid transparent;
            background-clip: padding;
            min-height: 28px;
        }
        QScrollBar::handle:vertical:hover { background: rgba(229,231,235,0.38); }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }

        QScrollBar:horizontal {
            height: 12px;
            background: transparent;
            margin: 4px 6px 4px 6px;
        }
        QScrollBar::handle:horizontal {
            background: rgba(229,231,235,0.26);
            border-radius: 6px;
            border: 2px solid transparent;
            background-clip: padding;
            min-width: 28px;
        }
        QScrollBar::handle:horizontal:hover { background: rgba(229,231,235,0.38); }
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0px; }
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal { background: transparent; }
        """)

        table_layout.addWidget(self.comparison_table)
        self.table_tab.setLayout(table_layout)

        # Таб с графиками
        self.plot_tab = QWidget()
        plot_layout = QVBoxLayout()
        self.figure = Figure(figsize=(10, 8))
        self.canvas = FigureCanvas(self.figure)
        plot_layout.addWidget(self.canvas)
        self.plot_tab.setLayout(plot_layout)

        self.tabs.addTab(self.report_tab, " Отчёт")
        self.tabs.addTab(self.table_tab, " Таблица")
        self.tabs.addTab(self.plot_tab, " Графики")

        layout.addWidget(self.tabs)

        # Кнопки
        buttons_layout = QHBoxLayout()

        self.btn_save = QPushButton(" Сохранить отчёт")
        self.btn_save.clicked.connect(self.save_report)
        self.btn_save.setEnabled(False)
        buttons_layout.addWidget(self.btn_save)

        self.btn_close = QPushButton("Закрыть")
        self.btn_close.clicked.connect(self.accept)
        buttons_layout.addWidget(self.btn_close)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def start_validation(self):
        """Запуск валидации"""
        self.validation_thread = ValidationThread(
            self.validator,
            self.data,
            self.sampling_rate,
            self.channel_names,
            self.our_filtered
        )

        self.validation_thread.progress_signal.connect(self.update_progress)
        self.validation_thread.result_signal.connect(self.on_validation_complete)
        self.validation_thread.error_signal.connect(self.on_validation_error)

        self.validation_thread.start()

    def update_progress(self, value):
        """Обновление прогресса"""
        self.progress_bar.setValue(value)

        if value == 20:
            self.progress_label.setText("Обработка данных с MNE-Python...")
        elif value == 50:
            self.progress_label.setText("Сравнение результатов...")
        elif value == 80:
            self.progress_label.setText("Генерация отчёта...")
        elif value == 100:
            self.progress_label.setText("Валидация завершена!")

    def on_validation_complete(self, result):
        """Обработка результатов валидации"""
        self.validation_result = result

        # Отображаем отчёт
        pretty = self.build_pretty_report(result)
        self.report_text.setPlainText(pretty)

        # Заполняем таблицу
        self.fill_comparison_table(result['comparison'])

        # Строим графики
        self.plot_comparison(result)

        # Активируем кнопку сохранения
        self.btn_save.setEnabled(True)

        # Скрываем прогресс бар
        self.progress_bar.hide()
        self.progress_label.hide()

    def on_validation_error(self, error_msg):
        """Обработка ошибки валидации"""
        self.progress_label.setText(f"Ошибка: {error_msg}")
        self.progress_bar.hide()
        self.report_text.setPlainText(f"ОШИБКА ВАЛИДАЦИИ:\n\n{error_msg}")

    def fill_comparison_table(self, comparison):
        channels = comparison['channels']

        self.comparison_table.setRowCount(len(channels))
        self.comparison_table.setColumnCount(6)
        self.comparison_table.setHorizontalHeaderLabels([
            'Канал', 'Corr', 'R²', 'RMSE', 'MAE', 'NRMSE (%)'
        ])

        for i, ch in enumerate(channels):
            # Канал
            item0 = QTableWidgetItem(f"Канал {ch['channel']}")
            item0.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.comparison_table.setItem(i, 0, item0)

            # Числа
            def num_item(val, fmt):
                it = QTableWidgetItem(format(val, fmt))
                it.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                return it

            self.comparison_table.setItem(i, 1, num_item(ch['correlation'], ".4f"))
            self.comparison_table.setItem(i, 2, num_item(ch['r_squared'], ".4f"))
            self.comparison_table.setItem(i, 3, num_item(ch['rmse'], ".6f"))
            self.comparison_table.setItem(i, 4, num_item(ch['mae'], ".6f"))
            self.comparison_table.setItem(i, 5, num_item(ch['nrmse'], ".2f"))

        # Чуть компактнее по высоте
        self.comparison_table.resizeColumnsToContents()
        self.comparison_table.resizeRowsToContents()

        # Если хочется, чтобы таблица занимала ширину красиво:
        hh = self.comparison_table.horizontalHeader()
        hh.setSectionResizeMode(0, QHeaderView.Stretch)  # "Канал" растягиваем
        for col in range(1, 6):
            hh.setSectionResizeMode(col, QHeaderView.ResizeToContents)

    def plot_comparison(self, result):
        """Построение графиков сравнения (тёмная тема)"""
        self.figure.clear()

        our_data = result['our_data']
        mne_data = result['mne_data']

        n_channels = min(4, our_data.shape[0])
        time_axis = np.arange(our_data.shape[1]) / self.sampling_rate

        for i in range(n_channels):
            ax = self.figure.add_subplot(n_channels, 1, i + 1)

            ax.plot(time_axis, our_data[i],
                    label='Наш результат', alpha=0.95, linewidth=1.2, color="#22c55e")
            ax.plot(time_axis, mne_data[i],
                    label='MNE-Python', alpha=0.9, linewidth=1.1, linestyle='--', color="#60a5fa")

            ax.set_ylabel(f'{self.channel_names[i] if i < len(self.channel_names) else f"Канал {i}"}')

            if i == 0:
                ax.set_title('Сравнение фильтрованных сигналов')
            if i == n_channels - 1:
                ax.set_xlabel('Время (сек)')

            ax.legend(loc='upper right')

        # важное: сначала tight_layout, потом theme
        self.figure.tight_layout()
        self._apply_dark_matplotlib()
        self.canvas.draw()

    def save_report(self):
        """Сохранение отчёта"""
        from PyQt5.QtWidgets import QFileDialog

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить отчёт валидации",
            "validation_report.txt",
            "Text Files (*.txt)"
        )

        if file_path and self.validation_result:
            txt = self.build_pretty_report(self.validation_result)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(txt)

            self.progress_label.setText(f"Отчёт сохранён: {file_path}")
            self.progress_label.show()
