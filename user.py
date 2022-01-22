import pickle


class User:
    def __init__(self, id):
        self.id = id
        self.tickers = []
        self.portfolio = {}
        self.load_user()

    def add_ticker(self, ticker):
        if isinstance(ticker, str):
            self.tickers.append(ticker)
        elif isinstance(ticker, list):
            self.tickers += ticker

    def delete_ticker(self, tickers):
        for ticker in tickers:
            self.tickers.remove(ticker)

    def print_user_info(self):
        print(self.id)
        print(self.tickers)
        print(self.portfolio)

    def save_user(self):
        database = self.load_user_database()
        database[self.id] = self
        with open('test_db.pickle', 'wb') as handler:
            pickle.dump(database, handler)

    def load_user_database(self):
        with open('test_db.pickle', 'rb') as handler:
            database = pickle.load(handler)
        return database

    def load_user(self):
        database = self.load_user_database()
        if self.id in database:
            self.tickers = database[self.id].tickers


class Ticker:
    def __init__(self, ticker, quantity, average):
        self.ticker = ticker
        self.quantity = quantity
        self.average = average
        self.value = self.quantity * self.average

    def __str__(self):
        return f'Ticker - {self.ticker}, quantity of {self.quantity} with average price of {self.average}'

    def buy(self, quantity, price):
        self.average = (self.average * self.quantity + price * quantity) / (self.quantity + quantity)
        self.quantity += quantity
        print(f'Bought {quantity} of {self.ticker} at {price}\n'
              f'New quantity {self.quantity} with average price of {self.average}')
        self._update_value(self.buy, quantity, price)

    def sell(self, quantity, price):
        self.quantity -= quantity
        print(f'Sold {quantity} of {self.ticker} at {price}\n'
              f'New quantity {self.quantity} with average price of {self.average}')
        self._update_value(self.sell, quantity, price)

    def _update_value(self, action, quantity, price):
        if action == self.buy:
            self.value += quantity * price
        else:
            self.value -= quantity * price


class Portfolio:
    def __init__(self, tickers: [Ticker]):
        self.tickers = tickers

    def add_ticker(self, ticker: Ticker):
        self.tickers.append(ticker)

    def delete_ticker(self, ticker: Ticker):
        self.tickers.remove(ticker)

    def update(self, ticker: Ticker):
        self.tickers.index[ticker] = ticker

    def print_portfolio(self):
        print('Current Portfolio...')
        for ticker in self.tickers:
            print(f'\t{ticker}')

    def build(self):
        print(sum([i.value for i in self.tickers]))