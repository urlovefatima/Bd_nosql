from django.shortcuts import render
from mongo import db  

def get_events(request):
    if db is not None :
        events = list(db.events.find({}, {"_id": 0}))
        return render(request, 'events.html', {'events': events})
    else:
        return render(request, 'events.html', {'events': []})
