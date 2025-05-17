from django.shortcuts import render

# Create your views here.
import pandas as pd
from io import BytesIO
import openpyxl
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from openpyxl.styles import PatternFill, Alignment


@csrf_exempt
def attendance_form(request):
    num_days = 7  # or any other default number

    if request.method == "POST":
        all_people = set()
        attendance_lists = []

        for i in range(1, num_days + 1):
            names = request.POST.get(f"day{i}", "")
            people = set(n.strip() for n in names.strip().splitlines() if n.strip())
            attendance_lists.append((f"Day {i}", people))
            all_people.update(people)

        all_people = sorted(all_people)
        data = {"Name": all_people}
        for label, people in attendance_lists:
            data[label] = ["+" if name in people else "-" for name in all_people]

        df = pd.DataFrame(data)
        output = BytesIO()
        df.to_excel(output, index=False)
        output.seek(0)

        # Get the workbook from the BytesIO object
        wb = openpyxl.load_workbook(output)
        ws = wb.active

        ws.column_dimensions['A'].width = 35  # default is around 13, so 20 is ~50% more

        # Define styles
        green_fill = PatternFill(start_color='90EE90', end_color='90EE90', fill_type='solid')
        red_fill = PatternFill(start_color='FFB6C1', end_color='FFB6C1', fill_type='solid')
        center_alignment = Alignment(horizontal='center')

        # Apply formatting to cells with + and -
        for row in ws.iter_rows(min_row=2):  # Start from row 2 to skip header
            for cell in row[1:]:  # Skip the name column
                if cell.value == '+':
                    cell.fill = green_fill
                    cell.alignment = center_alignment
                elif cell.value == '-':
                    cell.fill = red_fill
                    cell.alignment = center_alignment

        output = BytesIO()
        wb.save(output)
        output.seek(0)

        response = HttpResponse(
            output.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = "attachment; filename=attendance.xlsx"
        return response

    return render(request, "prod_handout/attendance_form.html", {"range": range(1, num_days + 1)})
