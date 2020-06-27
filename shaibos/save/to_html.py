# -*- coding: utf-8 -*-

from jinja2 import Environment

from shaibos.util.currency import format_currency
from shaibos.util.currency import round_to_decimal_places
from shaibos.util.date import format_date


def render_html(invoice, template_path):
    with open(template_path, 'r', encoding='utf-8') as template_f:
        template = template_f.read()

    env = Environment(trim_blocks=True, lstrip_blocks=True)

    env.globals.update(format_currency=format_currency)
    env.globals.update(format_date=format_date)
    env.globals.update(round_to_decimal_places=round_to_decimal_places)

    return env.from_string(template).render(invoice)


def save_html(invoice, template_path, output_path):
    html = render_html(invoice=invoice, template_path=template_path)
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(html)


def default_html_export_path():
    return "invoices/html/"
