#!/usr/bin/python3
"""Software configuration script"""
import math
import time

import questionary

from constants import CONFIG_FILE, DEFAULT_STOCKS, DEFAULT_CRYPTOS, DEFAULT_FOREX, CLOCK_FORMATS, DATE_FORMATS, \
    DEFAULT_DATE_FORMAT, DEFAULT_ROTATION_RATE, DEFAULT_UPDATE_RATE
from data.currency import CURRENCIES
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
        'forex': ' '.join(preferences['tickers']['forex']),
        'currency': preferences['options']['currency'],
        'clock_format': preferences['options']['clock_format'],
        'date_format': preferences['options']['date_format'],
        'rotation_rate': preferences['options']['rotation_rate'],
        'show_logos': preferences['options']['show_logos']
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


def get_forex(pref: str) -> list:
    """
    Get user's preferred forex pairs.
    :param pref (str) Current preferred forex list
    :return: forex: (list) List of forex
    """
    forex = questionary.text('Enter forex pairs:',
                             default=' '.join(DEFAULT_FOREX) if len(pref) < 1 else pref,
                             qmark='\U0001F4B1',
                             instruction='(Separate each pair by a space)').ask().upper().split()
    return [i for n, i in enumerate(forex) if i not in forex[:n]]


def get_currency(pref: str) -> str:
    """
    Get user's preferred currency.
    :param pref (str) Current preferred currency
    :return: currency: (str) Currency
    """
    return questionary.select('Select currency:',
                              choices=list(CURRENCIES.keys()),
                              default='USD' if len(pref) < 1 else pref,
                              qmark='\U0001F4B2').ask()


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

    return int(questionary.select(' Select update rate:',
                                  choices=choices,
                                  default=str(DEFAULT_UPDATE_RATE // 60),
                                  qmark='\U000123EC',
                                  instruction='(in minutes)').ask())


def get_show_logos(pref: bool) -> bool:
    """
    Get user's choice to show company stock/crypto logos.
    :param pref: current user preference
    :return: (bool) show_logos preference
    """
    return questionary.confirm('Show company stock & crypto logos? History chart will be displayed otherwise: ',
                               default=pref if pref else False,
                               qmark='\U0001F5BC').ask()


def set_preferences(config: dict, current_config: dict) -> dict:
    """
    Write preferences to config.json file.
    :param config (dict) Config dict to edit
    :param current_config (dict) Current config dict values
    :return: data: (dict) Data dictionary
    """
    config['tickers']['stocks'] = get_stocks(current_config['stocks'])
    config['tickers']['cryptos'] = get_cryptos(current_config['cryptos'])
    config['tickers']['forex'] = get_forex(current_config['forex'])
    config['options']['currency'] = get_currency(current_config['currency'])
    config['options']['clock_format'] = get_clock_format(current_config['clock_format'])
    config['options']['date_format'] = get_date_format(current_config['date_format'])
    config['options']['rotation_rate'] = get_rotation_rate(current_config['rotation_rate'])
    total_tickers = len(config['tickers']['stocks'] + config['tickers']['cryptos'] + config['tickers']['forex'])
    config['options']['update_rate'] = get_update_rate(total_tickers, config['options']['rotation_rate'])
    config['options']['show_logos'] = get_show_logos(current_config['show_logos'])
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
