# -*- coding: utf-8 -*-

from decimal import Decimal

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
