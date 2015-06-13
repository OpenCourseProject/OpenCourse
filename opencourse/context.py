from opencourse.forms import ReportForm

def report(request):
    return {'report_form': ReportForm()}
