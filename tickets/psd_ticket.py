import sys
import qrcode

from collections import OrderedDict

from psd_tools import PSDImage

from reportlab.lib.units import mm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas

import io

from reportlab.lib.utils import ImageReader

class PSDTicketGenerator:
    def __init__(self, psd_file, pdf_width, pdf_height):
        self.psd = PSDImage.load(psd_file)

        self.width = pdf_width
        self.height = pdf_height

        if not self.check_scale():
            raise ValueError('PSD is not the right size.')

        self.name_dummy_layer = 'FIRSTNAME SURNAME'
        self.qr_dummy_layer = 'qr code example'
        self.ga_layer_name = 'GENERAL ADMISSION'
        self.qj_layer_name = 'QUEUE JUMP'
        self.ga_text_layer_name = 'general admission text'
        self.qj_text_layer_name = 'que jump ext'

        self.ignore_layers = ['Background', self.name_dummy_layer, self.qr_dummy_layer]

        self.buf = io.BytesIO()
        self.pdf = canvas.Canvas(
            self.buf,
            pagesize=(self.width*mm, self.height*mm),
        )

        self.layers = OrderedDict(
            (layer.name, (layer, ImageReader(layer.as_PIL()))) for layer in self.psd.layers
        )

    def check_scale(self):
        scale_factor_height = self.psd.header.height / self.height
        scale_factor_width = self.psd.header.width / self.width

        self.scale_factor = scale_factor_width

        sfd = abs(scale_factor_width - scale_factor_height)

        return sfd <= 0.1

    def qr_box(self):
        layer, _ = self.layers[self.qr_dummy_layer]

        x = self.scale(layer.bbox.x1)*mm
        y = (self.height - self.scale(layer.bbox.y2))*mm
        w = self.scale(layer.bbox.width)*mm
        h = self.scale(layer.bbox.height)*mm

        return x, y, w, h

    def text_position(self):
        layer, _ = self.layers[self.name_dummy_layer]
        x = self.scale((layer.bbox.x1 + layer.bbox.x2) / 2)*mm
        y = (self.height - self.scale(layer.bbox.y2))*mm

        return x, y

    def scale(self, x):
        return x / self.scale_factor

    def generate(self, queryset):
        qr_x, qr_y, qr_w, qr_h = self.qr_box()
        name_x, name_y = self.text_position()

        for ticket in queryset:
            for name, layer in reversed(self.layers.items()):
                if name in self.ignore_layers:
                    continue

                if ticket.premium and name in (self.ga_layer_name, self.ga_text_layer_name):
                    continue
                elif not ticket.premium and name in (self.qj_layer_name, self.qj_text_layer_name):
                    continue

                layer, image = layer

                x = self.scale(layer.bbox.x1)*mm
                y = (self.height - self.scale(layer.bbox.y2))*mm
                w = self.scale(layer.bbox.width)*mm
                h = self.scale(layer.bbox.height)*mm

                self.pdf.drawImage(image, x, y, width=w, height=h, mask='auto')

            qr = qrcode.make('http://www.kingsaffair.com/t/%s/' % ticket.code)
            self.pdf.drawImage(ImageReader(qr._img), qr_x, qr_y, width=qr_w, height=qr_h)

            self.pdf.setFillColorRGB(0.21,0.21,0.21)

            self.pdf.setFont("mono", 10)
            self.pdf.drawCentredString(qr_x + (qr_w / 2), (qr_h - qr_y), ticket.code)

            self.pdf.setFont("sans", 16)
            self.pdf.drawCentredString(name_x, name_y, str(ticket).upper())

            self.pdf.showPage()

        self.pdf.save()
        return self.buf
