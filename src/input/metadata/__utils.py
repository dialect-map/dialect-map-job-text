# -*- coding: utf-8 -*-

import pytz

from datetime import datetime


def str_to_datetime(date: str, fmt: str) -> datetime:
    """
    Parses a string date into a Datetime object preserving the timezone (%Z)
    :param date: string date to parse
    :param fmt: string date format
    :return: Datetime object
    """

    # Extracting the timezone out of the string
    dt = date[:-3].strip()
    tz = date[-3:].strip()

    # Pruning the timezone out of the format
    fmt = fmt[:-3]

    off_date = datetime.strptime(dt, fmt)
    off_date = off_date.replace(tzinfo=pytz.timezone(tz))

    return off_date
