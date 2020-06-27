# -*- coding: utf-8 -*-
from decimal import Decimal
import unittest

from shaibos.load.from_yaml import load_invoices_from_yaml_string
from shaibos.tax.totals import invoice_totals, buyer_totals, activity_totals, tax_totals


# noinspection PyPep8Naming
class TestClass(unittest.TestCase):
    test_invoices = None
    test_invoices_year = 2015

    test_invoices_yaml = u"""
---

sellers:
    - &vardenis
        name: "Vardenis Pavardenis"
        vsd_tax_rate: 28.5
        iea_certificate_number: 123456
        iea_certificate_issue_date: 2011-01-03
        personal_number: 38912010123
        address:
            lt_LT: "Vardenio g. 1-2, LT-05229 Vilnius"
            en_US: "Vardenio str. 1-2, LT-05229 Vilnius, Lithuania"
            en_GB: "Vardenio str. 1-2, LT-05229 Vilnius, Lithuania"
        phone: "+37068712345"
#        fax: "+37068712345"
        email: "vardenis.pavardenis@gmail.com"
        bank_credentials:
            account: "LT627300010012345678"
            name:
                lt_LT: "„Swedbank“, AB"
                en_US: "Swedbank, AB"
                en_GB: "Swedbank, AB"
            swift: "HABALT22"


# http://www.lb.lt/ekonomines_veiklos_rusiu_klasifikatorius
activities:
    - &programming
        title: "Kompiuterių programavimo veikla"
        evrk_code: 620100
        gpm_tax_rate: 15
        invoice_number_prefix: "VVP"
        invoice_number_length: 5
    - &software_sales
        title: "Kompiuterių, jų išorinės ir programinės įrangos mažmeninė prekyba specializuotose parduotuvėse"
        evrk_code: 474100
        gpm_tax_rate: 5
        invoice_number_prefix: "VVS"
        invoice_number_length: 5
    - &hosting
        title: "Duomenų apdorojimo, interneto serverių paslaugų (prieglobos) ir susijusi veikla"
        evrk_code: 631100
        gpm_tax_rate: 5
        invoice_number_prefix: "VVH"
        invoice_number_length: 5
    - &misc_sales
        title: "Kita mažmeninė prekyba ne parduotuvėse, kioskuose ar prekyvietėse"
        evrk_code: 479900
        invoice_number_prefix: "VVM"
        invoice_number_length: 5


buyers:
    - &saraskinas
        name: "UAB „Šaraškinas ir co.“"
        address: "Šaraškino g. 3-4, LT-06325 Vilnius"
        company_code: "1234567890"
        vat_payer_code: "LT123456789"
        phone: "+370 5 1234567"
        fax: "+370 5 1234567"
        currency: "EUR"
        languages:
            - "lt_LT"
    - &judaskinas
        name: "UAB „Judaškinas ir co.“"
        address: "Judaškino g. 3-4, LT-06325 Vilnius"
        company_code: "123456789"
        vat_payer_code: "LT12345678"
        phone: "+370 5 123456"
        fax: "+370 5 123456"
        currency: "EUR"
        languages:
            - "lt_LT"

services:
    - &saraskinas_lt_programming
        description: 'Svetainės saraskinas.lt programavimo darbai.'
        measure: hour
    - &saraskinas_app_sales
        description: 'Programos „Šaraškinas“ pardavimas.'
        measure: unit
    - &judaskinas_app_sales
        description: 'Programos „Judaškinas“ pardavimas.'
        measure: unit

# ---

invoices:

    # Basic invoice (15% tax rate)
    - date: 2015-03-31
      seller: *vardenis
      buyer: *saraskinas
      activity: *programming
      items:
          - <<: *saraskinas_lt_programming
            quantity: 6     # hours
            price: 30.00    # per hour
      payment:
          paid: True

    # Another basic invoice (5% tax rate)
    - date: 2015-03-31
      seller: *vardenis
      buyer: *saraskinas
      activity: *software_sales
      items:
          - <<: *saraskinas_app_sales
            quantity: 29    # units
            price: 199.99   # per unit
      payment:
          paid: True

    # Yet another basic invoice (5% tax rate, different client)
    - date: 2015-03-31
      seller: *vardenis
      buyer: *judaskinas
      activity: *software_sales
      items:
          - <<: *judaskinas_app_sales
            quantity: 29    # units
            price: 199.99   # per unit
      payment:
          paid: True

    # Unpaid invoice
    - date: 2015-04-01
      seller: *vardenis
      buyer: *saraskinas
      activity: *programming
      items:
          - <<: *saraskinas_lt_programming
            quantity: 6     # hours
            price: 30.00    # per hour

    # Paid in different currency
    - date: 2015-04-01
      seller: *vardenis
      buyer: *saraskinas
      activity: *programming
      items:
          - <<: *saraskinas_lt_programming
            quantity: 6     # hours
            price: 30.00    # per hour
      payment:
          paid: True
          date: 2015-04-03
          amount: 100.99
          currency: "GBP"

    # Paid later than 2015
    - date: 2015-12-31
      seller: *vardenis
      buyer: *saraskinas
      activity: *programming
      items:
          - <<: *saraskinas_lt_programming
            quantity: 6     # hours
            price: 30.00    # per hour
      payment:
          paid: True
          date: 2016-01-01

    """  # noqa

    def __reset_test_invoices(self):
        self.test_invoices = load_invoices_from_yaml_string(yaml_string=self.test_invoices_yaml)

    def setUp(self):
        self.__reset_test_invoices()

    def test_invoice_totals(self):

        for invoice_number_prefix in self.test_invoices:

            activity_invoices = self.test_invoices[invoice_number_prefix]
            first_invoice = invoice_totals(invoice=activity_invoices[0],
                                           year=self.test_invoices_year)

            if invoice_number_prefix == 'VVS':
                self.assertEqual(first_invoice.income, Decimal('5799.71'))  # 199.99 * 29
                self.assertEqual(first_invoice.expenses, Decimal('1739.91'))  # total * 0.3
                self.assertEqual(first_invoice.tax_base, Decimal('4059.80'))  # total - expenses
                self.assertEqual(first_invoice.sodra_tax_base, Decimal('2029.90'))  # tax_base / 2
                self.assertEqual(first_invoice.vsd, Decimal('578.52'))  # sodra_tax_base * 0.285
                self.assertEqual(first_invoice.psd, Decimal('182.69'))  # sodra_tax_base * 0.09
                self.assertEqual(first_invoice.gpm, Decimal('202.99'))  # tax_base * 0.05
                self.assertEqual(first_invoice.tax, Decimal('964.20'))  # vsd + psd + gpm
                self.assertEqual(first_invoice.profit, Decimal('4835.51'))  # total - tax

            elif invoice_number_prefix == 'VVP':
                self.assertEqual(first_invoice.gpm, Decimal('18.90'))  # tax_base * 0.15

    def test_buyer_totals(self):
        totals_by_buyer = buyer_totals(invoices=self.test_invoices, year=self.test_invoices_year)

        self.assertEqual(len(totals_by_buyer), 2)

        judaskinas = totals_by_buyer[u"UAB „Judaškinas ir co.“"]
        saraskinas = totals_by_buyer[u"UAB „Šaraškinas ir co.“"]

        # 29 * 199.99
        self.assertEqual(judaskinas.income, Decimal("5799.71"))

        # (6 * 30.00) + (29 * 199.99) + (100.99 GBP / 0.73160)
        self.assertEqual(saraskinas.income, Decimal("6117.75"))

        # 5799.71 * 0.7 * 0.05
        self.assertEqual(judaskinas.gpm, Decimal("202.99"))

        # ((6 * 30.00) + (100.99 GBP / 0.73160)) * 0.7 * 0.15
        # +
        # (29 * 199.99) * 0.7 * 0.05
        self.assertEqual(saraskinas.gpm, Decimal("236.38"))

    def test_activity_totals(self):

        totals_by_activity = activity_totals(invoices=self.test_invoices,
                                             year=self.test_invoices_year)

        gpm_5_percent = totals_by_activity[474100]
        gpm_15_percent = totals_by_activity[620100]

        # (29 * 199.99) + (29 * 199.99)
        self.assertEqual(gpm_5_percent.income, Decimal("11599.42"))

        # (6 * 30.00) + (100.99 GBP / 0.73160)
        self.assertEqual(gpm_15_percent.income, Decimal("318.04"))

        # 11599.42 * 0.7 * 0.05
        self.assertEqual(gpm_5_percent.gpm, Decimal("405.98"))

        # 318.04 * 0.7 * 0.15
        self.assertEqual(gpm_15_percent.gpm, Decimal("33.39"))

    def test_tax_totals(self):

        totals = tax_totals(invoices=self.test_invoices, year=self.test_invoices_year)

        # 11599.42 + 318.04
        self.assertEqual(totals.income, Decimal("11917.46"))

        # (11599.42 * 0.3) + (318.04 * 0.3)
        self.assertEqual(totals.expenses, Decimal("3575.24"))

        # (11599.42 - (11599.42 * 0.3)) + (318.04 - (318.04 * 0.3))
        self.assertEqual(totals.tax_base, Decimal("8342.22"))

        # (11599.42 - (11599.42 * 0.3)) * 0.5 + (318.04 - ((318.04 * 0.3))) * 0.5
        # (expenses for each type is rounded)
        self.assertEqual(totals.sodra_tax_base, Decimal("4171.12"))

        # 4171.12 * 0.285
        self.assertEqual(totals.vsd, Decimal("1188.77"))

        # 4171.12 * 0.09
        self.assertEqual(totals.psd, Decimal("375.40"))

        # 405.98 + 33.39
        self.assertEqual(totals.gpm, Decimal("439.37"))

        # 1188.77 + 375.40 + 439.37
        self.assertEqual(totals.tax, Decimal("2003.54"))

        # 11917.46 - 2003.54
        self.assertEqual(totals.profit, Decimal("9913.92"))
