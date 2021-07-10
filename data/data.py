from constants import MAX_API_REQUESTS, EASTERN_TZ
from datetime import datetime
from pytz import timezone
from .ticker import Ticker
import time


class Data:
    def __init__(self, config):
        self.config = config

        self.tickers = []
        self.current_ticker_index = 0

        self.time_app_started = datetime.now(timezone(EASTERN_TZ))
        self.time_of_use = self.calc_time_of_use()
        self.total_tickers = self.calc_total_tickers()
        self.update_rate = self.calc_update_rate()

        self.refresh_tickers()

    def get_tickers_data(self):
        """
        Setup initial tickers' data
        """
        count = 0
        for ticker in self.config.tickers:
            time_started = datetime.now()
            if count is 4:  # 8 API (max. limit) requests have been made
                time.sleep(60 - time_started.second)  # Wait until next minute for following 8 requests
            self.tickers.append(Ticker(self.config.api_key, ticker, self.config.country, self.update_rate))
            count += 1

    def refresh_tickers(self):
        """
        Update tickers' prices
        """
        if len(self.tickers) < 1:
            self.get_tickers_data()
        else:
            for ticker in self.tickers:
                ticker.update_data()

    def calc_total_tickers(self):
        """
        Calculate the total number of tickers on config file
        :return: total_tickers: int
        """
        return len(self.config.tickers)

    def calc_time_of_use(self):
        """
        Determine amount of time (in minutes) that new data will need to be updated.
        (i.e. Amount of time between current time, and 4:00 PM EST, when prices are no longer updated)
        Result is used to determine update rate.
        :return: time_of_use: float
        """
        end_time = datetime.now(timezone(EASTERN_TZ)).replace(hour=16, minute=0, second=0, microsecond=0)  # 4:00PM
        time_delta = end_time - self.time_app_started
        return time_delta.total_seconds() / 60

    def calc_update_rate(self):
        """
        Determine rate at which software will fetch new data from API
        :return: update_rate: float
        """
        # Number of requests available, after initial data is fetched
        available_requests = MAX_API_REQUESTS - self.total_tickers
        max_rpm = available_requests / self.time_of_use  # Maximum number of requests per minute
        update_rate = round((self.total_tickers / max_rpm) * 60, 2)  # In seconds

        if update_rate > 90.0:
            return update_rate
        else:
            return 90.0

    def current_ticker(self):
        """
        Determine the index of the ticker
        :return: index: int
        """
        return self.tickers[self.current_ticker_index]

    def advance_to_next(self):
        """
        Increase index to the following ticker in the list
        :return: ticker: Ticker
        """
        self.current_ticker_index = self.next_ticker_index()
        return self.current_ticker()

    def next_ticker_index(self):
        """
        Returns the index of the next ticker in the list
        :return: counter: int
        """
        counter = self.current_ticker_index + 1
        if counter >= len(self.tickers):
            counter = 0
        return counter
