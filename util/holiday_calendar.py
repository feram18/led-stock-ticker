from pandas.tseries.offsets import WeekOfMonth
from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday, sunday_to_monday, GoodFriday, USMemorialDay, \
    USLaborDay, USThanksgivingDay


class MarketHolidayCalendar(AbstractHolidayCalendar):
    """
    NYSE-observed US federal holidays calendar.
    Based on holidays listed at https://www.nyse.com/markets/hours-calendars
    """
    rules = [
        Holiday("New Year's Day",
                month=1,
                day=1,
                observance=sunday_to_monday),
        Holiday('Martin Luther King, Jr. Day',
                month=1,
                day=1,
                offset=WeekOfMonth(week=3, weekday=1)),
        Holiday("Washington's Birthday",
                month=2,
                day=1,
                offset=WeekOfMonth(week=3, weekday=1)),
        GoodFriday,
        USMemorialDay,
        Holiday('Juneteenth',
                month=6,
                day=19,
                observance=sunday_to_monday),
        Holiday('Independence Day',
                month=7,
                day=4,
                observance=sunday_to_monday),
        USLaborDay,
        USThanksgivingDay,
        Holiday('Christmas Day',
                month=12,
                day=25,
                observance=sunday_to_monday),
    ]
