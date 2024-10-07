from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.utils import get_column_letter
from itertools import chain
from fals.models import FAL
from receipts.models.invoice import Invoice
from receipts.models.reporting import FALReportEntry
from receipts.models import ReceiptRequest, ReceiptRequestCoupon, Certificate

from .utils import cell_center_border, THIN_BORDER
from .reporting_summary_document_handler import ReportingSummaryReportDocumentHandler
from .base_document_handler import BaseFALDocumentHandler
from .invoice_document_handler import InvoiceDocumentHandler


DEP_BY_INDEX = {}


class FALDocumentHandler(BaseFALDocumentHandler):

    def get_dep(self):
        if type(self.fal.document_object) in [ReceiptRequestCoupon, Certificate]:
            return self.fal.document_object.destination
        else:
            return self.fal.document_object.sender

    def update_total_base_dep(self):
        if type(self.fal.document_object) in [ReceiptRequestCoupon, Certificate]:
            self.state['total_by_dep'][self.fal.document_object.destination] = self.fal.amount + \
                self.state['total_by_dep'].get(
                    self.fal.document_object.destination, 0)
        else:
            self.state['total_by_dep'][self.fal.document_object.sender] = self.state['total_by_dep'].get(
                self.fal.document_object.sender, 0) - self.fal.amount

    def get_document_name(self):
        return self.fal.document_object._meta.verbose_name

    def get_document_number(self):
        doc = self.fal.document_object
        if type(doc) in [ReceiptRequest, ReceiptRequestCoupon]:
            return f'{
                doc.number}/{doc.book_number}{doc.book_series.upper()}'
        return doc.number

    def get_fal_income(self):
        doc = self.fal.document_object
        if type(doc) in [Certificate, ReceiptRequestCoupon]:
            return self.fal.amount
        return 0

    def get_fal_outcome(self):
        doc = self.fal.document_object
        if type(doc) in [Certificate, ReceiptRequestCoupon]:
            return 0
        return self.fal.amount

    def get_document_sender(self):
        doc = self.fal.document_object
        if type(doc) in [Certificate, ReceiptRequestCoupon]:
            return doc.sender.upper()
        return doc.destination.upper()

    def get_document_operation_date(self):
        return self.fal.document_object.operation_date


def export_fal_type(fal_type, ws, departments):
    format_header(ws, fal_type, departments)
    format_rows(ws, fal_type)


def get_fal_date(obj):
    if type(obj) is FALReportEntry:
        return obj.report.summary_report.end_date
    return obj.document_object.operation_date


def get_sorted_fals(fal_type):
    fals = FAL.objects \
        .filter(fal_type=fal_type) \
        .exclude(object_id__isnull=True) \
        .prefetch_related('document_object')
    fal_report_entries = FALReportEntry.objects \
        .filter(fal_type=fal_type) \
        .exclude(report__isnull=True) \
        .exclude(report__summary_report__isnull=True)

    sorted_fals = sorted(
        chain(fals, fal_report_entries),
        key=get_fal_date)
    return sorted_fals


def format_rows(ws, fal_type):
    ws_state = {'total': 0,
                'total_by_dep': {},
                'DEP_BY_INDEX': DEP_BY_INDEX}
    fals = get_sorted_fals(fal_type)
    j = 3
    for i, fal in enumerate(fals):
        ws_state['idx'] = i + j
        if type(fal) is FALReportEntry:
            if not ReportingSummaryReportDocumentHandler(fal, ws, ws_state).process():
                j -= 1
        elif type(fal.document_object) != Invoice:
            FALDocumentHandler(fal, ws, ws_state).process()
        elif type(fal.document_object) == Invoice:
            InvoiceDocumentHandler(fal, ws, ws_state).process()


def format_header(ws, fal_type, departments):
    ws.column_dimensions['A'].width = 30
    ws.column_dimensions['b'].width = 30
    ws.column_dimensions['c'].width = 30
    ws.column_dimensions['d'].width = 30
    ws.column_dimensions['e'].width = 20
    ws.column_dimensions['f'].width = 20
    ws.column_dimensions['g'].width = 20
    ws['A1'] = fal_type.name
    ws['a1'].border = THIN_BORDER
    ws[f'a1'].alignment = Alignment(horizontal='center')
    ws['a1'].font = Font(bold=True)
    ws['a1'].fill = PatternFill(
        start_color="c4d79b", end_color="c4d79b", fill_type="solid")
    ws.merged_cells.ranges.add('A1:D1')
    ws.merged_cells.ranges.add('E1:G1')
    total_cell = cell_center_border(ws, 'E1', 'Загалом')
    total_cell.font = Font(bold=True)
    total_cell.fill = PatternFill(
        start_color="9bb8d9", end_color="9bb8d9", fill_type="solid")

    cell_center_border(
        ws, 'a2', 'Найменування документу').font = Font(bold=True)
    cell_center_border(ws, 'b2', 'Номер документу').font = Font(bold=True)
    cell_center_border(ws, 'c2', 'Дата операції').font = Font(bold=True)
    cell_center_border(
        ws, 'd2', 'Постачальник (одержувач)').font = Font(bold=True)
    cell_center_border(ws, 'e2', 'Надійшло').font = Font(bold=True)
    cell_center_border(ws, 'f2', 'Вибуло').font = Font(bold=True)
    cell_center_border(ws, 'g2', 'Всього').font = Font(bold=True)

    format_departments(ws, departments)


def format_departments(ws, deps):
    col_idx = 8
    for dep in deps:
        DEP_BY_INDEX[dep.name] = col_idx
        start_cell_name = f'{get_column_letter(col_idx)}1'
        ws.merged_cells.ranges.add(f'{start_cell_name}:{
                                   get_column_letter(col_idx+2)}1')
        dep_name_cell = cell_center_border(ws, start_cell_name, dep.name)
        dep_name_cell.font = Font(bold=True)
        dep_name_cell.fill = PatternFill(
            start_color="fee8d9", end_color="fee8d9", fill_type="solid")

        cell_center_border(ws, f'{get_column_letter(
            col_idx)}2', 'Надійшло').font = Font(bold=True)
        cell_center_border(ws, f'{get_column_letter(
            col_idx+1)}2', 'Вибуло').font = Font(bold=True)
        cell_center_border(ws, f'{get_column_letter(
            col_idx+2)}2', 'Всього').font = Font(bold=True)
        col_idx += 3
