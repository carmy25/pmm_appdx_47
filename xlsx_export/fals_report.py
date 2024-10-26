from receipts.models.certificate import Certificate
from receipts.models.receipt import ReceiptRequest, ReceiptRequestCoupon
from receipts.models.reporting import FALReportEntry
from xlsx_export.utils import cell_center_border, header_cell_center_border


def format_header(ws):
    ws.column_dimensions["A"].width = 40
    ws.column_dimensions["B"].width = 25
    ws.column_dimensions["C"].width = 25
    ws.column_dimensions["D"].width = 25
    ws.column_dimensions["E"].width = 25
    ws.column_dimensions["F"].width = 25
    ws.column_dimensions["G"].width = 25
    ws.freeze_panes = ws["B2"]
    header_cell_center_border(ws, "A1", 'Види ПММ')
    header_cell_center_border(ws, "B1", 'Атестат')
    header_cell_center_border(ws, "C1", 'Талони Чек Вимог')
    header_cell_center_border(ws, "D1", 'Чекові Вимоги')
    header_cell_center_border(ws, "E1", 'Донесення')
    header_cell_center_border(ws, "F1", 'Рахується')
    header_cell_center_border(ws, "G1", 'Проведено ФЕС')
    header_cell_center_border(ws, "H1", '% ФЕС')


def export_fals_report(ws, fal_types):
    format_header(ws)
    total_by_category = {}
    for i, fal_type in enumerate(fal_types, 2):
        cell_center_border(ws, f"a{i}", fal_type.name)
        for fal in fal_type.fals.all():
            if isinstance(fal.document_object, Certificate):
                cn = f'b{i}'
                value = ws[cn].value + fal.amount if ws[cn].value else fal.amount
                cell_center_border(ws, cn, value)
            elif isinstance(fal.document_object, ReceiptRequestCoupon):
                cn = f'c{i}'
                value = ws[cn].value + fal.amount if ws[cn].value else fal.amount
                cell_center_border(ws, cn, value)
            elif isinstance(fal.document_object, ReceiptRequest):
                cn = f'd{i}'
                value = ws[cn].value + fal.amount if ws[cn].value else fal.amount
                cell_center_border(ws, cn, value)
        for fre in fal_type.fal_report_entries.all():
            cn = f'e{i}'
            value = ws[cn].value + fre.outcome if ws[cn].value else fre.outcome
            cell_center_border(ws, cn, value)
