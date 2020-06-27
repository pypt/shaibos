# -*- coding: utf-8 -*-

import os
import tempfile
import subprocess

from shaibos.save.to_html import render_html


def save_pdf(invoice, template_path, output_path):
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.html', delete=False) as f:
        try:
            html = render_html(invoice=invoice, template_path=template_path)
            f.write(html.encode('utf-8'))
            f.close()
            subprocess.check_call(['chromium-browser', '--headless', '--disable-gpu',
                                   '--print-to-pdf=' + output_path, f.name])
        finally:
            os.remove(f.name)


def default_pdf_export_path():
    return "invoices/pdf/"
