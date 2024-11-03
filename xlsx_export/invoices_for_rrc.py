from openpyxl.styles import Font
from xlsx_export.utils import cell_center_border


class InvoiceForRRCMut:
    def __init__(self, invoice_for_rrc):
        self.doc = invoice_for_rrc
        self._fals = None

    @property
    def operation_date(self):
        return self.doc.rrc.operation_date

    @property
    def fals(self):
        if self._fals is None:
            self._fals = [InvoiceForRRCEntry(e) for e in self.doc.fals.all()]
        return self._fals


class InvoiceForRRCEntry:
    def __init__(self, invoice_for_rrc_entry):
        print(invoice_for_rrc_entry)
        self.doc = invoice_for_rrc_entry
        self._amount = self.doc.amount
        self._price = self.doc.price

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
        self.amount = diff
        self.price = self.amount * self.price_per_kg()
        return res


def report_price_format_header(ws, date):
    ws.column_dimensions["A"].width = 40
    ws.column_dimensions["B"].width = 30
    ws.column_dimensions["C"].width = 30
    ws.row_dimensions[1].height = 30
    ws.merged_cells.ranges.add('A1:C1')
    year, month = date
    c = cell_center_border(ws, 'A1', f'Списано по донесеннях за {month}-{year}')
    c.font = Font(bold=True, size=20)

    c = cell_center_border(ws, 'A2', 'Тип ПММ')
    c.font = Font(bold=True)

    c = cell_center_border(ws, 'B2', 'Кількість(кг)')
    c.font = Font(bold=True)

    c = cell_center_border(ws, 'C2', 'Сума (грн)')
    c.font = Font(bold=True)


def report_price_format_fals(ws, amounts, prices):
    for idx, (name, amount) in enumerate(amounts.items(), 3):
        cell_center_border(ws, f'A{idx}', name)
        cell_center_border(ws, f'B{idx}', amount)
        cell_center_border(ws, f'C{idx}', prices[name])
