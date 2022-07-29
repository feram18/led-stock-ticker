#!/usr/bin/python3
"""Software configuration script"""

import questionary
import math
import time
from constants import CONFIG_FILE, CLOCK_FORMATS, DEFAULT_CRYPTOS, DEFAULT_STOCKS, DEFAULT_ROTATION_RATE, \
    DEFAULT_UPDATE_RATE, DEFAULT_DATE_FORMAT, DATE_FORMATS
from data.currency import currencies as valid_currencies
from util.utils import read_json, write_json


def get_current_preferences() -> dict:
    """
    Return current preferences from config.json
    :return: current_preferences (dict)
    """
    preferences = read_json(CONFIG_FILE)
    return {
        'stocks': ' '.join(preferences['tickers']['stocks']),
        'cryptos': ' '.join(preferences['tickers']['cryptos']),
        'currency': preferences['currency'],
        'clock_format': preferences['clock_format'],
        'date_format': preferences['date_format'],
        'rotation_rate': preferences['rotation_rate']
    }


def get_stocks(pref: str) -> list:
    """
    Get user's preferred stocks.
    :param pref (str) Current preferred stocks list
    :return: stocks: (list) List of stocks
    """
    stocks = questionary.text('Enter stocks:',
                              default=' '.join(DEFAULT_STOCKS) if len(pref) < 1 else pref,
                              qmark='\U0001F4C8',
                              instruction='(Separate each ticker by a space)').ask().upper().split()
    return [i for n, i in enumerate(stocks) if i not in stocks[:n]]


def get_cryptos(pref: str) -> list:
    """
    Get user's preferred cryptos.
    :param pref (str) Current preferred cryptos list
    :return: cryptos: (list) List of cryptos
    """
    cryptos = questionary.text('Enter cryptos:',
                               default=' '.join(DEFAULT_CRYPTOS) if len(pref) < 1 else pref,
                               qmark='\U0001F4B0',
                               instruction='(Separate each ticker by a space)').ask().upper().split()
    return [i for n, i in enumerate(cryptos) if i not in cryptos[:n]]


def get_currency(pref: str) -> str:
    """
    Get user's preferred currency.
    :param pref (str) Current preferred currency
    :return: currency: (str) Currency
    """
    currencies = list(valid_currencies.keys())
    return questionary.select('Select currency:',
                              choices=currencies,
                              default='USD' if len(pref) < 1 else pref,
                              qmark='\U0001F4B1').ask()


def get_clock_format(pref: str) -> str:
    """
    Get user's preferred clock format.
    :param pref (str) Current preferred clock format
    :return: clock_format: (str) Clock format
    """
    return questionary.select('Select clock format:',
                              choices=CLOCK_FORMATS,
                              default=CLOCK_FORMATS[0] if len(pref) < 1 else pref,
                              qmark='\U0001F552').ask()


def get_date_format(pref: str) -> str:
    """
    Get user's preferred date format.
    :param pref: (str) Current preferred date format
    :return: date_format: (str) Date format
    """
    choices = [time.strftime(fmt) for fmt in DATE_FORMATS]
    selection = questionary.select('Select date format:',
                                   choices=choices,
                                   default=time.strftime(DEFAULT_DATE_FORMAT) if len(pref) < 1 else time.strftime(pref),
                                   qmark='\U0001F4C5').ask()
    return DATE_FORMATS[choices.index(selection)]


def get_rotation_rate(curr_preference: int) -> int:
    """
    Get user's preferred rotation rate
    :param curr_preference: (int) Current preferred rotation rate
    :return: rotation_rate: Rotation rate
    """
    return int(questionary.select('Select rotation rate:',
                                  choices=['5', '10', '15'],
                                  default=str(curr_preference) if curr_preference else DEFAULT_ROTATION_RATE,
                                  qmark='\U0001F504',
                                  instruction='(in seconds)').ask())


def get_update_rate(total_tickers: int, rotation_rate: int) -> int:
    """
    Get update rate based on the number of tickers.
    :param rotation_rate: ticker rotation rate
    :param total_tickers: total number of tickers
    :return: update_rate: (int) update rate in seconds
    """
    # Ensure a full rotation is complete before an update is requested
    min_rate = math.ceil((total_tickers * rotation_rate) + rotation_rate) // 60  # in minutes

    choices = ['5', '10', '15', '20']
    if 1 < min_rate < 5:
        choices.insert(0, str(min_rate))
    elif 5 < min_rate < 10:
        choices[0] = str(min_rate)

    return int(questionary.select('Select update rate:',
                                  choices=choices,
                                  default=str(DEFAULT_UPDATE_RATE // 60),
                                  qmark='\U000123EC',
                                  instruction='(in minutes)').ask()) * 60


def set_preferences(config: dict, current_config: dict) -> dict:
    """
    Write preferences to config.json file.
    :param config (dict) Config dict to edit
    :param current_config (dict) Current config dict values
    :return: data: (dict) Data dictionary
    """
    config['tickers']['stocks'] = get_stocks(current_config['stocks'])
    config['tickers']['cryptos'] = get_cryptos(current_config['cryptos'])
    config['currency'] = get_currency(current_config['currency'])
    config['clock_format'] = get_clock_format(current_config['clock_format'])
    config['date_format'] = get_date_format(current_config['date_format'])
    config['rotation_rate'] = get_rotation_rate(current_config['rotation_rate'])
    config['update_rate'] = get_update_rate(len(config['tickers']['stocks'] + config['tickers']['cryptos']),
                                            config['rotation_rate'])
    return config


def main():
    try:
        config_json = read_json(CONFIG_FILE)
        config_json = set_preferences(config_json, get_current_preferences())
        write_json(CONFIG_FILE, config_json)
        questionary.print('\u2705 Setup is complete!', style='bold fg:green')
    except (KeyboardInterrupt, AttributeError):
        SystemExit('Setup cancelled. Setting default values.')


if __name__ == '__main__':
    main()
