# Copyright 2021 Fabian Bosler

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
# Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFINGEMENT. IN NO EVENT SHALL THE AUTHORS
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import time
import logging
from functools import wraps


def retry(exceptions, total_tries=4, initial_wait=0.5, backoff_factor=2):
    """
    calling the decorated function applying an exponential backoff.
    Args:
        exceptions: Exception(s) that trigger a retry, can be a tuple
        total_tries: Total tries
        initial_wait: Time to first retry
        backoff_factor: Backoff multiplier (e.g. value of 2 will double the delay each retry).
    """

    def retry_decorator(f):
        @wraps(f)
        def func_with_retries(*args, **kwargs):
            _tries, _delay = total_tries + 1, initial_wait
            while _tries > 1:
                try:
                    logging.warning(f'{total_tries + 2 - _tries}. try:')
                    return f(*args, **kwargs)
                except exceptions as e:
                    _tries -= 1
                    print_args = args if args else 'no args'
                    if _tries == 1:
                        logging.warning(str(f'Function: {f.__name__}\n'
                                            f'Failed despite best efforts after {total_tries} tries.\n'
                                            f'args: {print_args}, kwargs: {kwargs}'))
                        raise
                    logging.warning(str(f'Function: {f.__name__}\n'
                                        f'Exception: {e}\n'
                                        f'Retrying in {_delay} seconds!, args: {print_args}, kwargs: {kwargs}\n'))
                    time.sleep(_delay)
                    _delay *= backoff_factor

        return func_with_retries

    return retry_decorator
