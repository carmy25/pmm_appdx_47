from openpyxl.styles import Font
from fals.models import FALType
from xlsx_export.utils import cell_center_border

import logging
logger = logging.getLogger(__name__)

PRICE_FAL_TYPE_BY_INDEX = {}


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
    ws.column_dimensions["E"].width = 30
    ws.column_dimensions["F"].width = 30
    ws.column_dimensions["G"].width = 30
    ws.row_dimensions[1].height = 30
    ws.merged_cells.ranges.add('A1:D1')
    year, month = date
    c = cell_center_border(ws, 'A1', f'Списано по донесеннях за {month}-{year}')
    c.font = Font(bold=True, size=20)

    c = cell_center_border(ws, 'A2', 'Тип ПММ')
    c.font = Font(bold=True)

    c = cell_center_border(ws, 'B2', 'Кількість(кг)')
    c.font = Font(bold=True)

    c = cell_center_border(ws, 'C2', 'Недостача(кг)')
    c.font = Font(bold=True)

    c = cell_center_border(ws, 'D2', 'Всього(кг)')
    c.font = Font(bold=True)

    c = cell_center_border(ws, 'E2', 'Сума (грн)')
    c.font = Font(bold=True)

    c = cell_center_border(ws, 'F2', 'Ціна різниці за кг(грн)')
    c.font = Font(bold=True)

    c = cell_center_border(ws, 'G2', 'Сума з різницею(грн)')
    c.font = Font(bold=True)


def prepear_fal_type_index():
    global PRICE_FAL_TYPE_BY_INDEX
    if len(PRICE_FAL_TYPE_BY_INDEX.keys()) == 0:
        PRICE_FAL_TYPE_BY_INDEX = {f.name: i for i, f in enumerate(FALType.objects.all(), 3)}


def report_price_format_fals(ws, amounts, prices, totals):
    prepear_fal_type_index()
    for name, i in PRICE_FAL_TYPE_BY_INDEX.items():
        cell_center_border(ws, f'A{i}', name)
        cell_center_border(ws, f'B{i}', amounts[name])
        cell_center_border(ws, f'C{i}', f'=D{i}-B{i}')
        cell_center_border(ws, f'D{i}', totals[name])
        cell_center_border(ws, f'E{i}', prices[name])
        cell_center_border(ws, f'F{i}', 0)
        cell_center_border(ws, f'G{i}', f'=E{i}+C{i}*F{i}')
