from openpyxl.styles import Border, \
    Side, PatternFill, Font, GradientFill, Alignment
import logging
from fals.models import FAL
from .models import ReceiptRequestCoupon


def export_fal_type(fal_type, ws):
    format_header(ws, fal_type)
    format_rows(ws, fal_type)


def format_rows(ws, fal_type):
    fals = FAL.objects.filter(fal_type=fal_type).order_by(
        'document__operation_date')
    j = 0
    total = 0
    for i, fal in enumerate(fals):
        if not fal.document_object:
            logging.info(f'fal do not assigned to any document: {fal.pk}')
            j += 1
            continue
        document = fal.document_object
        idx = i + 3 - j
        ws[f'A{idx}'] = document._meta.verbose_name
        ws[f'A{idx}'].alignment = Alignment(horizontal='center')
        ws[f'B{idx}'] = f'{
            document.number}/{document.book_number}{document.book_series}'
        ws[f'B{idx}'].alignment = Alignment(horizontal='center')
        ws[f'C{idx}'] = document.operation_date
        ws[f'C{idx}'].alignment = Alignment(horizontal='center')
        ws[f'D{idx}'] = document.sender if type(
            document) == ReceiptRequestCoupon else document.destination
        ws[f'D{idx}'].alignment = Alignment(horizontal='center')

        amount_cell_range = f'E{idx}' if type(
            document) == ReceiptRequestCoupon else f'f{idx}'
        ws[amount_cell_range] = fal.amount
        ws[amount_cell_range].alignment = Alignment(horizontal='center')

        if type(document) == ReceiptRequestCoupon:
            total += fal.amount
        else:
            total -= fal.amount

        ws[f'G{idx}'] = total
        ws[f'G{idx}'].alignment = Alignment(horizontal='center')


def format_header(ws, fal_type):
    ws.column_dimensions['A'].width = 30
    ws.column_dimensions['b'].width = 30
    ws.column_dimensions['c'].width = 30
    ws.column_dimensions['d'].width = 30
    ws.column_dimensions['e'].width = 20
    ws.column_dimensions['f'].width = 20
    ws.column_dimensions['g'].width = 20

    ws['A1'] = fal_type.name
    ws.merged_cells.ranges.add('A1:C1')
    ws['a2'] = 'Найменування документу'
    ws['b2'] = 'Номер документу'
    ws['c2'] = 'Дата операції'
    ws['d2'] = 'Постачальник (одержувач)'
    ws['e2'] = 'Надійшло'
    ws['f2'] = 'Вибуло'
    ws['g2'] = 'Всього'
