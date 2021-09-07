#!/usr/bin/python3
"""Software configuration script"""

import questionary
from constants import CONFIG_FILE, CLOCK_FORMATS, DEFAULT_CRYPTOS, DEFAULT_STOCKS
from data.currency import currencies as valid_currencies
from utils import read_json, write_json


def get_current_preferences() -> dict:
    """
    Return current config.json values
    :return: current_preferences (dict)
    """
    preferences = read_json(CONFIG_FILE)
    return {
        'stocks': ' '.join(preferences['tickers']['stocks']),
        'cryptos': ' '. join(preferences['tickers']['cryptos']),
        'currency': preferences['currency'],
        'clock_format': preferences['clock_format']
    }


def get_stocks(curr_preference: str) -> list:
    """
    Get user's preferred stocks.
    :param curr_preference (str) Current preferred stocks list
    :return: stocks: (list) List of stocks
    """
    stocks = questionary.text('Enter your preferred stocks:',
                              default=' '.join(DEFAULT_STOCKS) if len(curr_preference) < 1 else curr_preference,
                              validate=lambda text: len(text) > 0,
                              qmark='\U0001F4C8',
                              instruction='(Separate each ticker by a space)').ask().upper().split()
    result = []
    for stock in stocks:
        if stock not in result:  # Verify ticker is unique
            result.append(stock)
    return result


def get_cryptos(curr_preference: str) -> list:
    """
    Get user's preferred cryptos.
    :param curr_preference (str) Current preferred cryptos list
    :return: cryptos: (list) List of cryptos
    """
    cryptos = questionary.text('Enter your preferred cryptos:',
                               default=' '.join(DEFAULT_CRYPTOS) if len(curr_preference) < 1 else curr_preference,
                               qmark='\U0001F4B0',
                               instruction='(Separate each ticker by a space)').ask().upper().split()

    result = []
    for crypto in cryptos:
        if crypto not in result:  # Verify ticker is unique
            result.append(crypto)
    return result


def get_currency(curr_preference: str) -> str:
    """
    Get user's preferred currency.
    :param curr_preference (str) Current preferred currency
    :return: currency: (str) Currency
    """
    currencies = list(valid_currencies.keys())
    return questionary.select('Select your preferred currency:',
                              choices=currencies,
                              default='USD' if len(curr_preference) < 1 else curr_preference,
                              qmark='\U0001F4B1').ask()


def get_clock_format(curr_preference: str) -> str:
    """
    Get user's preferred clock format.
    :param curr_preference (str) Current preferred clock format
    :return: clock_format: (str) Clock format
    """
    return questionary.select('Select your preferred clock format:',
                              choices=CLOCK_FORMATS,
                              default=CLOCK_FORMATS[0] if len(curr_preference) < 1 else curr_preference,
                              qmark='\U0001F552').ask()


def set_data(config: dict, current_config: dict) -> dict:
    """
    Set config dictionary data.
    :param config (dict) Config dict to edit
    :param current_config (dict) Current config dict values
    :return: data: (dict) Data dictionary
    """
    config['tickers']['stocks'] = get_stocks(current_config['stocks'])
    config['tickers']['cryptos'] = get_cryptos(current_config['cryptos'])
    config['currency'] = get_currency(current_config['currency'])
    config['clock_format'] = get_clock_format(current_config['clock_format'])
    return config


def main():
    try:
        config_json = read_json(CONFIG_FILE)
        config_json = set_data(config_json, get_current_preferences())
        write_json(CONFIG_FILE, config_json)
        questionary.print('\u2705 Setup is complete!', style='bold fg:green')
    except (KeyboardInterrupt, AttributeError):
        SystemExit('Setup cancelled. Setting default values.')


if __name__ == '__main__':
    main()
