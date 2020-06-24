# -*- coding: utf-8 -*-

from decimal import Decimal

percent_multiplier = Decimal('0.01')


class TaxRates(object):
    def __init__(self, expenses_rate, sodra_tax_base, vsd_rate, psd_rate, gpm_rate):
        self.expenses_rate = expenses_rate
        self.sodra_tax_base = sodra_tax_base
        self.vsd_rate = vsd_rate
        self.psd_rate = psd_rate
        self.gpm_rate = gpm_rate

    def __eq__(self, other):
        if isinstance(other, TaxRates):
            return (self.expenses_rate == other.expenses_rate and
                    self.sodra_tax_base == other.sodra_tax_base and
                    self.vsd_rate == other.vsd_rate and self.psd_rate == other.psd_rate and
                    self.gpm_rate == other.gpm_rate)
        return NotImplemented

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

    @classmethod
    def from_defaults(cls, vsd_tax_percentage, gpm_tax_percentage):
        return TaxRates(
            expenses_rate=default_expenses_rate(),
            sodra_tax_base=default_sodra_tax_base(),
            vsd_rate=Decimal(vsd_tax_percentage) * percent_multiplier,
            psd_rate=default_psd_rate(),
            gpm_rate=Decimal(gpm_tax_percentage) * percent_multiplier,
        )


def default_expenses_rate():
    # 30%
    return Decimal('30') * percent_multiplier


def default_sodra_tax_base():
    # 50%
    return Decimal('50') * percent_multiplier


def default_psd_rate():
    # 9%
    return Decimal('9') * percent_multiplier


def default_income_type_code():
    """Pajamų rūšies kodas"""
    return 93


def evrk_code_to_activity_type_code(evrk_code):
    return int(str(evrk_code)[:2])
