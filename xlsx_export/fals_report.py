from receipts.models.certificate import Certificate
from receipts.models.inspection_certificate import InspectionCertificate
from receipts.models.receipt import ReceiptRequest, ReceiptRequestCoupon
from receipts.models.reporting import FALReportEntry
from receipts.models.writing_off_act import WritingOffAct
from xlsx_export.utils import cell_center_border, header_cell_center_border, get_or_zero

from fals.models import Category


def format_header(ws):
    ws.column_dimensions["A"].width = 40
    ws.column_dimensions["B"].width = 25
    ws.column_dimensions["C"].width = 25
    ws.column_dimensions["D"].width = 25
    ws.column_dimensions["E"].width = 25
    ws.column_dimensions["F"].width = 25
    ws.column_dimensions["G"].width = 25
    ws.column_dimensions["H"].width = 25
    ws.column_dimensions["I"].width = 25
    ws.column_dimensions["J"].width = 25
    ws.freeze_panes = ws["B2"]
    header_cell_center_border(ws, "A1", 'Види ПММ')
    header_cell_center_border(ws, "B1", 'Атестат')
    header_cell_center_border(ws, "C1", 'Талони Чек Вимог')
    header_cell_center_border(ws, "D1", 'Чекові Вимоги')
    header_cell_center_border(ws, "E1", 'Донесення')
    header_cell_center_border(ws, "f1", 'Акти списання')
    header_cell_center_border(ws, "g1", 'Інспект. Посвідчення')
    header_cell_center_border(ws, "h1", 'Рахується')
    header_cell_center_border(ws, "i1", 'Проведено ФЕС')
    header_cell_center_border(ws, "j1", '% ФЕС')

    ws.merged_cells.ranges.add("k1:L1")
    header_cell_center_border(ws, "k1", 'Підсумок')


def format_summary(ws, total_by_category):
    cell_center_border(ws, 'k2', 'ДП')
    cell_center_border(ws, 'k3', 'АБ')
    cell_center_border(ws, 'k4', 'МіМ')
    cell_center_border(ws, 'k5', 'Керосин')

    cell_center_border(ws, 'l2', total_by_category['DIESEL'])
    cell_center_border(ws, 'l3', total_by_category['PETROL'])
    cell_center_border(ws, 'l4', total_by_category['OIL'] + total_by_category['POISON'])
    cell_center_border(ws, 'l5', total_by_category['KEROSENE'])


def export_fals_report(ws, fal_types):
    format_header(ws)
    total_by_category = {c[0]: 0 for c in Category.choices}
    for i, fal_type in enumerate(fal_types, 2):
        cell_center_border(ws, f"a{i}", fal_type.name)
        for fal in fal_type.fals.all():
            if isinstance(fal.document_object, Certificate):
                cn = f'b{i}'
                b_value = ws[cn].value + fal.amount if ws[cn].value else fal.amount
                cell_center_border(ws, cn, b_value)
                total_by_category[fal_type.category] += fal.amount
            elif isinstance(fal.document_object, ReceiptRequestCoupon):
                cn = f'c{i}'
                c_value = ws[cn].value + fal.amount if ws[cn].value else fal.amount
                cell_center_border(ws, cn, c_value)
                total_by_category[fal_type.category] += fal.amount
            elif isinstance(fal.document_object, ReceiptRequest):
                cn = f'd{i}'
                d_value = ws[cn].value + fal.amount if ws[cn].value else fal.amount
                cell_center_border(ws, cn, d_value)
                total_by_category[fal_type.category] -= fal.amount
            elif isinstance(fal.document_object, WritingOffAct):
                cn = f'f{i}'
                d_value = ws[cn].value + fal.amount if ws[cn].value else fal.amount
                cell_center_border(ws, cn, d_value)
                total_by_category[fal_type.category] -= fal.amount
            elif isinstance(fal.document_object, InspectionCertificate):
                cn = f'G{i}'
                d_value = ws[cn].value + fal.amount if ws[cn].value else fal.amount
                cell_center_border(ws, cn, d_value)
                total_by_category[fal_type.category] -= fal.amount
        for fre in fal_type.fal_report_entries.all():
            cn = f'e{i}'
            outcome = fre.outcome * fre.get_density()
            value = ws[cn].value + outcome if ws[cn].value else outcome
            if fal_type.category in [Category.DIESEL,
                                     Category.PETROL,
                                     Category.KEROSENE]:
                value = round(value)
            elif fal_type.category == Category.OIL:
                value = round(value, 1)
            elif fal_type.category == Category.POISON:
                value = round(value, 2)
            cell_center_border(ws, cn, value)

            total_by_category[fal_type.category] -= round(outcome)

        cn = f'H{i}'
        cell_center_border(ws, cn, f'=b{i}+c{i}-d{i}-e{i}-f{i}-g{i}')

        cell_center_border(ws, f'J{i}', f'=i{i}/h{i} * 100')
    format_summary(ws, total_by_category)
