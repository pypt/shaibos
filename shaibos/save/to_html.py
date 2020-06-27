# -*- coding: utf-8 -*-
import codecs
import os
import tempfile

from jinja2 import Environment

from shaibos.util.currency import format_currency
from shaibos.util.currency import round_to_decimal_places
from shaibos.util.date import format_date


def render_html(invoice, template_path):
    template = codecs.open(template_path, 'r', 'utf-8').read()

    env = Environment(trim_blocks=True, lstrip_blocks=True)

    env.globals.update(format_currency=format_currency)
    env.globals.update(format_date=format_date)
    env.globals.update(round_to_decimal_places=round_to_decimal_places)

    return env.from_string(template).render(invoice)


def save_html(invoice, template_path, output_path):
    html = render_html(invoice=invoice, template_path=template_path)
    with codecs.open(output_path, 'wb', 'utf-8') as output_file:
        output_file.write(html)


def save_html_tempdir(invoice, template_path):
    temp_dir = tempfile.mkdtemp()

    invoice_filename_prefix = 'invoice_%s%s' % (
        invoice.seller.invoice_number_prefix.lower(),
        invoice.padded_number
    )
    temp_html_file_path = os.path.join(temp_dir, invoice_filename_prefix + '.html')
    save_html(invoice=invoice, template_path=template_path, output_path=temp_html_file_path)

    return temp_html_file_path


def default_html_export_path():
    return "invoices/html/"
