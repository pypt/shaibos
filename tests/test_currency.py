# -*- coding: utf-8 -*-

from dateutil import parser as dateparser
import unittest

from shaibos.util.currency import *

class TestRound(unittest.TestCase):

    def tests(self):
        self.assertEqual(round_to_decimal_places(Decimal('0.00'), 2), Decimal('0.00'))
        self.assertEqual(round_to_decimal_places(Decimal('0.001'), 2), Decimal('0.00'))
        self.assertEqual(round_to_decimal_places(Decimal('0.004'), 2), Decimal('0.00'))
        self.assertEqual(round_to_decimal_places(Decimal('0.005'), 2), Decimal('0.01'))
        self.assertEqual(round_to_decimal_places(Decimal('0.009'), 2), Decimal('0.01'))
        self.assertEqual(round_to_decimal_places(Decimal('0.01'), 2), Decimal('0.01'))
        self.assertEqual(round_to_decimal_places(Decimal('0.04'), 2), Decimal('0.04'))
        self.assertEqual(round_to_decimal_places(Decimal('0.05'), 2), Decimal('0.05'))


class TestFormatCurrency(unittest.TestCase):
    def test_format_currency(self):
        amount = Decimal('12345678.90')

        self.assertEqual(format_currency(
            amount=amount,
            currency='LTL',
            language='lt_LT'
        ), u"12%(nbsp)s345%(nbsp)s678,90%(nbsp)sLt" % {'nbsp': u"\xa0"})

        self.assertEqual(format_currency(
            amount=amount,
            currency='LTL',
            language='en_US'
        ), u"LTL%(nbsp)s12,345,678.90" % {'nbsp': u"\xa0"})

        self.assertEqual(format_currency(
            amount=amount,
            currency='LTL',
            language='en_GB'
        ), u"LTL%(nbsp)s12,345,678.90" % {'nbsp': u"\xa0"})

        self.assertEqual(format_currency(
            amount=amount,
            currency='EUR',
            language='lt_LT'
        ), u"12%(nbsp)s345%(nbsp)s678,90%(nbsp)s€" % {'nbsp': u"\xa0"})

        self.assertEqual(format_currency(amount=amount, currency='EUR',
                                         language='en_US'),
                         u"€12,345,678.90")
        self.assertEqual(format_currency(amount=amount, currency='EUR',
                                         language='en_GB'),
                         u"€12,345,678.90")

        self.assertEqual(format_currency(
            amount=amount,
            currency='GBP',
            language='lt_LT'
        ), u"12%(nbsp)s345%(nbsp)s678,90%(nbsp)sGBP" % {'nbsp': u"\xa0"})

        self.assertEqual(format_currency(amount=amount, currency='GBP',
                                         language='en_US'), u"£12,345,678.90")
        self.assertEqual(format_currency(amount=amount, currency='GBP',
                                         language='en_GB'), u"£12,345,678.90")


