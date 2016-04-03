# -*- coding: utf-8 -*-

import babel
import decimal

import re
from money import Money

import suds.client
from num2words import num2words

__decimal_places = {
    'EUR': 2,
    'LTL': 2,
    'USD': 2,
    'GBP': 2,
}


class CurrencyStrings(object):
    def __init__(self, singular_nominative, plural_nominative, plural_genitive, subunit):
        self.singular_nominative = singular_nominative
        self.plural_nominative = plural_nominative
        self.plural_genitive = plural_genitive
        self.subunit = subunit


__num2words_strings = {
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
}


def tax_currency(year):
    if year <= 2014:
        return 'LTL'
    else:
        return 'EUR'


def decimal_places(currency):
    return __decimal_places[currency.upper()]


def num2words_strings(currency):
    return __num2words_strings[currency.upper()]


def format_currency(amount, currency, language):
    locale = babel.Locale.parse(language)
    money = Money(amount=float(amount), currency=str(currency.upper()))
    formatted_amount = money.format(locale=language, pattern=locale.currency_formats.get('accounting'))

    if currency.upper() == 'LTL':
        nbsp = u"\xa0"
        regex_nbsp_or_space = "(" + nbsp + "|\s)"
        if language == 'lt_LT':
            # "12 345 678,90 LTL" -> "12 345 678,90 Lt"
            formatted_amount = re.sub(
                pattern='(?P<last_digit>\d)' + regex_nbsp_or_space + 'LTL$',
                repl='\g<last_digit>' + nbsp + 'Lt',
                string=formatted_amount
            )
        elif language.startswith('en_'):
            # "Lt12,345,678.90" -> "LTL 12,345,678.90"
            # (https://en.wikipedia.org/wiki/ISO_4217#Position_of_ISO_4217_code_in_amounts)
            formatted_amount = re.sub(
                pattern='Lt(?P<first_digit>\d)',
                repl='LTL' + nbsp + '\g<first_digit>',
                string=formatted_amount
            )

    return formatted_amount


def amount_to_words(amount, currency):
    amount = round_to_decimal_places(amount, decimal_places(currency))
    integer_part = int(amount)
    float_part = int(amount % decimal.Decimal('1') * decimal.Decimal('100'))

    strings = num2words_strings(currency)

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

    return u'%s %s ir %d %s' % (
        num2words(integer_part, lang='lt'),
        currency_string,
        float_part,
        strings.subunit
    )


def round_to_decimal_places(number, dec_places):
    return decimal.Decimal(number.quantize(decimal.Decimal('.' + '0' * dec_places), rounding=decimal.ROUND_HALF_UP))


def lb_exchange_rate(from_currency_code, to_currency_code, date):
    """
    Usage:

    print lb_exchange_rate(from_currency_code='USD', to_currency_code='LTL', date=dateutil.parser.parse('2013-01-01'))

    https://www.lb.lt/webservices/FxRates/
    """
    from_currency_code == from_currency_code.upper()
    to_currency_code = to_currency_code.upper()

    # Don't bother the server if we already know the rate
    if date.year >= 2015:
        if from_currency_code == 'EUR' and to_currency_code == 'LTL':
            return 1.0 * 3.4528
        elif from_currency_code == 'LTL' and to_currency_code == 'EUR':
            return 1.0 / 3.4528
        else:
            raise TypeError('You should be paying taxes in either LTL or EUR')

    api_eur_endpoint = "https://www.lb.lt/webservices/FxRates/FxRates.asmx"
    soap_client = suds.client.Client(api_eur_endpoint + '?wsdl')
    soap_rate = soap_client.service.getFxRates(tp='LT', dt=date)

    for rate in soap_rate.FxRates.FxRate:
        if len(rate.CcyAmt) != 2:
            raise Exception('Only two currencies per listing are expected')
        first_currency = rate.CcyAmt[0].Ccy
        first_amount = float(rate.CcyAmt[0].Amt)
        second_currency = rate.CcyAmt[1].Ccy
        second_amount = float(rate.CcyAmt[1].Amt)

        if first_currency == from_currency_code and second_currency == to_currency_code:
            return second_amount / first_amount
        elif first_currency == to_currency_code and second_currency == from_currency_code:
            return first_amount / second_amount

    raise RuntimeError("Currency rate between %s and %s was not found" % (from_currency_code, to_currency_code))
