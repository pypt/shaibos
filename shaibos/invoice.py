# -*- coding: utf-8 -*-

from decimal import Decimal
from collections import defaultdict

from shaibos.util.currency import amount_to_words, currency_decimal_places, round_to_decimal_places, lb_exchange_rate, \
    tax_currency
from shaibos.util.iterable import Iterable


class Bank(Iterable):
    def __init__(self, account, name, swift=None):
        self.account = account
        self.name = name
        self.swift = swift

    @classmethod
    def from_dictionary(cls, dictionary):
        if dictionary is None:
            return None
        else:
            return cls(
                account=dictionary['account'],
                name=dictionary['name'],
                swift=dictionary.get('swift', None),
            )


class CorrespondentBank(Bank):
    def __init__(self, account, name, swift):
        """SWIFT is required in the correspondent bank."""
        super(CorrespondentBank, self).__init__(account=account, name=name, swift=swift)


class Item(Iterable):
    def __init__(self, sku, description, measure, quantity, price, number=None):
        self.sku = sku
        self.description = description
        self.measure = measure
        self.quantity = quantity
        self.price = price
        self.number = number

        # Set by parent Invoice object to round the subtotals correctly
        self.currency = None

    @classmethod
    def from_dictionary(cls, dictionary):
        if dictionary is None:
            return None
        return cls(
            sku=dictionary['sku'],
            description=dictionary['description'],
            measure=dictionary['measure'],
            quantity=dictionary['quantity'],
            price=dictionary['price'],
            number=dictionary.get('number', None),
        )

    @property
    def subtotal(self):
        if self.currency is None:
            raise RuntimeError("'currency' wasn't set by the parent")

        quantity = Decimal(self.quantity)
        dec_places = currency_decimal_places(self.currency)
        price = round_to_decimal_places(Decimal(self.price), dec_places)
        subtotal = round_to_decimal_places(quantity * price, dec_places)
        return subtotal


class Seller(Iterable):
    def __init__(self, name, personal_number, address, email, bank_credentials, vsd_tax_rate, iea_certificate_number,
                 iea_certificate_issue_date, phone=None, fax=None):
        self.name = name
        self.personal_number = personal_number
        self.address = address
        self.email = email
        self.bank_credentials = bank_credentials
        self.vsd_tax_rate = vsd_tax_rate
        self.iea_certificate_number = iea_certificate_number
        self.iea_certificate_issue_date = iea_certificate_issue_date
        self.phone = phone
        self.fax = fax

    @classmethod
    def from_dictionary(cls, dictionary):
        return cls(
            name=dictionary['name'],
            personal_number=dictionary['personal_number'],
            address=dictionary['address'],
            email=dictionary['email'],
            bank_credentials=Bank.from_dictionary(dictionary['bank_credentials']),
            vsd_tax_rate=dictionary['vsd_tax_rate'],
            iea_certificate_number=dictionary['iea_certificate_number'],
            iea_certificate_issue_date=dictionary.get('iea_certificate_issue_date', None),
            phone=dictionary.get('phone', None),
            fax=dictionary.get('fax', None),
        )


class Buyer(Iterable):
    default_locale = 'lt_LT'

    def __init__(self, name, address, languages, personal_number=None, company_code=None, vat_payer_code=None,
                 phone=None, fax=None, currency=None, correspondent_bank=None):
        self.name = name
        self.address = address
        self.languages = languages
        self.personal_number = personal_number
        self.company_code = company_code
        self.vat_payer_code = vat_payer_code
        self.phone = phone
        self.fax = fax
        self.currency = currency
        self.correspondent_bank = correspondent_bank

    def __unicode__(self):
        if isinstance(self.name, dict):
            return self.name[self.default_locale]
        else:
            return self.name

    @classmethod
    def from_dictionary(cls, dictionary):
        return cls(
            name=dictionary['name'],
            address=dictionary['address'],
            languages=dictionary['languages'],
            personal_number=dictionary.get('personal_number', None),
            company_code=dictionary.get('company_code', None),
            vat_payer_code=dictionary.get('vat_payer_code', None),
            phone=dictionary.get('phone', None),
            fax=dictionary.get('fax', None),
            currency=dictionary.get('currency', None),
            correspondent_bank=CorrespondentBank.from_dictionary(dictionary.get('correspondent_bank', None)),
        )


class Payment(Iterable):
    def __init__(self, paid, date=None, amount=None, currency=None):

        if currency is not None:
            if amount is None:
                raise Exception('Please define amount paid for invoice when custom currency is set')
            if date is None:
                raise Exception('Please define date when the invoice was paid when custom currency is set')

        self.paid = paid
        self.date = date
        self.amount = amount
        self.currency = currency

    @classmethod
    def from_dictionary(cls, dictionary):
        if dictionary is None:
            return None
        else:
            return cls(
                paid=dictionary['paid'],
                date=dictionary.get('date', None),
                amount=dictionary.get('amount', None),
                currency=dictionary.get('currency', None),
            )


