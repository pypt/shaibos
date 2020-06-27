# -*- coding: utf-8 -*-

import os
import dateutil.parser
import unittest
from unittest import mock

from parameterized import parameterized

from shaibos.util.currency import amount_to_words
from shaibos.util.currency import format_currency
from shaibos.util.currency import lb_exchange_rate
from shaibos.util.currency import lb_exchange_rate_download
from shaibos.util.currency import lb_exchange_rate_parse
from shaibos.util.currency import round_to_decimal_places
from shaibos.util.currency import Decimal


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


def enable_www_tests():
    setting = os.environ.get("SHAIBOS_TEST_LB_CURRENCY_WWW", None)
    if setting is None or setting == "0":
        return False
    return True


def get_exchange_data_dir():
    return os.path.join(os.path.dirname(__file__), "currency_data")


def get_reference_exchange_data(date_str):
    path = os.path.join(get_exchange_data_dir(), "lb_{}_expected.xml".format(date_str))
    with open(path, "rb") as reference_f:
        return reference_f.read()


# Reference rates: http://www.lb.lt/exchange/default.asp
class TestLbExchangeRate(unittest.TestCase):

    @parameterized.expand([
        ("2013-01-01"),
        ("2015-01-01"),
    ])
    @unittest.skipIf(not enable_www_tests(), "Tests that make web requests have not been enabled")
    def test_lb_exchange_rate_download(self, date_str):
        date = dateutil.parser.parse(date_str)

        content = lb_exchange_rate_download(date)
        expected_content = get_reference_exchange_data(date_str)
        result_path = os.path.join(get_exchange_data_dir(), "lb_{}_result.xml".format(date_str))

        if content != expected_content:
            with open(result_path, 'wb') as result_f:
                result_f.write(content)

        self.assertEqual(content, expected_content, "The format of exchange rates has changed")

    def test_lb_exchange_rate_known(self):
        date = dateutil.parser.parse('2015-01-01')

        with mock.patch("shaibos.util.currency.lb_exchange_rate_download",
                        side_effect=Exception("Rates should not be downloaded")):
            self.assertEqual(lb_exchange_rate('EUR', 'LTL',
                                              date=date),
                             Decimal('3.4528'))
            self.assertEqual(lb_exchange_rate('LTL', 'EUR',
                                              date=date),
                             Decimal('0.2896'))

    def test_lb_post_eurozone_rates(self):
        content = get_reference_exchange_data('2015-01-01')

        self.assertEqual(lb_exchange_rate_parse('EUR', 'GBP', content), Decimal('0.7789'))
        self.assertTrue(str(lb_exchange_rate_parse('GBP', 'EUR', content)
                            ).startswith('1.2838618'))

    def test_lb_pre_eurozone_rates(self):
        content = get_reference_exchange_data('2013-01-01')

        self.assertEqual(lb_exchange_rate_parse('GBP', 'LTL', content), Decimal('4.2015'))
        self.assertTrue(str(lb_exchange_rate_parse('LTL', 'GBP', content)).startswith('0.2380102'))

    def test_rounding(self):
        rate = Decimal("1.378929950358521787093215665")  # GBP to EUR on 2015-12-15
        self.assertEqual(round_to_decimal_places(number=(Decimal('416.00') * rate), dec_places=2),
                         Decimal('573.63'))

    @parameterized.expand([
        ('USD', 'GBP', '2015-01-01'),  # Unsupported currency
        ('GBP', 'LTL', '2015-01-01'),  # Converting to LTL after Eurozone
        ('GBP', 'EUR', '2013-01-01'),  # converting to EUR before Eurozone
    ])
    def test_unsupported_currency(self, from_currency, to_currency, date_str):
        date = dateutil.parser.parse(date_str)

        with mock.patch("shaibos.util.currency.lb_exchange_rate_download",
                        side_effect=Exception("Rates should not be downloaded")):
            with self.assertRaisesRegex(Exception, r"Only conversions (from|to) / (to|from).*"):
                lb_exchange_rate(from_currency, to_currency, date)
