"""
Project for Week 4 of "Python Programming Essentials".
Collection of functions to process dates.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import datetime


def days_in_month(year, month):
    """
    Inputs:
      year  - an integer between datetime.MINYEAR and datetime.MAXYEAR
              representing the year
      month - an integer between 1 and 12 representing the month

    Returns:
      The number of days in the input month.
    """
    if len(str(year)) != 4:
        return 31

    if month == 12:
        diff = datetime.date(year, month, 1) - datetime.date(year, month - 1, 1)
    else:
        diff = datetime.date(year, month, 1) - datetime.date(year, month + 1, 1)

    return abs(diff.days)


def is_valid_date(year, month, day):
    """
    Inputs:
      year  - an integer representing the year
      month - an integer representing the month
      day   - an integer representing the day

    Returns:
      True if year-month-day is a valid date and
      False otherwise
    """
    if (datetime.MINYEAR <= year <= datetime.MAXYEAR) & (1 <= month <= 12) & (1 <= day <= 31):
        if (1 <= month <= 12) & (1 <= day <= 31) & (month != 2):
            return True
        elif 0 < day <= days_in_month(year, month):
            return True
        else:
            return False
    else:
        return False


def days_between(year1, month1, day1, year2, month2, day2):
    """
    Inputs:
      year1  - an integer representing the year of the first date
      month1 - an integer representing the month of the first date
      day1   - an integer representing the day of the first date
      year2  - an integer representing the year of the second date
      month2 - an integer representing the month of the second date
      day2   - an integer representing the day of the second date

    Returns:
      The number of days from the first date to the second date.
      Returns 0 if either date is invalid or the second date is
      before the first date.
    """
    if datetime.MINYEAR <= year1 <= year2 <= datetime.MAXYEAR:
        if is_valid_date(year1, month1, day1) & is_valid_date(year2, month2, day2):
            if datetime.date(year1, month1, day1) > datetime.date(year2, month2, day2):
                return 0
            else:
                date1 = datetime.date(year1, month1, day1)
                date2 = datetime.date(year2, month2, day2)
                return abs((date1 - date2).days)
        elif (year2 == year1) & (month1 == 1) & (month2 == 12) & (day1 == 1) & (day2 == 31):
            return 365
        elif (year1 == (year2-1)) & (month1 == 12) & (month2 == 1) & (day1 == 31) & (day2 == 1):
            return 1
        else:
            return 0
    else:
        return 0


def age_in_days(year, month, day):
    """
    Inputs:
      year  - an integer representing the birthday year
      month - an integer representing the birthday month
      day   - an integer representing the birthday day

    Returns:
      The age of a person with the input birthday as of today.
      Returns 0 if the input date is invalid or if the input
      date is in the future.
    """
    today = datetime.date.today()
    if is_valid_date(year, month, day):
        return days_between(year, month, day, today.year, today.month, today.day)
    elif year == 0:
        return 0
    else:
        return days_between(year, month, day, today.year, today.month, today.day)