class TestAmountToWords(unittest.TestCase):
    def test_LTL_lt(self):
        self.assertEqual(amount_to_words(amount=Decimal('0.99'),
                                         currency='LTL',
                                         locale='lt_LT'),
                         u'nulis litų ir 99 ct.')
        self.assertEqual(amount_to_words(amount=Decimal('1.99'),
                                         currency='LTL',
                                         locale='lt_LT'),
                         u'vienas litas ir 99 ct.')
        self.assertEqual(amount_to_words(amount=Decimal('2.99'),
                                         currency='LTL',
                                         locale='lt_LT'),
                         u'du litai ir 99 ct.')
        self.assertEqual(amount_to_words(amount=Decimal('10.99'),
                                         currency='LTL',
                                         locale='lt_LT'),
                         u'dešimt litų ir 99 ct.')
        self.assertEqual(amount_to_words(amount=Decimal('11.99'),
                                         currency='LTL',
                                         locale='lt_LT'),
                         u'vienuolika litų ir 99 ct.')
        self.assertEqual(amount_to_words(amount=Decimal('21.99'),
                                         currency='LTL',
                                         locale='lt_LT'),
                         u'dvidešimt vienas litas ir 99 ct.')
        self.assertEqual(amount_to_words(amount=Decimal('29.99'),
                                         currency='LTL',
                                         locale='lt_LT'),
                         u'dvidešimt devyni litai ir 99 ct.')

    def test_EUR_lt(self):
        self.assertEqual(amount_to_words(amount=Decimal('0.99'),
                                         currency='EUR',
                                         locale='lt_LT'),
                         u'nulis eurų ir 99 ct.')
        self.assertEqual(amount_to_words(amount=Decimal('1.99'),
                                         currency='EUR',
                                         locale='lt_LT'),
                         u'vienas euras ir 99 ct.')
        self.assertEqual(amount_to_words(amount=Decimal('2.99'),
                                         currency='EUR',
                                         locale='lt_LT'),
                         u'du eurai ir 99 ct.')
        self.assertEqual(amount_to_words(amount=Decimal('10.99'),
                                         currency='EUR',
                                         locale='lt_LT'),
                         u'dešimt eurų ir 99 ct.')
        self.assertEqual(amount_to_words(amount=Decimal('11.99'),
                                         currency='EUR',
                                         locale='lt_LT'),
                         u'vienuolika eurų ir 99 ct.')
        self.assertEqual(amount_to_words(amount=Decimal('21.99'),
                                         currency='EUR',
                                         locale='lt_LT'),
                         u'dvidešimt vienas euras ir 99 ct.')
        self.assertEqual(amount_to_words(amount=Decimal('29.99'),
                                         currency='EUR',
                                         locale='lt_LT'),
                         u'dvidešimt devyni eurai ir 99 ct.')

    def test_USD_lt(self):
        self.assertEqual(amount_to_words(amount=Decimal('0.99'),
                                         currency='USD',
                                         locale='lt_LT'),
                         u'nulis JAV dolerių ir 99 ¢')
        self.assertEqual(amount_to_words(amount=Decimal('1.99'),
                                         currency='USD',
                                         locale='lt_LT'),
                         u'vienas JAV doleris ir 99 ¢')
        self.assertEqual(amount_to_words(amount=Decimal('2.99'),
                                         currency='USD',
                                         locale='lt_LT'),
                         u'du JAV doleriai ir 99 ¢')
        self.assertEqual(amount_to_words(amount=Decimal('10.99'),
                                         currency='USD',
                                         locale='lt_LT'),
                         u'dešimt JAV dolerių ir 99 ¢')
        self.assertEqual(amount_to_words(amount=Decimal('11.99'),
                                         currency='USD',
                                         locale='lt_LT'),
                         u'vienuolika JAV dolerių ir 99 ¢')
        self.assertEqual(amount_to_words(amount=Decimal('21.99'),
                                         currency='USD',
                                         locale='lt_LT'),
                         u'dvidešimt vienas JAV doleris ir 99 ¢')
        self.assertEqual(amount_to_words(amount=Decimal('29.99'),
                                         currency='USD',
                                         locale='lt_LT'),
                         u'dvidešimt devyni JAV doleriai ir 99 ¢')


    def test_LTL_en(self):
        self.assertEqual(amount_to_words(amount=Decimal('0.99'),
                                         currency='LTL',
                                         locale='en_US'),
                         u'zero litas and 99 ct.')

        self.assertEqual(amount_to_words(amount=Decimal('1.99'),
                                         currency='LTL',
                                         locale='en_US'),
                         u'one litas and 99 ct.')
        self.assertEqual(amount_to_words(amount=Decimal('2.99'),
                                         currency='LTL',
                                         locale='en_US'),
                         u'two litas and 99 ct.')
        self.assertEqual(amount_to_words(amount=Decimal('10.99'),
                                         currency='LTL',
                                         locale='en_US'),
                         u'ten litas and 99 ct.')
        self.assertEqual(amount_to_words(amount=Decimal('11.99'),
                                         currency='LTL',
                                         locale='en_US'),
                         u'eleven litas and 99 ct.')
        self.assertEqual(amount_to_words(amount=Decimal('21.99'),
                                         currency='LTL',
                                         locale='en_US'),
                         u'twenty-one litas and 99 ct.')
        self.assertEqual(amount_to_words(amount=Decimal('29.99'),
                                         currency='LTL',
                                         locale='en_US'),
                         u'twenty-nine litas and 99 ct.')

    def test_EUR_en(self):
        self.assertEqual(amount_to_words(amount=Decimal('0.99'),
                                         currency='EUR',
                                         locale='en_US'),
                         u'zero euro and 99 ct.')
        self.assertEqual(amount_to_words(amount=Decimal('1.99'),
                                         currency='EUR',
                                         locale='en_US'),
                         u'one euro and 99 ct.')
        self.assertEqual(amount_to_words(amount=Decimal('2.99'),
                                         currency='EUR',
                                         locale='en_US'),
                         u'two euro and 99 ct.')
        self.assertEqual(amount_to_words(amount=Decimal('10.99'),
                                         currency='EUR',
                                         locale='en_US'),
                         u'ten euro and 99 ct.')
        self.assertEqual(amount_to_words(amount=Decimal('11.99'),
                                         currency='EUR',
                                         locale='en_US'),
                         u'eleven euro and 99 ct.')
        self.assertEqual(amount_to_words(amount=Decimal('21.99'),
                                         currency='EUR',
                                         locale='en_US'),
                         u'twenty-one euro and 99 ct.')
        self.assertEqual(amount_to_words(amount=Decimal('29.99'),
                                         currency='EUR',
                                         locale='en_US'),
                         u'twenty-nine euro and 99 ct.')

    def test_USD_en(self):
        self.assertEqual(amount_to_words(amount=Decimal('0.99'),
                                         currency='USD',
                                         locale='en_US'),
                         u'zero US dollars and 99 ¢')
        self.assertEqual(amount_to_words(amount=Decimal('1.99'),
                                         currency='USD',
                                         locale='en_US'),
                         u'one US dollar and 99 ¢')
        self.assertEqual(amount_to_words(amount=Decimal('2.99'),
                                         currency='USD',
                                         locale='en_US'),
                         u'two US dollars and 99 ¢')
        self.assertEqual(amount_to_words(amount=Decimal('10.99'),
                                         currency='USD',
                                         locale='en_US'),
                         u'ten US dollars and 99 ¢')
        self.assertEqual(amount_to_words(amount=Decimal('11.99'),
                                         currency='USD',
                                         locale='en_US'),
                         u'eleven US dollars and 99 ¢')
        self.assertEqual(amount_to_words(amount=Decimal('21.99'),
                                         currency='USD',
                                         locale='en_US'),
                         u'twenty-one US dollar and 99 ¢')
        self.assertEqual(amount_to_words(amount=Decimal('29.99'),
                                         currency='USD',
                                         locale='en_US'),
                         u'twenty-nine US dollars and 99 ¢')


