from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from bson import ObjectId
from datetime import datetime
from mongo import db
# Create your views here.
def post_event(request, id):
    events = list(db.events.find())
    for ev in events:
        ev['id'] = str(ev['_id'])
    
    event = db.events.find_one({"_id": ObjectId(id)})
    if event:
        user = db.users.find_one({"_id": event['createur']})
        nombre_reservation = len(event['reservations'])
    #     event['date_heure'] = datetime.strptime(event['date_heure'], "%Y-%m-%d %H:%M:%S")
    #     event['date_heure'] = event['date_heure'].strftime("%Y-%m-%dT%H:%M")
    #     event['reservations'] = list(db.reservations.find({"evenement": ObjectId(id)}))
    #     for reservation in event['reservations']:
    #         reservation['id'] = str(reservation['_id'])
    #         reservation['utilisateur'] = db.users.find_one({"_id": reservation["utilisateur"]})
    #         reservation['utilisateur']['id'] = str(reservation['utilisateur']['_id'])
        
        return render(request, 'event_detail.html', {'event': event, 'events': events, 'user': user, 'nombre_reservation': nombre_reservation})
    else:
        error = f"L'événement n'existe pas."
        return render(request, 'event_detail.html', {'error': error})