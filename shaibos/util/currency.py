# -*- coding: utf-8 -*-

import functools
import re

import babel
from decimal import Decimal, ROUND_HALF_UP

import datetime
import requests
from lxml import etree

from money import Money

from num2words import num2words

__decimal_places = {
    'EUR': 2,
    'LTL': 2,
    'USD': 2,
    'GBP': 2,
}


class CurrencyStrings:
    def __init__(self, singular_nominative, plural_nominative, plural_genitive, subunit):
        self.singular_nominative = singular_nominative
        self.plural_nominative = plural_nominative
        self.plural_genitive = plural_genitive
        self.subunit = subunit


__num2words_strings = {
    'lt': {
        'EUR': CurrencyStrings(
            singular_nominative=u'euras',
            plural_nominative=u'eurai',
            plural_genitive=u'eurų',
            subunit=u'ct.',
        ),
        'LTL': CurrencyStrings(
            singular_nominative=u'litas',
            plural_nominative=u'litai',
            plural_genitive=u'litų',
            subunit=u'ct.',
        ),
        'USD': CurrencyStrings(
            singular_nominative=u'JAV doleris',
            plural_nominative=u'JAV doleriai',
            plural_genitive=u'JAV dolerių',
            subunit=u'¢',
        ),
        'GBP': CurrencyStrings(
            singular_nominative=u'svaras sterlingas',
            plural_nominative=u'svarai sterlingai',
            plural_genitive=u'svarų sterlingų',
            subunit=u'p.',
        ),
    },
    'en': {
        'EUR': CurrencyStrings(
            singular_nominative=u'euro',
            plural_nominative=u'euro',
            plural_genitive=u'euro',
            subunit=u'ct.',
        ),
        'LTL': CurrencyStrings(
            singular_nominative=u'litas',
            plural_nominative=u'litas',
            plural_genitive=u'litas',
            subunit=u'ct.',
        ),
        'USD': CurrencyStrings(
            singular_nominative=u'US dollar',
            plural_nominative=u'US dollars',
            plural_genitive=u'US dollars',
            subunit=u'¢',
        ),
        'GBP': CurrencyStrings(
            singular_nominative=u'pound sterling',
            plural_nominative=u'pound sterling',
            plural_genitive=u'pound sterling',
            subunit=u'p.',
        ),
    },
}


def tax_currency(year):
    if year <= 2014:
        return 'LTL'
    return 'EUR'


def currency_decimal_places(currency):
    return __decimal_places[currency.upper()]


def num2words_strings(locale, currency):
    lang = locale.split('_')[0]
    return __num2words_strings[lang][currency.upper()]


def format_currency(amount, currency, language):
    locale = babel.Locale.parse(language)
    money = Money(amount=float(amount), currency=str(currency.upper()))
    formatted_amount = money.format(locale=language,
                                    pattern=locale.currency_formats.get('accounting'))

    if currency.upper() == 'LTL':
        nbsp = u"\xa0"
        regex_nbsp_or_space = "(" + nbsp + r"|\s)"
        if language == 'lt_LT':
            # "12 345 678,90 LTL" -> "12 345 678,90 Lt"
            formatted_amount = re.sub(
                pattern=r'(?P<last_digit>\d)' + regex_nbsp_or_space + 'LTL$',
                repl=r'\g<last_digit>' + nbsp + 'Lt',
                string=formatted_amount
            )
        elif language.startswith('en_'):
            # "Lt12,345,678.90" -> "LTL 12,345,678.90"
            # (https://en.wikipedia.org/wiki/ISO_4217#Position_of_ISO_4217_code_in_amounts)
            formatted_amount = re.sub(
                pattern=r'(?:Lt|LTL)(?P<first_digit>\d)',
                repl='LTL' + nbsp + r'\g<first_digit>',
                string=formatted_amount
            )

    return formatted_amount


def __integer_part(decimal_number):
    return int(decimal_number)


def __fractional_part(decimal_number):
    if decimal_number < Decimal('0'):
        raise Exception("Negative numbers are not supported")
    fraction = decimal_number % Decimal('1')
    str_fraction = str(fraction)
    if str_fraction == "0":
        return 0
    zero_prefix = "0."
    if not str_fraction.startswith(zero_prefix):
        raise Exception("Unknown number format: %s" % str_fraction)
    return int(str_fraction[len(zero_prefix):])


