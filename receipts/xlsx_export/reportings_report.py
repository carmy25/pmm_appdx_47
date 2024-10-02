from openpyxl.utils import get_column_letter

from receipts.xlsx_export.utils import cell_center_border, month_iter
from receipts.xlsx_export.xlsx_export import format_departments_column


MONTH_BY_INDEX = {}
DEP_BY_INDEX = {}


def export_reportings_report(ws, reportings):
    departments = [r.department for r in reportings]
    ws.column_dimensions['A'].width = 40
    format_departments_column(ws, departments)
    idx = 2
    for dep in departments:
        DEP_BY_INDEX[dep.name] = idx
        cell_center_border(ws, f'A{idx}', dep.name)
        idx += 1
    oldest = reportings.first().end_date
    newest = reportings.last().end_date

    idx = 2
    for y, m in month_iter(oldest.month, oldest.year, newest.month, newest.year):
        col_name = get_column_letter(idx)
        MONTH_BY_INDEX[(y, m)] = col_name
        idx += 1
        cell_center_border(ws, f'{col_name}1', f'{m}/{y}')

    format_deps_reportings(ws, reportings)


def format_deps_reportings(ws, reportings):
    for report in reportings:
        end_date = report.end_date
        col_name = MONTH_BY_INDEX[(end_date.year, end_date.month)]
        row_idx = DEP_BY_INDEX[report.department.name]
        cell_center_border(ws, f'{col_name}{row_idx}', '+')
