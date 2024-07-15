import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def analyze_data():
    moex_data = pd.read_csv('moex_data.csv')
    binance_data = pd.read_csv('binance_data.csv')

    # Пример анализа и визуализации данных
    plt.figure(figsize=(14, 7))
    sns.lineplot(x='timestamp', y='close', data=binance_data)
    plt.title('Binance BTC/USDT Closing Prices')
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.show()


if __name__ == "__main__":
    analyze_data()
