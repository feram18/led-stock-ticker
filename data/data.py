from stock import Stock
import datetime
import time


class Data:
    def __init__(self, config):
        self.config = config

        self.symbols = []
        self.current_symbol_index = 0

        self.refresh_symbols()

    def get_symbols_data(self):
        count = 0
        for symbol in self.config.symbols:
            time_started = datetime.datetime.now()
            if count is 4:  # 8 API (max. limit) requests have been made
                time.sleep(60 - time_started.second)  # Wait until next minute for following 8 requests
            self.symbols.append(Stock(self.config.api_key, symbol, self.config.country))
            count += 1

    def refresh_symbols(self):
        if len(self.symbols) < 1:
            self.get_symbols_data()
        else:
            for symbol in self.symbols:
                symbol.update_data()

    def current_symbol(self):
        return self.symbols[self.current_symbol_index]

    def advance_to_next(self):
        self.current_symbol_index = self.next_symbol_index()
        return self.current_symbol()

    def next_symbol_index(self):
        counter = self.current_symbol_index + 1
        if counter >= len(self.symbols):
            counter = 0
        return counter
