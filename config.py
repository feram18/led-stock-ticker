#!/usr/bin/python3
"""Software configuration script"""

import questionary
import math
from constants import CONFIG_FILE, CLOCK_FORMATS, DEFAULT_CRYPTOS, DEFAULT_STOCKS, ROTATION_RATE
from data.currency import currencies as valid_currencies
from utils import read_json, write_json


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
    return [i for n, i in enumerate(stocks) if i not in stocks[:n]]


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
    return [i for n, i in enumerate(cryptos) if i not in cryptos[:n]]


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


def get_update_rate(total_tickers: int) -> float:
    """
    Get update rate based on the number of tickers.
    :param total_tickers: total number of tickers
    :return: update_rate: (float) update rate in seconds
    """
    # Ensure a full rotation is complete before an update is requested
    min_rate = math.ceil((total_tickers * ROTATION_RATE) + ROTATION_RATE) // 60  # in minutes

    choices = ['5', '10', '15', '20']
    if 1 < min_rate < 5:
        choices.insert(0, str(min_rate))
    elif 5 < min_rate < 10:
        choices[0] = str(min_rate)

    return float(questionary.select('Select update rate:',
                                    choices=choices,
                                    default='15',
                                    qmark='\U0011F504',
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
    config['update_rate'] = get_update_rate(len(config['tickers']['stocks'] + config['tickers']['cryptos']))
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