def amount_to_words(amount, currency, locale):
    amount = round_to_decimal_places(amount, currency_decimal_places(currency))
    integer_part = __integer_part(amount)
    float_part = __fractional_part(amount)

    strings = num2words_strings(locale, currency)

    last_two_digits = int(amount % 100)
    if 11 <= last_two_digits <= 20:
        currency_string = strings.plural_genitive
    else:
        last_digit = int(amount % 10)
        if last_digit == 1:
            currency_string = strings.singular_nominative
        elif last_digit == 0:
            currency_string = strings.plural_genitive
        else:
            currency_string = strings.plural_nominative

    sep_map = {
        'lt_LT': 'ir',
        'en_US': 'and',
        'en_GB': 'and',
    }
    if locale not in sep_map:
        raise NotImplementedError()

    sep_string = sep_map[locale]
    return u'%s %s %s %d %s' % (
        num2words(integer_part, lang=locale),
        currency_string,
        sep_string,
        float_part,
        strings.subunit
    )


def round_to_decimal_places(number, dec_places):
    return Decimal(number.quantize(Decimal('.' + '0' * dec_places), rounding=ROUND_HALF_UP))


def lb_exchange_rate_parse(from_currency_code, to_currency_code, response_content):
    response_xml = etree.fromstring(response_content)
    namespaces = {'lb': response_xml.nsmap[None]}
    if not response_xml.tag.endswith("FxRates"):
        raise Exception("Invalid response, root element is not 'FxRates'")

    rate = None
    for currency_rates in response_xml.xpath('/lb:FxRates/lb:FxRate', namespaces=namespaces):
        currencies = currency_rates.xpath('lb:CcyAmt', namespaces=namespaces)
        if len(currencies) != 2:
            raise Exception('Only two currencies per listing are expected')

        first_currency = currencies[0].xpath('lb:Ccy', namespaces=namespaces)[0].text
        first_amount = Decimal(currencies[0].xpath('lb:Amt', namespaces=namespaces)[0].text)
        second_currency = currencies[1].xpath('lb:Ccy', namespaces=namespaces)[0].text
        second_amount = Decimal(currencies[1].xpath('lb:Amt', namespaces=namespaces)[0].text)

        if first_currency == from_currency_code and second_currency == to_currency_code:
            rate = second_amount / first_amount
        elif first_currency == to_currency_code and second_currency == from_currency_code:
            rate = first_amount / second_amount

        if rate:
            break

    if rate is None:
        raise Exception("Currency rate between {} and {} was not found".format(from_currency_code,
                                                                               to_currency_code))

    return rate


def lb_exchange_rate_download(date):
    # note that we may get data for a different date than `date` if currency exchange rates were
    # not published on `date`. This happens on e.g. 2015-01-01.

    exchange_tax_currency = tax_currency(date.year)

    # API supports SOAP but there's no decent SOAP client library for Python at the moment
    lb_currency_rates_api_endpoint = "https://www.lb.lt/webservices/FxRates/FxRates.asmx/getFxRates"
    response = requests.get(lb_currency_rates_api_endpoint, params={
        'tp': 'LT' if exchange_tax_currency == 'LTL' else 'EU',
        'dt': date.isoformat(),
    })

    return response.content


@functools.lru_cache(maxsize=None)
def lb_exchange_rate(from_currency_code, to_currency_code, date):
    """
    Usage:

    print(lb_exchange_rate(from_currency_code='USD', to_currency_code='LTL',
                           date=dateutil.parser.parse('2013-01-01')))

    https://www.lb.lt/webservices/FxRates/
    """

    if isinstance(date, datetime.datetime):
        date = date.date()

    from_currency_code == from_currency_code.upper()
    to_currency_code = to_currency_code.upper()
    exchange_tax_currency = tax_currency(date.year)

    supported_currencies = {'EUR', 'LTL'}
    if from_currency_code not in supported_currencies and \
            to_currency_code not in supported_currencies:
        raise Exception('Only conversions from / to ' + ','.join(supported_currencies) +
                        ' are supported')

    if exchange_tax_currency == 'EUR':
        if 'EUR' not in {from_currency_code, to_currency_code}:
            raise Exception('Only conversions to / from EUR in year %d are supported' % date.year)
    if exchange_tax_currency == 'LTL':
        if 'LTL' not in {from_currency_code, to_currency_code}:
            raise Exception('Only conversions to / from LTL in year %d are supported' % date.year)

    # Don't bother the server if we already know the rate
    if exchange_tax_currency == 'EUR':
        if from_currency_code == 'EUR' and to_currency_code == 'LTL':
            return Decimal('3.4528')
        if from_currency_code == 'LTL' and to_currency_code == 'EUR':
            return Decimal('0.2896')

    response_content = lb_exchange_rate_download(date)

    return lb_exchange_rate_parse(from_currency_code, to_currency_code, response_content)
