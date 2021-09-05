from data.ticker import Ticker
from data.status import Status


class Crypto(Ticker):
    """Class to represent a Crypto object"""

    def get_name(self) -> str:
        """
        Fetch crypto's full name. i.e. BTC -> Bitcoin.
        :return: name: (str) Name
        :exception KeyError: If incorrect data type is provided as an argument. Can occur when a ticker is not valid.
        """
        try:
            return self.format_name(self.data.info['shortName'])
        except KeyError:
            self.valid = False
            self.update_status = Status.FAIL
            return ''

    @staticmethod
    def format_name(name: str) -> str:
        """
        Format crypto's name string to remove currency from it.
        i.e. Bitcoin USD -> Bitcoin
        :param name: (str) Name to format
        :return: name: (str) Formatted name
        """
        currency_postfix = ' USD'
        if currency_postfix in name.upper():
            return name.replace(currency_postfix, '')
        else:
            return name
