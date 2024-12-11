from datetime import datetime

from fals.models import Category
from xlsx_export.utils import cell_center_border


def format_dep_fals(ws, dep, data):
    for fal_type, value in data['fals'].items():
        idx = value['idx']
        amount = value.setdefault('invoices_kgs', 0) + value.setdefault('handout_kgs',
                                                                        0) + value.setdefault('reporting_remains', 0)
        cell_center_border(ws, f'C{value["idx"]}', fal_type.name)
        cell_center_border(ws, f'F{value["idx"]}', amount)
        cell_center_border(ws, f'G{value["idx"]}', value['price'])
        cell_center_border(ws, f'H{value["idx"]}', f'=G{idx}*F{idx}')


def export_stocktaking_report(wb, deps):
    data = {}
    for dep in deps:
        data[dep.name] = {}
        update_reporting_dep_data(dep, data[dep.name])
        update_invoice_dep_data(dep, data[dep.name])
        update_handout_dep_data(dep, data[dep.name])
        update_price_dep_data(dep, data[dep.name])

        ws = wb.create_sheet(dep.name)
        format_dep_fals(ws, dep, data[dep.name])

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
