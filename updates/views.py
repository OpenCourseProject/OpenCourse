from django.shortcuts import render
from updates.models import Update
from course.models import QueryLog

def render_updates(request, updates):
    query_terms = [
        201610,
    ]
    queries = {}
    for term in query_terms:
        iden = request.user if request.user.is_authenticated() else None
        total = len(QueryLog.objects.filter(term__value=term))
        user = len(QueryLog.objects.filter(term__value=term, user=iden))
        data = [
            {
                'value': user,
                'label': 'You ({} searches)'.format(user)
            },
            {
                'value': total - user,
                'label': 'Everyone else ({} searches)'.format(total - user)
            },
        ]
        queries[term] = {
            'data': data,
            'num_total': total,
            'num_user': user,
            'percentage': (float(user)/float(total)) * 100,
        }
    context = {
        'updates': updates,
        'queries': queries,
    }
    return render(request, 'updates/index.html', context)

def index(request):
    updates = Update.objects.all().order_by('-time_created')
    return render_updates(request, updates)

def update(request, update):
    return render_updates(request, [Update.objects.get(id=update),])
