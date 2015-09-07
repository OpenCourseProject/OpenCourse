from django.shortcuts import render
from updates.models import Update
import HTMLParser

def render_updates(request, updates):
    for update in updates:
        update.body = HTMLParser.HTMLParser().unescape(update.body)
    context = {'updates' : updates}
    return render(request, 'updates/index.html', context)

def index(request):
    updates = Update.objects.all().order_by('-time_created')
    return render_updates(request, updates)

def update(request, update):
    return render_updates(request, [Update.objects.get(id=update),])
