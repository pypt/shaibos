# -*- coding: utf-8 -*-

from dateutil import parser as dateparser
from nose.tools import assert_raises

from shaibos.util.currency import *


def test_round_to_decimal_places():
    assert round_to_decimal_places(Decimal('0.00'), 2) == Decimal('0.00')
    assert round_to_decimal_places(Decimal('0.001'), 2) == Decimal('0.00')
    assert round_to_decimal_places(Decimal('0.004'), 2) == Decimal('0.00')
    assert round_to_decimal_places(Decimal('0.005'), 2) == Decimal('0.01')
    assert round_to_decimal_places(Decimal('0.009'), 2) == Decimal('0.01')
    assert round_to_decimal_places(Decimal('0.01'), 2) == Decimal('0.01')
    assert round_to_decimal_places(Decimal('0.04'), 2) == Decimal('0.04')
    assert round_to_decimal_places(Decimal('0.05'), 2) == Decimal('0.05')


def test_format_currency():
    amount = Decimal('12345678.90')

    assert format_currency(
        amount=amount,
        currency='LTL',
        language='lt_LT'
    ) == u"12%(nbsp)s345%(nbsp)s678,90%(nbsp)sLt" % {'nbsp': u"\xa0"}
    assert format_currency(
        amount=amount,
        currency='LTL',
        language='en_US'
    ) == u"LTL%(nbsp)s12,345,678.90" % {'nbsp': u"\xa0"}

    assert format_currency(
        amount=amount,
        currency='LTL',
        language='en_GB'
    ) == u"LTL%(nbsp)s12,345,678.90" % {'nbsp': u"\xa0"}

    assert format_currency(
        amount=amount,
        currency='EUR',
        language='lt_LT'
    ) == u"12%(nbsp)s345%(nbsp)s678,90%(nbsp)s€" % {'nbsp': u"\xa0"}
    assert format_currency(amount=amount, currency='EUR', language='en_US') == u"€12,345,678.90"
    assert format_currency(amount=amount, currency='EUR', language='en_GB') == u"€12,345,678.90"

    assert format_currency(
        amount=amount,
        currency='GBP',
        language='lt_LT'
    ) == u"12%(nbsp)s345%(nbsp)s678,90%(nbsp)sGBP" % {'nbsp': u"\xa0"}
    assert format_currency(amount=amount, currency='GBP', language='en_US') == u"£12,345,678.90"
    assert format_currency(amount=amount, currency='GBP', language='en_GB') == u"£12,345,678.90"


def test_amount_to_words():
    assert amount_to_words(amount=Decimal('0.99'), currency='LTL') == u'nulis litų ir 99 ct.'
    assert amount_to_words(amount=Decimal('1.99'), currency='LTL') == u'vienas litas ir 99 ct.'
    assert amount_to_words(amount=Decimal('2.99'), currency='LTL') == u'du litai ir 99 ct.'
    assert amount_to_words(amount=Decimal('10.99'), currency='LTL') == u'dešimt litų ir 99 ct.'
    assert amount_to_words(amount=Decimal('11.99'), currency='LTL') == u'vienuolika litų ir 99 ct.'
    assert amount_to_words(amount=Decimal('21.99'), currency='LTL') == u'dvidešimt vienas litas ir 99 ct.'
    assert amount_to_words(amount=Decimal('29.99'), currency='LTL') == u'dvidešimt devyni litai ir 99 ct.'

    assert amount_to_words(amount=Decimal('0.99'), currency='EUR') == u'nulis eurų ir 99 ct.'
    assert amount_to_words(amount=Decimal('1.99'), currency='EUR') == u'vienas euras ir 99 ct.'
    assert amount_to_words(amount=Decimal('2.99'), currency='EUR') == u'du eurai ir 99 ct.'
    assert amount_to_words(amount=Decimal('10.99'), currency='EUR') == u'dešimt eurų ir 99 ct.'
    assert amount_to_words(amount=Decimal('11.99'), currency='EUR') == u'vienuolika eurų ir 99 ct.'
    assert amount_to_words(amount=Decimal('21.99'), currency='EUR') == u'dvidešimt vienas euras ir 99 ct.'
    assert amount_to_words(amount=Decimal('29.99'), currency='EUR') == u'dvidešimt devyni eurai ir 99 ct.'

    assert amount_to_words(amount=Decimal('0.99'), currency='USD') == u'nulis JAV dolerių ir 99 ¢'
    assert amount_to_words(amount=Decimal('1.99'), currency='USD') == u'vienas JAV doleris ir 99 ¢'
    assert amount_to_words(amount=Decimal('2.99'), currency='USD') == u'du JAV doleriai ir 99 ¢'
    assert amount_to_words(amount=Decimal('10.99'), currency='USD') == u'dešimt JAV dolerių ir 99 ¢'
    assert amount_to_words(amount=Decimal('11.99'), currency='USD') == u'vienuolika JAV dolerių ir 99 ¢'
    assert amount_to_words(amount=Decimal('21.99'), currency='USD') == u'dvidešimt vienas JAV doleris ir 99 ¢'
    assert amount_to_words(amount=Decimal('29.99'), currency='USD') == u'dvidešimt devyni JAV doleriai ir 99 ¢'


# Reference rates: http://www.lb.lt/exchange/default.asp
def test_lb_exchange_rate():
    post_eurozone_date = dateparser.parse('2015-01-01')
    pre_eurozone_date = dateparser.parse('2013-01-01')

    # Known currency rates
    assert lb_exchange_rate(from_currency_code='EUR', to_currency_code='LTL', date=post_eurozone_date) == Decimal(
        '3.4528')
    assert lb_exchange_rate(from_currency_code='LTL', to_currency_code='EUR', date=post_eurozone_date) == Decimal(
        '0.2896')

    # Post-Eurozone rate
    assert lb_exchange_rate(from_currency_code='EUR', to_currency_code='GBP', date=post_eurozone_date) == Decimal(
        '0.7789')
    assert str(lb_exchange_rate(from_currency_code='GBP', to_currency_code='EUR', date=post_eurozone_date)).startswith(
        '1.2838618')

    # Pre-Eurozone rate
    assert lb_exchange_rate(from_currency_code='GBP', to_currency_code='LTL', date=pre_eurozone_date) == Decimal(
        '4.2015')
    assert str(lb_exchange_rate(from_currency_code='LTL', to_currency_code='GBP', date=pre_eurozone_date)).startswith(
        '0.2380102')

    # Rounding errors
    assert round_to_decimal_places(
        number=(Decimal('416.00') * lb_exchange_rate(
            from_currency_code='GBP',
            to_currency_code='EUR',
            date=dateparser.parse('2015-12-15')
        )),
        dec_places=2) == Decimal('573.63')

    # Unsupported currency
    assert_raises(Exception, lb_exchange_rate, 'USD', 'GBP', post_eurozone_date)

    # Converting to LTL after Eurozone
    assert_raises(Exception, lb_exchange_rate, 'GBP', 'LTL', post_eurozone_date)

    # Converting to EUR before Eurozone
    assert_raises(Exception, lb_exchange_rate, 'GBP', 'EUR', pre_eurozone_date)
