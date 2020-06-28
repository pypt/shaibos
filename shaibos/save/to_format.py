# -*- coding: utf-8 -*-

from decimal import Decimal
import os
import tempfile
import subprocess

from jinja2 import Environment

from shaibos.util.currency import format_currency
from shaibos.util.currency import round_to_decimal_places
from shaibos.util.date import format_date


def render_html(data, template_path):
    with open(template_path, 'r', encoding='utf-8') as template_f:
        template = template_f.read()

    env = Environment(trim_blocks=True, lstrip_blocks=True)

    env.globals.update(format_currency=format_currency)
    env.globals.update(format_date=format_date)
    env.globals.update(round_to_decimal_places=round_to_decimal_places)
    env.globals.update(Decimal=Decimal)

    return env.from_string(template).render(data)


def save_html(data, template_path, output_path):
    html = render_html(data, template_path=template_path)
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(html)


def save_pdf(data, template_path, output_path):
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.html', delete=False) as f:
        try:
            html = render_html(data, template_path)
            f.write(html.encode('utf-8'))
            f.close()
            subprocess.check_call(['chromium-browser', '--headless', '--disable-gpu',
                                   '--print-to-pdf=' + output_path, f.name])
        finally:
            os.remove(f.name)


def save_any(data, template_path, output_path, format):
    if format == 'pdf':
        save_pdf(data, template_path, output_path)
    elif format == 'html':
        save_html(data, template_path, output_path)
    else:
        raise Exception("Unsupported format {}".format(format))


def format_to_extension(format):
    # at the time format matches the file extension
    return format
