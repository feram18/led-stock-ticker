from data.ticker import Ticker
from data.status import Status


class Crypto(Ticker):
    """Class to represent a Crypto object"""

    def get_name(self) -> str:
        """
        Fetch crypto's full name. i.e. BTC -> Bitcoin. Removes 'USD' suffix.
        :return: name: (str) Name
        :exception KeyError: If incorrect data type is provided as an argument. Can occur when a ticker is not valid.
        """
        try:
            name = self.data.info['shortName']
            return name.replace(' USD', '')
        except KeyError:
            self.valid = False
            self.update_status = Status.FAIL
            return ''
