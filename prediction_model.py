import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error


def train_model():
    binance_data = pd.read_csv('binance_data.csv')

    # Пример подготовки данных и тренировки модели
    binance_data['timestamp'] = pd.to_datetime(binance_data['timestamp'])
    binance_data['timestamp'] = binance_data['timestamp'].map(pd.Timestamp.toordinal)

    X = binance_data[['timestamp']]
    y = binance_data['close']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    print(f'Mean Squared Error: {mse}')

    return model


if __name__ == "__main__":
    model = train_model()