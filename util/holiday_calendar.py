from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday, nearest_workday, USMartinLutherKingJr, \
    USPresidentsDay, GoodFriday, USMemorialDay, USLaborDay, USThanksgivingDay


class MarketHolidayCalendar(AbstractHolidayCalendar):
    """
    NYSE-observed US federal holidays calendar.
    Based on holidays listed at https://www.nyse.com/markets/hours-calendars
    """
    rules = [
        Holiday("New Year's Day", month=1, day=1, observance=nearest_workday),
        USMartinLutherKingJr,
        USPresidentsDay,
        GoodFriday,
        USMemorialDay,
        Holiday('Juneteenth National Independence Day', month=6, day=19, observance=nearest_workday),
        Holiday('Independence Day', month=7, day=4, observance=nearest_workday),
        USLaborDay,
        USThanksgivingDay,
        Holiday('Christmas Day', month=12, day=25, observance=nearest_workday),
    ]