# Reference rates: http://www.lb.lt/exchange/default.asp
class TestLbExchangeRate(unittest.TestCase):

    def test_lb_exchange_rate(self):
        post_eurozone_date = dateparser.parse('2015-01-01')
        pre_eurozone_date = dateparser.parse('2013-01-01')

        # Known currency rates
        self.assertEqual(lb_exchange_rate(from_currency_code='EUR',
                                          to_currency_code='LTL',
                                          date=post_eurozone_date),
                         Decimal('3.4528'))
        self.assertEqual(lb_exchange_rate(from_currency_code='LTL',
                                          to_currency_code='EUR',
                                          date=post_eurozone_date),
                         Decimal('0.2896'))

        # Post-Eurozone rate
        self.assertEqual(lb_exchange_rate(from_currency_code='EUR',
                                          to_currency_code='GBP',
                                          date=post_eurozone_date),
                         Decimal('0.7789'))
        self.assertTrue(str(lb_exchange_rate(from_currency_code='GBP',
                                             to_currency_code='EUR',
                                             date=post_eurozone_date)).startswith('1.2838618'))

        # Pre-Eurozone rate
        self.assertEqual(lb_exchange_rate(from_currency_code='GBP',
                                          to_currency_code='LTL',
                                          date=pre_eurozone_date),
                         Decimal('4.2015'))
        self.assertTrue(str(lb_exchange_rate(from_currency_code='LTL',
                                             to_currency_code='GBP',
                                             date=pre_eurozone_date)).startswith('0.2380102'))

        # Rounding errors
        self.assertEqual(round_to_decimal_places(
            number=(Decimal('416.00') * lb_exchange_rate(
                from_currency_code='GBP',
                to_currency_code='EUR',
                date=dateparser.parse('2015-12-15')
            )),
            dec_places=2), Decimal('573.63'))

        # Unsupported currency
        with self.assertRaises(Exception):
            lb_exchange_rate('USD', 'GBP', post_eurozone_date)

        # Converting to LTL after Eurozone
        with self.assertRaises(Exception):
            lb_exchange_rate('GBP', 'LTL', post_eurozone_date)

        # Converting to EUR before Eurozone
        with self.assertRaises(Exception):
            lb_exchange_rate('GBP', 'EUR', pre_eurozone_date)
