from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from bson import ObjectId
from datetime import datetime
from mongo import db
# Create your views here.
def post_event(request, id):
    email = request.session['email']
    events = list(db.events.find())
    for ev in events:
        ev['id'] = str(ev['_id'])
    
    event = db.events.find_one({"_id": ObjectId(id)})
    if event:
        event['id'] = str(event['_id'])
        user = db.users.find_one({"_id": event['createur']})
        if user == db.users.find_one({"email":email}):
            proprity = True
        else:
            proprity = False
        nombre_reservation = len(event['reservations'])
        
        return render(request, 'event_detail.html', {'event': event, 'events': events, 'user': user, 'nombre_reservation': nombre_reservation, 'proprity': proprity})
    else:
        error = f"L'événement n'existe pas."
        return render(request, 'event_detail.html', {'error': error})

def reserve_evenement(request, id):
    email = request.session['email']
    events = list(db.events.find())
    for ev in events:
        ev['id'] = str(ev['_id'])
    reserved = False
    event = db.events.find_one({"_id": ObjectId(id)})
    if event:
        # Add this line:
        event['id'] = str(event['_id'])
    user = db.users.find_one({"email":email})
    createur = db.users.find_one({"_id": event['createur']})
    if createur == db.users.find_one({"email":email}):
        proprity = True
    else:
        proprity = False
    nombre_reservation = len(event['reservations'])
    existed_reservation = False
    if event and user:
        for reservation in list(db.reservations.find()):
            if ((reservation['evenement'] == event['_id']) and (reservation['utilisateur'] == user['_id'])):
                existed_reservation = True
        if existed_reservation or proprity:
            success = f"Vous avez deja fait la reservation !"
            reserved = True
            return render(request, 'event_detail.html', {'event': event, 'events': events, 'createur': createur, 'nombre_reservation': nombre_reservation, 'proprity': proprity,'success': success,'reserved': reserved}) 
        
        reservation_result = db.reservations.insert_one({
            "date_heure": datetime.now(),
            "statut": event['statut'],
            "utilisateur": user['_id'],
            "evenement": event['_id']
        })
        reservation_id = reservation_result.inserted_id

        db.users.update_one(
            {"_id": user['_id']},
            {"$push": {"reservations": reservation_id}}
        )

        db.events.update_one(
            {"_id": event['_id']},
            {"$push": {"reservations": reservation_id}}
        )
        success = f"Reservation reussi !"
        reserved = True
        return render(request, 'event_detail.html', {'event': event, 'events': events, 'createur': createur, 'nombre_reservation': nombre_reservation, 'proprity': proprity,'success': success, 'reserved': reserved}) 
    else:
        error = f"Reservation non prise en charge"
        reserved = False
        return render(request, 'event_detail.html', {'event': event, 'events': events, 'createur': createur, 'nombre_reservation': nombre_reservation, 'proprity': proprity,'error': error, 'reserved': reserved})   

def annuler_reserve_evenement(request, id):
    email = request.session['email']
    events = list(db.events.find())
    for ev in events:
        ev['id'] = str(ev['_id'])
    reserved = False
    event = db.events.find_one({"_id": ObjectId(id)})
    if event:
        # Add this line:
        event['id'] = str(event['_id'])
    user = db.users.find_one({"email":email})
    createur = db.users.find_one({"_id": event['createur']})
    if createur == db.users.find_one({"email":email}):
        proprity = True
    else:
        proprity = False
    nombre_reservation = len(event['reservations'])
    if event and user:
        for reservation in list(db.reservations.find()):
            if ((reservation['evenement'] == event['_id']) and (reservation['utilisateur'] == user['_id'])):
                main_reservation = reservation
        if not main_reservation:
            error = f"Vous ne pouvez pas supprime !"
            reserved = True
            return render(request, 'event_detail.html', {'event': event, 'events': events, 'createur': createur, 'nombre_reservation': nombre_reservation, 'proprity': proprity,'error': error, 'reserved': reserved}) 
        
        delete_result = db.reservations.delete_one({"_id": main_reservation['_id']})
        
        # Retirer la réservation de la liste des réservations de l'utilisateur
        db.users.update_one(
            {"_id": main_reservation['utilisateur']},
            {"$pull": {"reservations": main_reservation['_id']}}
        )
        
        # Retirer la réservation de la liste des réservations de l'événement
        db.events.update_one(
            {"_id": main_reservation['evenement']},
            {"$pull": {"reservations": main_reservation['_id']}}
        )
        success = f"Reservation supprime !"
        reserved = False
        return render(request, 'event_detail.html', {'event': event, 'events': events, 'createur': createur, 'nombre_reservation': nombre_reservation, 'proprity': proprity,'success': success, 'reserved': reserved}) 
    else:
        error = f"Operation non prise en charge"
        reserved = True
        return render(request, 'event_detail.html', {'event': event, 'events': events, 'createur': createur, 'nombre_reservation': nombre_reservation, 'proprity': proprity,'error': error, 'reserved': reserved})   
        
        