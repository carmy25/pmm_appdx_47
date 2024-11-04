from openpyxl.styles import Font
from xlsx_export.utils import cell_center_border

import logging
logger = logging.getLogger(__name__)


class InvoiceForRRCMut:
    def __init__(self, invoice_for_rrc):
        self.doc = invoice_for_rrc
        self._fals = None

    @property
    def operation_date(self):
        return self.doc.operation_date

    @property
    def fals(self):
        if self._fals is None:
            self._fals = [InvoiceForRRCEntry(e) for e in self.doc.fals.all()]
            self._fals += [InvoiceForRRCEntry(e) for e in self.doc.fals.all()]
        return self._fals


class InvoiceForRRCEntry:
    def __init__(self, invoice_for_rrc_entry):
        self.doc = invoice_for_rrc_entry
        self._amount = self.doc.amount
        self._price = self.doc.price
        logger.info(f'Invoice Entry Created({
            self.doc.fal_type}): {
            self.doc.amount}:{
                self.doc.price} - {
                    self.price_per_kg()}. RRC: {
                        self.doc.invoice_for_rrc.base_document_number}')

    @property
    def fal_type(self):
        return self.doc.fal_type

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value

    def price_per_kg(self):
        return self.price / self.amount

    def write_off(self, amount):
        diff = self.amount - amount
        res = {'amount': 0, 'price': 0}
        if diff <= 0:
            res['amount'] = self.amount
            res['price'] = self.price
            self.amount = 0
            self.price = 0
            return res

        res['amount'] = amount
        res['price'] = amount * self.price_per_kg()
        self.price = diff * self.price_per_kg()
        self.amount = diff
        return res


def report_price_format_header(ws, date):
    ws.column_dimensions["A"].width = 40
    ws.column_dimensions["B"].width = 30
    ws.column_dimensions["C"].width = 30
    ws.column_dimensions["D"].width = 30
    ws.row_dimensions[1].height = 30
    ws.merged_cells.ranges.add('A1:D1')
    year, month = date
    c = cell_center_border(ws, 'A1', f'Списано по донесеннях за {month}-{year}')
    c.font = Font(bold=True, size=20)

    c = cell_center_border(ws, 'A2', 'Тип ПММ')
    c.font = Font(bold=True)

    c = cell_center_border(ws, 'B2', 'Кількість(кг)')
    c.font = Font(bold=True)

    c = cell_center_border(ws, 'C2', 'Всього(кг)')
    c.font = Font(bold=True)

    c = cell_center_border(ws, 'D2', 'Сума (грн)')
    c.font = Font(bold=True)


def report_price_format_fals(ws, amounts, prices, totals):
    for idx, (name, amount) in enumerate(amounts.items(), 3):
        cell_center_border(ws, f'A{idx}', name)
        cell_center_border(ws, f'B{idx}', amount)
        cell_center_border(ws, f'C{idx}', totals[name])
        cell_center_border(ws, f'D{idx}', prices[name])
