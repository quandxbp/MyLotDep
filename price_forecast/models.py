from timeseries.models.time_price import TimePrice

import pandas as pd
from fbprophet import Prophet

import datetime
import logging

class PriceForecast:

    def prophet_forecast(self, product_id):
        tp = TimePrice()
        data = tp.get_price_list_by_id(product_id)
        df = pd.DataFrame(data)

        df['Date'] = pd.DatetimeIndex(df['Date'])
        df = df.rename(columns={'Date': 'ds', 'Price': 'y'})
        my_model = Prophet(interval_width=0.8, daily_seasonality=True)
        try:
            my_model.fit(df)
        except ValueError:
            logging.warning("Not enough data to predict")
            return [], []
        future_dates = my_model.make_future_dataframe(periods=5, freq='D')
        forecast = my_model.predict(future_dates)

        datetime_stamp = forecast['ds'].tail(5).tolist()
        yhat = forecast['yhat'].tail(5).tolist()
        trend = forecast['trend'].tail(10).tolist()

        labels = []
        for dt in datetime_stamp:
            format_date = datetime.datetime.strftime(dt, '%d/%m/%Y')
            labels.append(format_date)

        prices = []
        for price in yhat:
            prices.append(self._round_price(price))

        return labels, prices

    def _round_price(self, price):
        price = round(price)
        del_value = abs(price) % 10000

        if del_value < 5000:
            price -= del_value
        else:
            price += 10000 - del_value

        return price



    # def train_data(self):
    #     tp = TimePrice()
    #     data = tp.get_price_list_by_id("23590831")
    #     df = pd.DataFrame(data)
    #     df['Date'] = pd.to_datetime(df.Date, format='%d-%m-%Y %H:%M:%S')
    #     df.index = df['Date']
    #
    #     data = df.sort_index(ascending=True, axis=0)
    #     new_data = pd.DataFrame(index=range(0, len(df)), columns=['Date', 'Price'])
    #
    #     for i in range(0, len(data)):
    #         new_data['Date'][i] = data['Date'][i]
    #         new_data['Price'][i] = data['Price'][i]
    #
    #     # setting index
    #     new_data.index = new_data.Date
    #     new_data.drop('Date', axis=1, inplace=True)
    #
    #     # creating train and test sets
    #     dataset = new_data.values
    #
    #     train = dataset[0:97, :]
    #     valid = dataset[97:, :]
    #
    #     # converting dataset into x_train and y_train
    #     scaler = MinMaxScaler(feature_range=(0, 1))
    #     scaled_data = scaler.fit_transform(dataset)
    #
    #     x_train, y_train = [], []
    #     for i in range(60, len(train)):
    #         x_train.append(scaled_data[i - 60:i, 0])
    #         y_train.append(scaled_data[i, 0])
    #     x_train, y_train = np.array(x_train), np.array(y_train)
    #
    #     x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    #
    #     # create and fit the LSTM network
    #     model = Sequential()
    #     model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    #     model.add(LSTM(units=50))
    #     model.add(Dense(1))
    #
    #     model.compile(loss='mean_squared_error', optimizer='adam')
    #     model.fit(x_train, y_train, epochs=1, batch_size=1, verbose=2)
    #
    #     # predicting 246 values, using past 60 from the train data
    #     inputs = new_data[len(new_data) - len(valid) - 60:].values
    #     inputs = inputs.reshape(-1, 1)
    #     inputs = scaler.transform(inputs)
    #
    #     X_test = []
    #     for i in range(60, inputs.shape[0]):
    #         X_test.append(inputs[i - 60:i, 0])
    #     X_test = np.array(X_test)
    #
    #     X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    #     closing_price = model.predict(X_test)
    #     closing_price = scaler.inverse_transform(closing_price)
    #
    #     print(closing_price)
    #     valid['Predictions'] = closing_price
