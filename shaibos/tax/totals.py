# -*- coding: utf-8 -*-

import decimal

from shaibos.util.currency import round_to_decimal_places


class StaticTotals(object):
    """Basic counter of invoice totals."""

    income = decimal.Decimal('0.00')
    expenses = decimal.Decimal('0.00')
    tax_base = decimal.Decimal('0.00')
    sodra_tax_base = decimal.Decimal('0.00')
    vsd = decimal.Decimal('0.00')
    psd = decimal.Decimal('0.00')
    gpm = decimal.Decimal('0.00')
    tax = decimal.Decimal('0.00')
    profit = decimal.Decimal('0.00')

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

    def __str__(self):
        return self.__unicode__().encode('utf-8')

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


class DynamicTotals(StaticTotals):
    """Invoice totals counter that calculates appropriate taxes."""

    def __init__(self, income, decimal_places, tax_rates):
        super(DynamicTotals, self).__init__()
        self.income = round_to_decimal_places(decimal.Decimal(income), decimal_places)
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
        return round_to_decimal_places(decimal.Decimal(self.sodra_tax_base * self.tax_rates.vsd_rate),
                                       self.decimal_places)

    @property
    def psd(self):
        return round_to_decimal_places(decimal.Decimal(self.sodra_tax_base * self.tax_rates.psd_rate),
                                       self.decimal_places)

    @property
    def gpm(self):
        return round_to_decimal_places(decimal.Decimal(self.tax_base * self.tax_rates.gpm_rate), self.decimal_places)

    @property
    def tax(self):
        return self.vsd + self.psd + self.gpm

    @property
    def profit(self):
        return self.income - self.tax
