# from django.shortcuts import render
# from django.conf import settings

# def get_events(request):
#     if settings.db:
#         events = list(settings.db.events.find({}, {"_id": 0}))
#         return render(request, 'events.html', {'events': events})
#     else:
#         return render(request, 'events.html', {'events': []})

# # Create your views here.


# app/views.py

from django.shortcuts import render
from mongo import db  # <-- import direct depuis mongo.py

def get_events(request):
    if db:
        events = list(db.events.find({}, {"_id": 0}))
        return render(request, 'events.html', {'events': events})
    else:
        return render(request, 'events.html', {'events': []})
