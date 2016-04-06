# -*- coding: utf-8 -*-
from collections import defaultdict
from decimal import Decimal

import collections

from shaibos.tax.rates import TaxRates
from shaibos.util.currency import round_to_decimal_places, tax_currency, currency_decimal_places
from shaibos.util.log import get_logger
from shaibos.util.unicode_mixin import UnicodeMixin

logger = get_logger()


class AddedTotals(UnicodeMixin):
    """Basic counter of invoice totals."""

    income = Decimal('0.00')
    expenses = Decimal('0.00')
    tax_base = Decimal('0.00')
    sodra_tax_base = Decimal('0.00')
    vsd = Decimal('0.00')
    psd = Decimal('0.00')
    gpm = Decimal('0.00')
    tax = Decimal('0.00')
    profit = Decimal('0.00')

    def __init__(self):
        pass

    def __unicode__(self):
        descr_str = ""
        descr_str += "%(income)s; expenses: %(expenses)s; tax base: %(tax_base)s; SoDra tax base: %(sodra_tax_base)s; "
        descr_str += "VSD: %(vsd)s; PSD: %(psd)s; GPM: %(gpm)s; tax: %(tax)s; profit: %(profit)s"
        return descr_str % {
            'income': self.income,
            'expenses': self.expenses,
            'tax_base': self.tax_base,
            'sodra_tax_base': self.sodra_tax_base,
            'vsd': self.vsd,
            'psd': self.psd,
            'gpm': self.gpm,
            'tax': self.tax,
            'profit': self.profit,
        }

    def __iadd__(self, other):
        self.income += other.income
        self.expenses += other.expenses
        self.tax_base += other.tax_base
        self.sodra_tax_base += other.sodra_tax_base
        self.vsd += other.vsd
        self.psd += other.psd
        self.gpm += other.gpm
        self.tax += other.tax
        self.profit += other.profit
        return self


class CalculatedTotals(AddedTotals):
    """Invoice totals counter that calculates appropriate taxes."""

    countries = set()

    def __init__(self, income, decimal_places, tax_rates):
        super(CalculatedTotals, self).__init__()
        self.income = round_to_decimal_places(Decimal(income), decimal_places)
        self.decimal_places = decimal_places
        self.tax_rates = tax_rates

    def __iadd__(self, other):
        if self.decimal_places != other.decimal_places:
            raise TypeError("Decimal places do not match")
        if self.tax_rates != other.tax_rates:
            raise TypeError("Tax rates do not match")
        self.income += other.income
        return self

    @property
    def expenses(self):
        return round_to_decimal_places(self.income * self.tax_rates.expenses_rate, self.decimal_places)

    @property
    def tax_base(self):
        return self.income - self.expenses

    @property
    def sodra_tax_base(self):
        return round_to_decimal_places(self.tax_base * self.tax_rates.sodra_tax_base, self.decimal_places)

    @property
    def vsd(self):
        return round_to_decimal_places(Decimal(self.sodra_tax_base * self.tax_rates.vsd_rate), self.decimal_places)

    @property
    def psd(self):
        return round_to_decimal_places(Decimal(self.sodra_tax_base * self.tax_rates.psd_rate), self.decimal_places)

    @property
    def gpm(self):
        return round_to_decimal_places(Decimal(self.tax_base * self.tax_rates.gpm_rate), self.decimal_places)

    @property
    def tax(self):
        return self.vsd + self.psd + self.gpm

    @property
    def profit(self):
        return self.income - self.tax

    @property
    def country_count(self):
        return len(self.countries)


def invoice_totals(invoice, year):
    year_tax_currency = tax_currency(year)

    if not invoice.has_been_paid():
        logger.warn("Invoice '%s' hasn't been marked as paid, skipping" % invoice)
        return None

    paid_year = invoice.payment_date()
    if not paid_year.year == year:
        logger.warn("Invoice '%s' hasn't been paid in the year %d, skipping" % (invoice, year))
        return None

    paid_amount = invoice.paid_amount(tax_currency=year_tax_currency)
    totals_per_invoice = CalculatedTotals(
        income=paid_amount,
        decimal_places=currency_decimal_places(year_tax_currency),
        tax_rates=TaxRates.from_defaults(
            vsd_tax_percentage=invoice.seller.vsd_tax_rate,
            gpm_tax_percentage=invoice.activity.gpm_tax_rate
        )
    )

    return totals_per_invoice


def buyer_totals(invoices, year):
    totals_per_buyer = defaultdict(AddedTotals)

    for invoice_number_prefix in invoices:
        for invoice in invoices[invoice_number_prefix]:

            totals_per_invoice = invoice_totals(invoice=invoice, year=year)
            if totals_per_invoice is None:
                continue

            totals_per_buyer[invoice.buyer.__unicode__()] += totals_per_invoice

    # Sort by buyer name
    totals_per_buyer = collections.OrderedDict(sorted(totals_per_buyer.items()))

    return totals_per_buyer


def activity_totals(invoices, year):
    totals_by_activity = {}

    for invoice_number_prefix in invoices:
        for invoice in invoices[invoice_number_prefix]:

            totals_per_invoice = invoice_totals(invoice=invoice, year=year)
            if totals_per_invoice is None:
                continue

            totals_per_invoice.countries.add(invoice.buyer.country_code)
            evrk_code = invoice.activity.evrk_code

            if evrk_code in totals_by_activity:
                totals_by_activity[evrk_code] += totals_per_invoice
            else:
                totals_by_activity[evrk_code] = totals_per_invoice

    # Sort by EVRK code
    totals_by_activity = collections.OrderedDict(sorted(totals_by_activity.items()))

    return totals_by_activity


def tax_totals(invoices, year):
    totals_by_activity = activity_totals(invoices=invoices, year=year)

    # Add totals by activity without recalculating them because that's what VMI does
    totals = AddedTotals()
    for t in totals_by_activity.values():
        totals += t

    return totals


def gpm_percentages(invoices):
    gpm = {}

    for invoice_number_prefix in invoices:
        for invoice in invoices[invoice_number_prefix]:
            evrk_code = invoice.activity.evrk_code
            gpm[evrk_code] = invoice.activity.gpm_tax_rate

    return gpm
