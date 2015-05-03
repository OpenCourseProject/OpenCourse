from django.core.management.base import BaseCommand, CommandError
from course.models import Term
from schedule.models import ExamEntry
from datetime import datetime
import xlrd

class Command(BaseCommand):
    args = '<term_id file_name>'

    def handle(self, *args, **options):
        term = Term.objects.get(value=args[0])
        file = xlrd.open_workbook(args[1])
        for sheet_name in file.sheet_names():
            date = datetime.strptime(sheet_name, '%m-%d-%Y').date()
            sheet = file.sheet_by_name(sheet_name)
            # Row 0, Columns 0-4
            for i in range(0,4):
                time = sheet.cell(0, i).value
                exam_start = datetime.strptime(time.split("-")[0], '%H%M').time()
                exam_end = datetime.strptime(time.split("-")[1], '%H%M').time()
                # Rows 1-15
                first = True
                for cell in sheet.col(i):
                    if first:
                        first = False
                        continue
                    value = cell.value
                    if value == xlrd.empty_cell.value:
                        break
                    else:
                        print(value)
                        days = value.split(": ")[0]
                        time = value.split(": ")[1]
                        course_start = datetime.strptime(time.split("-")[0], '%H%M').time()
                        course_end = datetime.strptime(time.split("-")[1], '%H%M').time()
                        exam = ExamEntry(term=term, days=days, course_start_time=course_start, course_end_time=course_end, exam_date=date, exam_start_time=exam_start, exam_end_time=exam_end)
                        exam.save()
        self.stdout.write('Successfully imported exam times')