class Activity(Iterable):
    def __init__(self, title, evrk_code, gpm_tax_rate, invoice_number_prefix, invoice_number_length):
        self.title = title
        self.evrk_code = evrk_code
        self.gpm_tax_rate = gpm_tax_rate
        self.invoice_number_prefix = invoice_number_prefix
        self.invoice_number_length = invoice_number_length

    @classmethod
    def from_dictionary(cls, dictionary):
        return cls(
            title=dictionary['title'],
            evrk_code=dictionary['evrk_code'],
            gpm_tax_rate=dictionary['gpm_tax_rate'],
            invoice_number_prefix=dictionary['invoice_number_prefix'],
            invoice_number_length=dictionary['invoice_number_length'],
        )


class Invoice(Iterable):
    _currency = None

    def __init__(self, seller, buyer, activity, items, date, payment=None, currency=None, number=None):
        self.seller = seller
        self.buyer = buyer
        self.activity = activity
        self.items = items
        self.date = date
        self.payment = payment
        self.currency = currency
        self.number = number

        next_item_number = 1
        for item in self.items:

            # Assign numbers to items which don't have them
            if item.number is None:
                item.number = next_item_number
            else:
                next_item_number = item.number
            next_item_number += 1

    @classmethod
    def from_dictionary(cls, dictionary):
        return cls(
            seller=Seller.from_dictionary(dictionary['seller']),
            buyer=Buyer.from_dictionary(dictionary['buyer']),
            activity=Activity.from_dictionary(dictionary['activity']),
            items=list(map(Item.from_dictionary, dictionary['items'])),
            date=dictionary['date'],
            payment=Payment.from_dictionary(dictionary.get('payment', None)),
            number=dictionary.get('number', None),
            currency=dictionary.get('currency', None),
        )

    @property
    def currency(self):
        if self._currency is None:
            return self.buyer.currency
        else:
            return self._currency

    @currency.setter
    def currency(self, currency):
        self._currency = currency

        # Payment's default currency
        if self.payment is not None and self.payment.currency is None:
            self.payment.currency = self.currency

        for item in self.items:
            # Items will use this to round subtotals correctly
            # (uses getter above which might return buyer's currency)
            item.currency = self.currency

    @property
    def padded_number(self):
        return str(self.number).zfill(self.activity.invoice_number_length)

    @property
    def total(self):
        total = Decimal(0)
        for item in self.items:
            total += item.subtotal
        return total

    @property
    def total_in_words(self):
        return amount_to_words(self.total, self.currency)

    def filename_prefix(self):
        return 'invoice_%s%s' % (
            self.activity.invoice_number_prefix.lower(),
            self.padded_number
        )

    def __unicode__(self):
        return self.filename_prefix()

    def has_been_paid(self):
        return self.payment is not None and self.payment.paid

    def payment_date(self):
        if not self.has_been_paid():
            return None
        else:
            if self.payment.date:
                return self.payment.date
            else:
                # Assume the invoice date
                return self.date

    def paid_amount(self):
        """Always returns amount in tax currency for the year."""

        amount = None

        if not self.has_been_paid():
            amount = None
        if not self.payment.amount:
            amount = self.total
        if not bool(self.payment.currency):
            raise TypeError("When payment amount is set, currency must be set too.")
        if self.payment.amount:

            target_currency = tax_currency(self.payment.date.year)

            if self.payment.currency == target_currency:
                # Nothing to convert
                amount = Decimal(self.payment.amount)
            else:
                if not self.payment.date:
                    raise TypeError("When payment has been made in a custom currency, I need to know the payment date")

                exchange_rate = lb_exchange_rate(
                    from_currency_code=self.payment.currency,
                    to_currency_code=target_currency,
                    date=self.payment.date
                )
                amount = Decimal(self.payment.amount) * exchange_rate

        if amount is not None:
            amount = round_to_decimal_places(Decimal(amount), currency_decimal_places(self.currency))

        return amount


def from_list_enumerate(invoices_list):
    """
    Returns dictionary with invoice number prefixes as keys and lists of invoices belonging to that prefix as values.
    """

    invoices = defaultdict(list)
    next_invoice_numbers = {}

    # Assign numbers to invoices which don't have them, each activity being numbered independently
    for invoice_dict in invoices_list:
        invoice = Invoice.from_dictionary(invoice_dict)

        invoice_number_prefix = invoice.activity.invoice_number_prefix.upper()

        if invoice_number_prefix not in next_invoice_numbers:
            next_invoice_numbers[invoice_number_prefix] = 1

        if invoice.number is None:
            invoice.number = next_invoice_numbers[invoice_number_prefix]
        else:
            next_invoice_numbers[invoice_number_prefix] = invoice.number

        next_invoice_numbers[invoice_number_prefix] += 1

        invoices[invoice_number_prefix].append(invoice)

    return invoices
