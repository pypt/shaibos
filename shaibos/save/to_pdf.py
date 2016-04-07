# -*- coding: utf-8 -*-

import os
import tempfile

import pdfkit

from shaibos.save.to_html import render_html

pdfkit_options = {
    'page-size': 'A4',
    'margin-top': '0.25in',
    'margin-right': '0.25in',
    'margin-bottom': '0.25in',
    'margin-left': '0.25in',
    'encoding': 'UTF-8',
    'no-outline': None,
    'quiet': '',
}


def save_pdf(invoice, template_path, output_path):
    html = render_html(invoice=invoice, template_path=template_path)
    pdfkit.from_string(html, output_path, options=pdfkit_options)


def save_pdf_tempdir(invoice, template_path):
    temp_dir = tempfile.mkdtemp()

    invoice_filename_prefix = 'invoice_%s%s' % (
        invoice.seller.invoice_number_prefix.lower(),
        invoice.padded_number
    )
    temp_pdf_file_path = os.path.join(temp_dir, invoice_filename_prefix + '.pdf')
    save_pdf(invoice=invoice, template_path=template_path, output_path=temp_pdf_file_path)

    return temp_pdf_file_path
