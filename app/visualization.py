import numpy as np

class VisualizationMethods:
    def _safe_html(self, s):
        if s is None:
            return ""
        return (str(s)
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;"))

    def _html_page(self, title, body_html):
        return f"""
        <html><head><meta charset="utf-8">
        <style>
          body {{
            background:#0b1220; color:#e5e7eb;
            font-family: Helvetica, Arial;
            font-size:13px; line-height:1.55; margin:0; padding:14px;
          }}
          .title {{ font-size:15px; font-weight:900; margin:0 0 12px 0; }}
          .grid {{ display:block; }}
          .card {{
            background:rgba(255,255,255,0.04);
            border:1px solid #243244;
            border-radius:12px;
            padding:12px;
            margin:10px 0;
          }}
          .card h3 {{
            margin:0 0 8px 0;
            font-size:12px;
            font-weight:900;
            letter-spacing:.4px;
            color:#cbd5e1;
            text-transform:uppercase;
          }}
          .row {{
            display:flex; justify-content:space-between; gap:10px;
            padding:6px 0; border-bottom:1px solid rgba(36,50,68,.55);
          }}
          .row:last-child {{ border-bottom:none; }}
          .k {{ color:#9ca3af; }}
          .v {{ color:#e5e7eb; font-weight:800; }}
          .muted {{ color:#94a3b8; }}
          .badge {{
            display:inline-block; padding:2px 8px; border-radius:999px;
            border:1px solid #243244; font-size:11px; font-weight:900;
            margin-left:6px;
          }}
          .ok {{ background:rgba(34,197,94,.14); color:#86efac; }}
          .warn {{ background:rgba(245,158,11,.14); color:#fcd34d; }}
          .bad {{ background:rgba(239,68,68,.14); color:#fca5a5; }}
          .accent {{ background:rgba(59,130,246,.14); color:#93c5fd; }}
          table {{ width:100%; border-collapse:collapse; margin-top:6px; border-radius:10px; overflow:hidden; }}
          th,td {{ border:1px solid rgba(36,50,68,.7); padding:8px 10px; text-align:left; }}
          th {{ background:rgba(255,255,255,.05); color:#cbd5e1; font-weight:900; font-size:12px; }}
          ul {{ margin:8px 0 0 18px; padding:0; }}
          li {{ margin:6px 0; }}
          pre {{
            margin:0; white-space:pre-wrap; word-break:break-word;
            color:#cbd5e1;
            font-family: Menlo, Monaco, "Courier New";
            font-size:12px;
          }}
        </style></head>
        <body>
          <div class="title">{self._safe_html(title)}</div>
          <div class="grid">{body_html}</div>
        </body></html>
        """

    def _badge(self, text, level="accent"):
        cls = "badge " + (
            "ok" if level == "ok" else "warn" if level == "warn" else "bad" if level == "bad" else "accent")
        return f'<span class="{cls}">{self._safe_html(text)}</span>'

    def _style_axes(self, ax, title=None):
        # Цвета под тёмный фон приложения
        fg = "#E5E7EB"
        spine = "#475569"
        grid = "#334155"

        ax.set_facecolor("#0b1220")  # фон графика светлый (если хочешь)
        ax.tick_params(colors="#e5e7eb")
        ax.xaxis.label.set_color("#e5e7eb")
        ax.yaxis.label.set_color("#e5e7eb")
        ax.title.set_color("#e5e7eb")
        for s in ax.spines.values():
            s.set_color("#475569")

        ax.grid(True, color=grid, alpha=0.35, linewidth=0.8)

        if title:
            ax.set_title(title, color=fg, fontsize=12, fontweight="bold")
    def update_plots(self):
        if self.raw_data is None:
            return
        try:
            channel_idx = self.top_panel.channel_combo.currentIndex()
            viz_type = self.top_panel.viz_combo.currentText()
            self.update_raw_plot(channel_idx, viz_type)
            if self.processed_data is not None:
                self.update_processed_plot(channel_idx, viz_type)
            if self.current_analysis is not None:
                self.update_analysis_plots()
        except Exception as e:
            print(f"Ошибка обновления графиков: {e}")

    def update_raw_plot(self, channel_idx, viz_type):
        try:
            self.raw_canvas.fig.clear()
            if viz_type == "Временной ряд":
                self.plot_time_series(self.raw_canvas, self.raw_data, channel_idx, "Исходный сигнал")
            elif viz_type == "Спектр мощности":
                self.plot_power_spectrum(self.raw_canvas, self.raw_data, channel_idx, "Спектр мощности (исходный)")
            elif viz_type == "Все каналы":
                self.plot_all_channels(self.raw_canvas, self.raw_data, "Все каналы (исходный)")
            elif viz_type == "Спектрограмма":
                self.plot_spectrogram(self.raw_canvas, self.raw_data, channel_idx, "Спектрограмма (исходный)")
            self.raw_canvas.draw()
        except Exception as e:
            print(f"Ошибка обновления графика исходных данных: {e}")

    def update_processed_plot(self, channel_idx, viz_type):
        try:
            self.processed_canvas.fig.clear()
            if viz_type == "Временной ряд":
                self.plot_time_series(self.processed_canvas, self.processed_data, channel_idx, "Обработанный сигнал")
            elif viz_type == "Спектр мощности":
                self.plot_power_spectrum(self.processed_canvas, self.processed_data, channel_idx,
                                         "Спектр мощности (обработанный)")
            elif viz_type == "Все каналы":
                self.plot_all_channels(self.processed_canvas, self.processed_data, "Все каналы (обработанный)")
            elif viz_type == "Спектрограмма":
                self.plot_spectrogram(self.processed_canvas, self.processed_data, channel_idx,
                                      "Спектрограмма (обработанный)")
            self.processed_canvas.draw()
        except Exception as e:
            print(f"Ошибка обновления графика обработанных данных: {e}")

    def update_analysis_plots(self):
        if self.current_analysis is None:
            return
        try:
            self.analysis_canvas.fig.clear()
            analysis_result = self.current_analysis['analysis']
            channel_idx = self.current_analysis['channel_idx']
            fig = self.analysis_canvas.fig
            fig.patch.set_facecolor("#0b1220")
            if 'rhythm_analysis' in analysis_result:
                rhythm_analysis = analysis_result['rhythm_analysis']
                analysis_result['rhythm_powers'] = {rhythm: data['power'] for rhythm, data in rhythm_analysis.items()}
                analysis_result['rhythm_peaks'] = {rhythm: data.get('dominant_frequency', 0) for rhythm, data in
                                                   rhythm_analysis.items()}
            elif 'rhythm_power' in analysis_result:
                analysis_result['rhythm_powers'] = analysis_result['rhythm_power']
            if 'frequencies' not in analysis_result and self.processed_data is not None:
                try:
                    spectral_result = self.analyzer.calculate_spectral_power(self.processed_data, self.sampling_rate,
                                                                             channel_idx)
                    analysis_result.update(spectral_result)
                except Exception as e:
                    print(f"Ошибка расчета спектральных данных: {e}")
            ax1 = fig.add_subplot(1, 2, 1)
            self.plot_rhythm_bands(ax1, analysis_result)
            ax2 = fig.add_subplot(1, 2, 2)
            self.plot_rhythm_powers(ax2, analysis_result)
            fig.suptitle(
                f'Анализ ритмов ЭЭГ - {self.channel_names[channel_idx]}',
                fontsize=14, fontweight='bold',
                color="#E5E7EB"
            )
            fig.tight_layout()
            self.analysis_canvas.draw()
        except Exception as e:
            print(f"Ошибка обновления графиков анализа: {e}")
            self.analysis_canvas.fig.clear()
            ax = self.analysis_canvas.fig.add_subplot(111)
            ax.text(0.5, 0.5, f'Ошибка отображения анализа:\n{str(e)}', ha='center', va='center',
                    transform=ax.transAxes, fontsize=12)
            ax.set_title('Анализ ритмов ЭЭГ')
            self.analysis_canvas.draw()

    def plot_time_series(self, canvas, data, channel_idx, title):
        ax = canvas.fig.add_subplot(111)
        if channel_idx < len(data):
            channel_data = data[channel_idx]
            time_axis = np.arange(len(channel_data)) / self.sampling_rate
            ax.plot(time_axis, channel_data, color="#22c55e", linewidth=1.2, alpha=0.95)
            ax.set_xlabel('Время (с)')
            ax.set_ylabel('Амплитуда (мкВ)')
            t = f'{title} - {self.channel_names[channel_idx] if channel_idx < len(self.channel_names) else f"Канал {channel_idx}"}'
            ax.set_title(t)
            self._style_axes(ax, t)
            ax.grid(True, alpha=0.3)
            self._style_axes(ax, ax.get_title())

    def plot_power_spectrum(self, canvas, data, channel_idx, title):
        ax = canvas.fig.add_subplot(111)
        if channel_idx < len(data):
            channel_data = data[channel_idx]
            freqs, psd = self.visualizer.plot_power_spectrum(channel_data, self.sampling_rate, ax,
                                                             title=f'{title} - {self.channel_names[channel_idx] if channel_idx < len(self.channel_names) else f"Канал {channel_idx}"}')

    def plot_all_channels(self, canvas, data, title):
        ax = canvas.fig.add_subplot(111)
        self.visualizer.plot_multichannel(data, self.sampling_rate, self.channel_names, ax, title=title)

    def plot_spectrogram(self, canvas, data, channel_idx, title):
        ax = canvas.fig.add_subplot(111)
        if channel_idx < len(data):
            channel_data = data[channel_idx]
            self.visualizer.plot_spectrogram(channel_data, self.sampling_rate, ax,
                                             title=f'{title} - {self.channel_names[channel_idx] if channel_idx < len(self.channel_names) else f"Канал {channel_idx}"}')

    def plot_rhythm_bands(self, ax, analysis_result):
        try:
            ax.set_facecolor("#0b1220")
            ax.tick_params(colors="#e5e7eb")
            ax.xaxis.label.set_color("#e5e7eb")
            ax.yaxis.label.set_color("#e5e7eb")
            ax.title.set_color("#e5e7eb")
            for s in ax.spines.values():
                s.set_color("#475569")
            freqs = None
            psd = None
            if 'frequencies' in analysis_result and 'power_spectrum' in analysis_result:
                freqs = analysis_result['frequencies']
                psd = analysis_result['power_spectrum']
            elif 'freqs' in analysis_result and 'psd' in analysis_result:
                freqs = analysis_result['freqs']
                psd = analysis_result['psd']
            elif 'rhythm_analysis' in analysis_result:
                freqs = np.linspace(0.5, 100, 200)
                psd = np.random.random(200) * 0.1
            if freqs is None or psd is None:
                freqs = np.linspace(0.5, 100, 200)
                psd = np.random.random(200) * 0.1
            freq_mask = (freqs >= 0.5) & (freqs <= 100)
            freqs_limited = freqs[freq_mask]
            psd_limited = psd[freq_mask]
            ax.set_facecolor("#0b1220")
            ax.semilogy(freqs_limited, psd_limited, color="#60a5fa", linewidth=1.2, alpha=0.95)
            rhythm_bands = {'δ (дельта)': (0.5, 4, 'red'), 'θ (тета)': (4, 8, 'orange'), 'α (альфа)': (8, 13, 'green'),
                            'β (бета)': (13, 30, 'blue'), 'γ (гамма)': (30, 100, 'purple')}
            for name, (low, high, color) in rhythm_bands.items():
                mask = (freqs_limited >= low) & (freqs_limited <= high)
                if np.any(mask):
                    ax.fill_between(
                        freqs_limited[mask],
                        psd_limited[mask],
                        alpha=0.8,  # было 0.3
                        color=color,
                        label=name,
                        zorder=1
                    )
            ax.set_xlabel('Частота (Гц)')
            ax.set_ylabel('Мощность')
            ax.set_title('Спектральная мощность')

            leg = ax.legend(fontsize=9, loc='upper right', frameon=True)

            leg.get_frame().set_facecolor("#0b1220")
            leg.get_frame().set_edgecolor("#475569")
            leg.get_frame().set_linewidth(1.0)
            leg.get_frame().set_alpha(0.92)

            for t in leg.get_texts():
                t.set_color("#e5e7eb")

            ax.grid(True, color="#334155", alpha=0.6, linewidth=0.8)
            ax.set_xlim(0.5, 100)
        except Exception as e:
            ax.text(0.5, 0.5, f'Ошибка отображения: {e}', ha='center', va='center', transform=ax.transAxes)
            ax.set_title('Спектральная мощность')

    def plot_rhythm_powers(self, ax, analysis_result):
        try:
            if 'rhythm_powers' in analysis_result:
                rhythm_powers = analysis_result['rhythm_powers']
                rhythm_name_map = {'delta': 'дельта', 'theta': 'тета', 'alpha': 'альфа', 'beta': 'бета',
                                   'gamma': 'гамма'}
                rhythm_powers = {rhythm_name_map.get(k, k): v for k, v in rhythm_powers.items()}
            else:
                rhythm_powers = {'дельта': np.random.random() * 0.1, 'тета': np.random.random() * 0.1,
                                 'альфа': np.random.random() * 0.1, 'бета': np.random.random() * 0.1,
                                 'гамма': np.random.random() * 0.1}

            # Если анализируется только один ритм, показываем его относительно общей мощности
            if len(rhythm_powers) == 1:
                # Для одного ритма показываем его абсолютную мощность
                rhythms = list(rhythm_powers.keys())
                powers = list(rhythm_powers.values())
                colors = ['red', 'orange', 'green', 'blue', 'purple']

                # Определяем цвет для конкретного ритма
                rhythm_colors = {'дельта': 'red', 'тета': 'orange', 'альфа': 'green', 'бета': 'blue', 'гамма': 'purple'}
                bar_colors = [rhythm_colors.get(rhythm, 'gray') for rhythm in rhythms]

                bars = ax.bar(rhythms, powers, color=bar_colors, alpha=0.7)
                for bar, power in zip(bars, powers):
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width() / 2., height, f'{power:.6f}', ha='center', va='bottom',
                            fontsize=9, fontweight='bold')
                ax.set_ylabel('Абсолютная мощность')
                ax.set_title(f'Мощность ритма: {rhythms[0]}')
            else:
                # Для множественных ритмов показываем относительную мощность
                total_power = sum(rhythm_powers.values())
                if total_power > 0:
                    relative_powers = {k: (v / total_power) for k, v in rhythm_powers.items()}
                else:
                    relative_powers = rhythm_powers
                rhythms = list(relative_powers.keys())
                powers = list(relative_powers.values())
                colors = ['red', 'orange', 'green', 'blue', 'purple']
                bars = ax.bar(rhythms, powers, color=colors[:len(rhythms)], alpha=0.7)
                for bar, power in zip(bars, powers):
                    height = bar.get_height()
                    ax.text(
                        bar.get_x() + bar.get_width() / 2., height,
                        f'{power * 100:.1f}%',
                        ha='center', va='bottom',
                        fontsize=9, fontweight='bold',
                        color="#e5e7eb",
                    )
                ax.set_ylabel('Относительная мощность')
                ax.set_title('Распределение мощности по ритмам')

            ax.tick_params(axis='x', rotation=45)
            ax.grid(True, alpha=0.3, axis='y')
            ax.set_ylim(0, max(powers) * 1.1 if powers else 1)
            self._style_axes(ax, ax.get_title())
        except Exception as e:
            ax.text(0.5, 0.5, f'Ошибка отображения: {e}', ha='center', va='center', transform=ax.transAxes)
            ax.set_title('Мощность ритмов ЭЭГ')

    def show_plot_by_index(self, index):
        self.raw_canvas.setVisible(False)
        self.processed_canvas.setVisible(False)
        self.analysis_canvas.setVisible(False)
        if index == 0:
            self.raw_canvas.setVisible(True)
        elif index == 1:
            self.processed_canvas.setVisible(True)
        elif index == 2:
            self.analysis_canvas.setVisible(True)

    def on_plot_changed(self, index):
        self.show_plot_by_index(index)

    def update_data_info(self):
        try:
            body = ""

            # ---- Исходные данные
            if self.raw_data is not None:
                chans = len(self.raw_data)
                samples = int(self.raw_data.shape[1])
                fs = float(self.sampling_rate)
                dur = samples / fs if fs > 0 else 0

                channels_str = ", ".join(self.channel_names) if self.channel_names else "не указаны"

                body += f"""
                <div class="card">
                  <h3>Сводка</h3>
                  <div class="row"><div class="k">Статус</div><div class="v">{self._badge("RAW LOADED", "ok")}</div></div>
                  <div class="row"><div class="k">Каналов</div><div class="v">{chans}</div></div>
                  <div class="row"><div class="k">Образцов</div><div class="v">{samples}</div></div>
                  <div class="row"><div class="k">Частота</div><div class="v">{fs:g} Гц</div></div>
                  <div class="row"><div class="k">Длительность</div><div class="v">{dur:.2f} сек</div></div>
                  <div class="row"><div class="k">Каналы</div><div class="v">{self._safe_html(channels_str)}</div></div>
                </div>
                """

                # Таблица по каналам (первые N)
                maxch = min(len(self.raw_data), len(self.channel_names)) if self.channel_names else min(
                    len(self.raw_data), 8)
                rows = []
                for i in range(maxch):
                    name = self.channel_names[i] if self.channel_names else f"Канал {i}"
                    ch = self.raw_data[i]
                    rows.append(f"""
                      <tr>
                        <td>{self._safe_html(name)}</td>
                        <td>{np.mean(ch):.3f}</td>
                        <td>{np.std(ch):.3f}</td>
                        <td>{np.min(ch):.3f}</td>
                        <td>{np.max(ch):.3f}</td>
                      </tr>
                    """)

                body += f"""
                <div class="card">
                  <h3>Статистика каналов</h3>
                  <table>
                    <tr><th>Канал</th><th>Mean</th><th>Std</th><th>Min</th><th>Max</th></tr>
                    {''.join(rows)}
                  </table>
                  <div class="muted" style="margin-top:8px;">Показаны первые {maxch} каналов.</div>
                </div>
                """
            else:
                body += f"""
                <div class="card">
                  <h3>Сводка</h3>
                  <div class="row"><div class="k">Статус</div><div class="v">{self._badge("RAW EMPTY", "warn")}</div></div>
                  <div class="muted">Загрузите файл данных, чтобы отобразить информацию.</div>
                </div>
                """

            # ---- Обработка
            if self.processed_data is not None:
                p = self.processing_params
                body += f"""
                <div class="card">
                  <h3>Обработка</h3>
                  <div class="row"><div class="k">Фильтр</div><div class="v">{p['low_freq']}-{p['high_freq']} Гц</div></div>
                  <div class="row"><div class="k">Notch</div><div class="v">{p['notch_freq']} Гц</div></div>
                  <div class="row"><div class="k">Detrend</div><div class="v">{self._badge("ON", "ok") if p.get("detrend") else self._badge("OFF", "warn")}</div></div>
                  <div class="row"><div class="k">DC offset</div><div class="v">{self._badge("ON", "ok") if p.get("remove_dc") else self._badge("OFF", "warn")}</div></div>
                  <div class="row"><div class="k">Artifacts</div><div class="v">{self._badge("ON", "ok") if p.get("remove_artifacts") else self._badge("OFF", "warn")}</div></div>
                </div>
                """
                if p.get("remove_artifacts"):
                    body += f"""
                    <div class="card">
                      <h3>Порог артефактов</h3>
                      <div class="row"><div class="k">σ</div><div class="v">{p.get("artifact_threshold")}</div></div>
                    </div>
                    """
            else:
                body += f"""
                <div class="card">
                  <h3>Обработка</h3>
                  <div class="row"><div class="k">Статус</div><div class="v">{self._badge("PROCESSED EMPTY", "warn")}</div></div>
                  <div class="muted">Обработанные данные ещё не сформированы.</div>
                </div>
                """

            # ---- Анализ
            if self.current_analysis is not None:
                analysis = self.current_analysis["analysis"]
                channel_idx = self.current_analysis["channel_idx"]
                ch_name = self.channel_names[channel_idx] if self.channel_names else f"Канал {channel_idx}"

                body += f"""
                <div class="card">
                  <h3>Анализ</h3>
                  <div class="row"><div class="k">Канал</div><div class="v">{self._safe_html(ch_name)}</div></div>
                </div>
                """

                if "rhythm_powers" in analysis and isinstance(analysis["rhythm_powers"], dict):
                    items = []
                    for rhythm, power in analysis["rhythm_powers"].items():
                        items.append(f"<li><b>{self._safe_html(rhythm)}</b> — {float(power):.6f}</li>")
                    body += f"""
                    <div class="card">
                      <h3>Мощности ритмов</h3>
                      <ul>{''.join(items)}</ul>
                    </div>
                    """
            else:
                body += f"""
                <div class="card">
                  <h3>Анализ</h3>
                  <div class="row"><div class="k">Статус</div><div class="v">{self._badge("NO ANALYSIS", "warn")}</div></div>
                  <div class="muted">Запустите анализ ритмов, чтобы увидеть результат.</div>
                </div>
                """

            # ---- Производительность (кратко)
            if hasattr(self, "performance_monitor"):
                try:
                    perf_summary = self.performance_monitor.get_summary()
                    body += f"""
                    <div class="card">
                      <h3>Производительность</h3>
                      <pre>{self._safe_html(perf_summary)}</pre>
                    </div>
                    """
                except:
                    pass

            self.info_panel.info_text.setHtml(self._html_page("Информация", body))

        except Exception as e:
            self.info_panel.info_text.setHtml(self._html_page("Информация",
                                                              f"<div class='card'><h3>Ошибка</h3><pre>{self._safe_html(e)}</pre></div>"))

    def update_recommendations(self):
        if self.current_analysis is None:
            return
        try:
            analysis = self.current_analysis["analysis"]
            recommendations = self.current_analysis.get("recommendations", {})

            body = ""

            # --- Общий блок от анализатора
            if recommendations and isinstance(recommendations, dict) and "general" in recommendations:
                g = recommendations["general"]
                summary = g.get("summary", "—")
                dom = str(g.get("dominant_rhythm", "—")).upper()
                relax = g.get("relaxation_level", "—")

                body += f"""
                <div class="card">
                  <h3>Общее состояние</h3>
                  <div class="row"><div class="k">Итог</div><div class="v">{self._safe_html(summary)}</div></div>
                  <div class="row"><div class="k">Доминирующий ритм</div><div class="v">{self._badge(dom, "accent")}</div></div>
                  <div class="row"><div class="k">Расслабление</div><div class="v">{self._safe_html(relax)}</div></div>
                </div>
                """
            else:
                body += f"""
                <div class="card">
                  <h3>Общее состояние</h3>
                  <div class="muted">Нет структурированных рекомендаций от анализатора — отображены базовые блоки ниже.</div>
                </div>
                """

            # --- Детально по ритмам (карточками)
            if recommendations and isinstance(recommendations, dict) and "rhythm_details" in recommendations:
                for rhythm, details in recommendations["rhythm_details"].items():
                    state = str(details.get("state", "—"))
                    rec = str(details.get("recommendation", "—"))
                    p = float(details.get("relative_power", 0))

                    lvl = "accent"
                    s_low = state.lower()
                    if "стресс" in s_low or "высок" in s_low:
                        lvl = "warn"
                    if "аном" in s_low or "патолог" in s_low:
                        lvl = "bad"

                    body += f"""
                    <div class="card">
                      <h3>{self._safe_html(str(rhythm).upper())}</h3>
                      <div class="row"><div class="k">Состояние</div><div class="v">{self._badge(state, lvl)} {self._badge(f"{p * 100:.1f}%", "accent")}</div></div>
                      <div class="muted" style="margin-top:8px;">{self._safe_html(rec)}</div>
                    </div>
                    """

            # --- Специальные рекомендации (как чек-лист)
            if recommendations and isinstance(recommendations, dict) and recommendations.get(
                    "specific_recommendations"):
                items = []
                for rec in recommendations["specific_recommendations"]:
                    items.append(f"<li>{self._safe_html(rec)}</li>")
                body += f"""
                <div class="card">
                  <h3>Специальные рекомендации</h3>
                  <ul>{''.join(items)}</ul>
                </div>
                """

            # --- Твой lifestyle/text -> конвертим в списки (не простыня)
            lifestyle_txt = self._generate_lifestyle_recommendations(analysis)
            lifestyle_lines = [ln.strip() for ln in lifestyle_txt.splitlines() if ln.strip().startswith("•")]
            if lifestyle_lines:
                lis = "".join([f"<li>{self._safe_html(ln.replace('•', '').strip())}</li>" for ln in lifestyle_lines])
                body += f"""
                <div class="card">
                  <h3>Образ жизни</h3>
                  <ul>{lis}</ul>
                </div>
                """
            else:
                body += f"""
                <div class="card">
                  <h3>Образ жизни</h3>
                  <pre>{self._safe_html(lifestyle_txt)}</pre>
                </div>
                """

            # --- Медицинские наблюдения: тоже не простыня
            med_txt = self._generate_medical_alerts(analysis)
            med_lines = [ln.strip() for ln in med_txt.splitlines() if ln.strip()]
            # если есть явные "alerts" — делаем список
            med_bullets = [ln for ln in med_lines if "—" in ln or "возможно" in ln.lower() or "рекоменду" in ln.lower()]
            if med_bullets:
                lis = "".join([f"<li>{self._safe_html(ln)}</li>" for ln in med_bullets])
                body += f"""
                <div class="card">
                  <h3>Медицинские наблюдения</h3>
                  <ul>{lis}</ul>
                  <div class="muted" style="margin-top:8px;">Важно: это информационная интерпретация, не диагноз.</div>
                </div>
                """
            else:
                body += f"""
                <div class="card">
                  <h3>Медицинские наблюдения</h3>
                  <pre>{self._safe_html(med_txt)}</pre>
                </div>
                """

            self.info_panel.recommendations_text.setHtml(self._html_page("Рекомендации", body))

        except Exception as e:
            print(f"Ошибка обновления рекомендаций: {e}")
            self._show_basic_recommendations()

    def _generate_lifestyle_recommendations(self, analysis):
        rec_text = "РЕКОМЕНДАЦИИ ПО ОБРАЗУ ЖИЗНИ:\n\n"

        try:
            if 'rhythm_analysis' in analysis:
                rhythm_analysis = analysis['rhythm_analysis']

                alpha_power = rhythm_analysis.get('alpha', {}).get('relative_power', 0)
                beta_power = rhythm_analysis.get('beta', {}).get('relative_power', 0)
                theta_power = rhythm_analysis.get('theta', {}).get('relative_power', 0)
                delta_power = rhythm_analysis.get('delta', {}).get('relative_power', 0)
                gamma_power = rhythm_analysis.get('gamma', {}).get('relative_power', 0)

                if beta_power > 0.3:  # Высокая бета-активность
                    rec_text += "УПРАВЛЕНИЕ СТРЕССОМ:\n"
                    rec_text += "   • Необходимо снизить уровень стресса\n"
                    rec_text += "   • Рекомендуется медитация или дыхательные упражнения\n"
                    rec_text += "   • Избегайте кофеина и стимуляторов\n"
                    rec_text += "   • Практикуйте прогрессивную мышечную релаксацию\n\n"

                elif alpha_power > 0.25:  # Высокая альфа-активность
                    rec_text += "РАССЛАБЛЕНИЕ:\n"
                    rec_text += "   • Отличное состояние для медитации\n"
                    rec_text += "   • Подходящее время для творческой деятельности\n"
                    rec_text += "   • Можно продолжить текущую активность\n\n"

                # Рекомендации по сну
                if delta_power > 0.25:  # Высокая дельта-активность
                    rec_text += "СОН И ОТДЫХ:\n"
                    rec_text += "   • Организм нуждается в отдыхе\n"
                    rec_text += "   • Рекомендуется короткий сон (20-30 минут)\n"
                    rec_text += "   • Обеспечьте комфортные условия для сна\n"
                    rec_text += "   • Избегайте физических нагрузок\n\n"

                elif delta_power < 0.05:  # Низкая дельта-активность
                    rec_text += "КАЧЕСТВО СНА:\n"
                    rec_text += "   • Возможны проблемы с качеством сна\n"
                    rec_text += "   • Соблюдайте режим сна (7-9 часов)\n"
                    rec_text += "   • Создайте комфортную среду для сна\n"
                    rec_text += "   • Избегайте экранов за 1-2 часа до сна\n\n"

                # Рекомендации по когнитивной активности
                if gamma_power > 0.15:  # Высокая гамма-активность
                    rec_text += "КОГНИТИВНАЯ НАГРУЗКА:\n"
                    rec_text += "   • Высокая умственная активность\n"
                    rec_text += "   • Делайте регулярные перерывы (каждые 45-60 минут)\n"
                    rec_text += "   • Пейте достаточно воды\n"
                    rec_text += "   • Избегайте переутомления\n\n"

                elif gamma_power < 0.05:  # Низкая гамма-активность
                    rec_text += "СТИМУЛЯЦИЯ МОЗГА:\n"
                    rec_text += "   • Рекомендуется умственная активность\n"
                    rec_text += "   • Решайте головоломки или читайте\n"
                    rec_text += "   • Изучайте что-то новое\n"
                    rec_text += "   • Занимайтесь физическими упражнениями\n\n"

                # Рекомендации по творчеству
                if theta_power > 0.15:  # Высокая тета-активность
                    rec_text += "ТВОРЧЕСКАЯ ДЕЯТЕЛЬНОСТЬ:\n"
                    rec_text += "   • Отличное время для творчества\n"
                    rec_text += "   • Занимайтесь искусством или музыкой\n"
                    rec_text += "   • Практикуйте свободное письмо\n"
                    rec_text += "   • Используйте техники мозгового штурма\n\n"

        except Exception as e:
            rec_text += f"Ошибка генерации рекомендаций: {e}\n\n"

        return rec_text

    def _generate_medical_alerts(self, analysis):
        """Генерация медицинских предупреждений"""
        alert_text = "МЕДИЦИНСКИЕ НАБЛЮДЕНИЯ:\n\n"

        try:
            if 'rhythm_analysis' in analysis:
                rhythm_analysis = analysis['rhythm_analysis']
                alerts = []

                # Проверка на аномальные паттерны
                delta_power = rhythm_analysis.get('delta', {}).get('relative_power', 0)
                theta_power = rhythm_analysis.get('theta', {}).get('relative_power', 0)
                alpha_power = rhythm_analysis.get('alpha', {}).get('relative_power', 0)
                beta_power = rhythm_analysis.get('beta', {}).get('relative_power', 0)

                # Предупреждения о возможных состояниях
                if delta_power > 0.4:
                    alerts.append("Очень высокая дельта-активность - возможно состояние глубокого сна или патология")

                if beta_power > 0.4:
                    alerts.append("Очень высокая бета-активность - возможна тревожность или стресс")

                if alpha_power < 0.05 and beta_power > 0.3:
                    alerts.append("Низкая альфа при высокой бета - признаки стресса или переутомления")

                if theta_power > 0.3 and delta_power < 0.1:
                    alerts.append("Высокая тета при низкой дельта - возможна сонливость в бодрствующем состоянии")

                # Проверка на спайки (если есть данные)
                if 'spike_count' in analysis and analysis['spike_count'] > 10:
                    alerts.append("Обнаружено повышенное количество спайков - рекомендуется консультация специалиста")

                if alerts:
                    for alert in alerts:
                        alert_text += f"{alert}\n\n"
                    alert_text += "ВАЖНО: Данные рекомендации носят информационный характер.\n"
                    alert_text += "При наличии симптомов обратитесь к врачу-неврологу.\n\n"
                else:
                    alert_text += "Значительных отклонений не обнаружено.\n"
                    alert_text += "Показатели находятся в пределах нормальных значений.\n\n"

        except Exception as e:
            alert_text += f"Ошибка анализа медицинских данных: {e}\n\n"

        return alert_text

    def _show_basic_recommendations(self):
        body = """
        <div class="card">
          <h3>Базовые рекомендации</h3>
          <ul>
            <li>Проверьте качество сигнала перед анализом</li>
            <li>Убедитесь в корректности настроек фильтров</li>
            <li>Сравните результаты с нормативными диапазонами</li>
            <li>При необходимости проверьте расчёты через MNE-Python</li>
            <li>Сохраните отчёт для последующего сравнения</li>
          </ul>
        </div>
        <div class="card">
          <h3>Подсказка по ритмам</h3>
          <table>
            <tr><th>Ритм</th><th>Диапазон</th><th>Обычно связан с</th></tr>
            <tr><td>Дельта</td><td>0.5–4 Гц</td><td>Глубокий сон</td></tr>
            <tr><td>Тета</td><td>4–8 Гц</td><td>Сонливость / медитация</td></tr>
            <tr><td>Альфа</td><td>8–13 Гц</td><td>Расслабление</td></tr>
            <tr><td>Бета</td><td>13–30 Гц</td><td>Концентрация / стресс</td></tr>
            <tr><td>Гамма</td><td>30–100 Гц</td><td>Высокая когнитивная активность</td></tr>
          </table>
        </div>
        """
        self.info_panel.recommendations_text.setHtml(self._html_page("Рекомендации", body))

    def update_performance_display(self):
        try:
            report = self.performance_monitor.get_rhythm_analysis_report()
            body = f"""
            <div class="card">
              <h3>Мониторинг</h3>
              <div class="row"><div class="k">Источник</div><div class="v">{self._badge("Rhythm report", "ok")}</div></div>
            </div>
            <div class="card">
              <h3>Отчёт</h3>
              <pre>{self._safe_html(report)}</pre>
            </div>
            """
            self.info_panel.performance_text.setHtml(self._html_page("Мониторинг", body))
        except Exception as e:
            print(f"Ошибка обновления производительности: {e}")
            try:
                summary = self.performance_monitor.get_summary()
                body = f"""
                <div class="card">
                  <h3>Мониторинг</h3>
                  <div class="row"><div class="k">Источник</div><div class="v">{self._badge("Summary", "warn")}</div></div>
                </div>
                <div class="card">
                  <h3>Сводка</h3>
                  <pre>{self._safe_html(summary)}</pre>
                </div>
                """
                self.info_panel.performance_text.setHtml(self._html_page("Мониторинг", body))
            except:
                self.info_panel.performance_text.setHtml(self._html_page("Мониторинг",
                                                                         "<div class='card'><h3>Ошибка</h3><div class='muted'>Не удалось получить отчёт.</div></div>"))

    def show_performance_report(self, report):
        body = f"""
        <div class="card">
          <h3>Экспорт / отчёт</h3>
          <div class="muted">Ниже отображается сформированный текст отчёта в “моноширинном” виде.</div>
        </div>
        <div class="card">
          <h3>Текст отчёта</h3>
          <pre>{self._safe_html(report)}</pre>
        </div>
        """
        self.info_panel.performance_text.setHtml(self._html_page("Отчёт", body))
        self.info_panel.info_tabs.setCurrentWidget(self.info_panel.performance_text)