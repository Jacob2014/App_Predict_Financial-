import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from data_collection import fetch_moex_data, fetch_binance_data
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class StockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Приложение для анализа акций и криптовалют")
        self.root.geometry("800x600")

        self.style = ttk.Style()
        self.style.configure("TButton", font=("Helvetica", 12), padding=10)
        self.style.configure("TLabel", font=("Helvetica", 12), padding=10)
        self.style.configure("TEntry", font=("Helvetica", 12), padding=5)

        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill="both", expand=True)

        self.create_main_menu()

    def create_main_menu(self):
        self.clear_frame()

        ttk.Label(self.main_frame, text="Выберите тип данных:").pack(pady=10)

        self.data_type = tk.StringVar()
        self.data_type.set("Криптовалюта")

        crypto_radio = ttk.Radiobutton(self.main_frame, text="Криптовалюта", variable=self.data_type,
                                       value="Криптовалюта")
        stock_radio = ttk.Radiobutton(self.main_frame, text="Акции", variable=self.data_type, value="Акции")
        crypto_radio.pack(pady=5)
        stock_radio.pack(pady=5)

        ttk.Label(self.main_frame, text="Введите символ (например, BTCUSDT или SBER):").pack(pady=10)
        self.symbol_entry = ttk.Entry(self.main_frame)
        self.symbol_entry.pack(pady=5)

        analyze_button = ttk.Button(self.main_frame, text="Анализировать", command=self.analyze_data)
        analyze_button.pack(pady=20)

    def analyze_data(self):
        symbol = self.symbol_entry.get()
        data_type = self.data_type.get()

        if not symbol:
            messagebox.showerror("Ошибка", "Введите символ.")
            return

        if data_type == "Криптовалюта":
            data = fetch_binance_data(symbol)
            if data.empty:
                messagebox.showerror("Ошибка", "Данные для данного символа не найдены.")
                return
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(data['timestamp'], data['close'], label=f'{symbol} Цена закрытия')
            ax.set_title(f'Binance {symbol} Цена закрытия')
            ax.set_xlabel('Дата')
            ax.set_ylabel('Цена закрытия')
            ax.legend()
        elif data_type == "Акции":
            data = fetch_moex_data(symbol)
            if data is None or 'TRADEDATE' not in data.columns or 'CLOSE' not in data.columns:
                messagebox.showerror("Ошибка",
                                     f"Необходимые столбцы не найдены в данных. Доступные столбцы: {', '.join(data.columns)}")
                return
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(data['TRADEDATE'], data['CLOSE'], label=f'{symbol} Цена закрытия')
            ax.set_title(f'MOEX {symbol} Цена закрытия')
            ax.set_xlabel('Дата')
            ax.set_ylabel('Цена закрытия')
            ax.legend()

        self.clear_frame()
        canvas = FigureCanvasTkAgg(fig, master=self.main_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

        self.create_back_button()

    def create_back_button(self):
        back_button = ttk.Button(self.main_frame, text="Назад в главное меню", command=self.create_main_menu)
        back_button.pack(pady=10)

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = StockApp(root)
    root.mainloop()
