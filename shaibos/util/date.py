# -*- coding: utf-8 -*-

import babel.dates

def format_date(date, locale):
    return babel.dates.format_date(date, locale=locale, format='long')
