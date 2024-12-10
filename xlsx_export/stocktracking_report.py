def export_stocktaking_report(wb, deps):
    for dep in deps:
        ws = wb.create_sheet(dep.name)
        # get last dep reporting
        reporting = dep.reportings.all().order_by('end_date').last()
        if reporting is None:
            continue
        for i, fe in enumerate(reporting.fals.all().order_by('fal_type__name'), 36):
            remains_after_kgs = fe.get_remains_after_kgs()
            if remains_after_kgs > 0:
                ws[f'C{i}'] = fe.fal_type.name
                ws[f'F{i}'] = remains_after_kgs
                rrc = (fe.fal_type
                       .fal_rrc_entries.invoice_for_rrc
                       .order_by('invoice_for_rrc__rrc__operation_date')
                       .last())
                if rrc is None or rrc.invoice_for_rrc.rrc is None:
                    print(f'HHH {fe.fal_type.fal_rrc_entries}')
                    continue
                print(f'{fe.fal_type.name} {rrc.invoice_for_rrc.rrc.operation_date}')
