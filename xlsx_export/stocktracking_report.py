from copy import copy
from datetime import datetime
from django.conf import settings
import openpyxl as xl

from xlsx_export.utils import cell_center_border
from .number_to_text import num2text


def format_dep_fals(ws, dep, data):
    i = 0
    kgs_total = 0
    for i, (fal_type, value) in enumerate(data['fals'].items(), 1):
        idx = value['idx']
        amount = value.setdefault('invoices_kgs', 0) + value.setdefault('handout_kgs',
                                                                        0) + value.setdefault('reporting_remains', 0)
        cell_center_border(ws, f'A{value["idx"]}', i)
        cell_center_border(ws, f'B{value["idx"]}', '')
        cell_center_border(ws, f'C{value["idx"]}', fal_type.name)
        cell_center_border(ws, f'D{value["idx"]}', '')
        cell_center_border(ws, f'e{value["idx"]}', 'кг')
        cell_center_border(ws, f'F{value["idx"]}', amount)
        kgs_total += amount
        cell_center_border(ws, f'G{value["idx"]}', value['price'])
        cell_center_border(ws, f'H{value["idx"]}', f'=G{idx}*F{idx}')

        cell_center_border(ws, f'I{value["idx"]}', amount)
        cell_center_border(ws, f'J{value["idx"]}', value['price'])
        cell_center_border(ws, f'K{value["idx"]}', f'=G{idx}*F{idx}')
    if i == 0:
        return kgs_total
    cell_center_border(ws, f'F{36+i}', f'=sum(F36:F{35+i})')
    cell_center_border(ws, f'H{36+i}', f'=sum(H36:H{35+i})')
    cell_center_border(ws, f'I{36+i}', f'=sum(I36:I{35+i})')
    cell_center_border(ws, f'K{36+i}', f'=sum(K36:K{35+i})')
    return kgs_total


def format_dep_footer(ws, dep, data, kgs_total):
    ws_tmpl = settings.WB_TMPL.active
    entries_num = len(data['fals'].keys())
    idx = entries_num + 36 + 3
    for i in range(24):
        for j in range(1, 14):
            c = ws.cell(row=i+idx, column=j)
            tc = ws_tmpl.cell(row=i+39, column=j)
            c.value = tc.value
            c.font = copy(tc.font)
            c.fill = copy(tc.fill)
            c.border = copy(tc.border)
            c.alignment = copy(tc.alignment)
    ws[f'c{idx}'].value = f'а) кількість порядкових номерів - {num2text(entries_num)}'
    ws[f'c{
        idx+2}'].value = f'б) загальна кількість кілограм,  фактично - {num2text(round(kgs_total))}'
    ws[f'c{
        idx+4}'].value = f'в) загальна кількість кілограм,  за даними бухгалтерського обліку - {num2text(round(kgs_total))}'
    # ws.row_dimensions[idx].height = 30
    ws.merged_cells.ranges.add(f'a{idx+15}:m{idx+16}')


def export_stocktaking_report(wb, deps, form_data):
    data = {}
    for dep in deps:
        data[dep.name] = {}
        update_reporting_dep_data(dep, data[dep.name])
        update_invoice_dep_data(dep, data[dep.name])
        update_handout_dep_data(dep, data[dep.name])
        update_price_dep_data(dep, data[dep.name])

        ws = wb.create_sheet(dep.name)
        format_dep_header(ws, dep, data[dep.name], form_data)
        kgs_total = format_dep_fals(ws, dep, data[dep.name])
        format_dep_footer(ws, dep, data[dep.name], kgs_total)

    from pprint import pprint
    pprint(data)


def update_price_dep_data(dep, data):
    for fal_type, d in data['fals'].items():
        rrc = fal_type.fal_rrc_entries.filter(
            invoice_for_rrc__rrc__operation_date__lte=data.setdefault(
                'end_date',  datetime.now())).last()
        if rrc is None:
            print(f'FAL not found: {fal_type.name}')
            rrc = fal_type.fal_rrc_entries.filter().last()

        data['fals'][fal_type]['price'] = rrc.price / rrc.amount


def update_invoice_dep_data(dep, data):
    report_end_date = data.get('end_date')
    invoices = dep.invoices_receiver.all()
    if report_end_date:
        invoices = invoices.filter(
            operation_date__gt=report_end_date).order_by('operation_date')
    idx = 36
    for invoice in invoices:
        for fal in invoice.fals.all():
            fal_data = data['fals'].setdefault(fal.fal_type, {})
            fal_data.setdefault('invoices_kgs', 0)
            if not fal_data.get('idx'):
                fal_data['idx'] = idx
                idx += 1
            fal_data['invoices_kgs'] += fal.amount
    if invoices.count() > 0:
        data['end_date'] = invoice.operation_date


def update_handout_dep_data(dep, data):
    handouts = dep.received_handouts.filter(
        operation_date__lt=(data.get('end_date') or datetime.now()))
    for handout in handouts:
        for i, fal in enumerate(handout.fals.all(), 36):
            fal_data = data['fals'].setdefault(fal.fal_type, {})
            fal_data.setdefault('handout_kgs', 0)
            fal_data.setdefault('idx', i)
            fal_data['handout_kgs'] += fal.amount


def format_dep_header(ws, dep, data, form_data):
    ws_tmpl = settings.WB_TMPL.active
    ws.merged_cells.ranges = ws_tmpl.merged_cells.ranges
    for i in range(1, 36):
        for j in range(1, 14):
            c = ws.cell(row=i, column=j)
            tc = ws_tmpl.cell(row=i, column=j)
            c.value = tc.value
            c.font = copy(tc.font)
            c.fill = copy(tc.fill)
            c.border = copy(tc.border)
            c.alignment = copy(tc.alignment)
    ws['A3'].value = form_data['department_name']
    ws['A4'].value = f'Ідентифікаційний кол за ЄДРПО: {form_data['edrpo_code']}'
    ws['A10'].value = form_data['document_date_number']
    ws['A18'].value = f"станом на {form_data['date_remains']}"
    ws['C27'].value = f'розпочата {form_data["start_date"]}'
    chief_verbose = dep.chief_position_verbose()
    ws['D24'].value = f'{chief_verbose} {dep.name}'
    ws['K24'].value = f'{dep.chief_name}'
    ws['C28'].value = f'закінчена {form_data["end_date"]}'
    ws.column_dimensions['c'].width = 50
    ws['c16'].value = dep.name


def update_reporting_dep_data(dep, data):
    data['fals'] = {}
    reporting = dep.reportings.all().order_by('end_date').last()
    if reporting is None:
        return
    j = 0
    data['start_date'] = reporting.start_date
    data['end_date'] = reporting.end_date
    for i, fe in enumerate(reporting.fals.all().order_by('fal_type__name'), 36):
        idx = i - j
        remains_after_kgs = fe.get_remains_after_kgs()
        if remains_after_kgs == 0:
            j += 1
            continue
        data['fals'][fe.fal_type] = {
            'idx': idx,
            'reporting_remains': remains_after_kgs
        }
        '''
            rrc = (fe.fal_type
                   .fal_rrc_entries
                   .order_by('invoice_for_rrc__rrc__operation_date')
                   .last())
            if rrc is None or rrc.invoice_for_rrc.rrc is None:
                print(f'HHH {fe.fal_type.name}')
                continue
            print(f'{fe.fal_type.name} {rrc.invoice_for_rrc.rrc.operation_date}')
        '''
