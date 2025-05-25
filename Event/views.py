from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from bson import ObjectId
from datetime import datetime
from mongo import db

def post_event(request, id):
    email = request.session.get('email')
    events = list(db.events.find())
    for ev in events:
        ev['id'] = str(ev['_id'])
    
    event = db.events.find_one({"_id": ObjectId(id)})
    if event:
        event['id'] = str(event['_id'])
        user = db.users.find_one({"_id": event['createur']})
        current_user = db.users.find_one({"email": email})
        
        # Corriger la logique de comparaison
        if user and current_user and user['_id'] == current_user['_id']:
            proprity = True
        else:
            proprity = False
            
        nombre_reservation = len(event['reservations'])
        
        # Vérifier si l'utilisateur actuel a déjà une réservation
        reserved = False
        if current_user:
            for reservation in list(db.reservations.find()):
                if ((reservation['evenement'] == event['_id']) and (reservation['utilisateur'] == current_user['_id'])):
                    reserved = True
                    break
        
        return render(request, 'event_detail.html', {
            'event': event, 
            'events': events, 
            'user': user,  # Créateur de l'événement
            'current_user': current_user,  # Utilisateur connecté
            'nombre_reservation': nombre_reservation, 
            'proprity': proprity,
            'reserved': reserved
        })
    else:
        error = f"L'événement n'existe pas."
        return render(request, 'event_detail.html', {'error': error})

def reserve_evenement(request, id):
    email = request.session.get('email')
    events = list(db.events.find())
    for ev in events:
        ev['id'] = str(ev['_id'])
    
    reserved = False
    event = db.events.find_one({"_id": ObjectId(id)})
    if event:
        event['id'] = str(event['_id'])
    
    user = db.users.find_one({"email": email})
    createur = db.users.find_one({"_id": event['createur']})
    
    # Corriger la logique de comparaison
    if createur and user and createur['_id'] == user['_id']:
        proprity = True
    else:
        proprity = False
    
    nombre_reservation = len(event['reservations'])
    existed_reservation = False
    
    if event and user:
        # Vérifier si une réservation existe déjà
        for reservation in list(db.reservations.find()):
            if ((reservation['evenement'] == event['_id']) and (reservation['utilisateur'] == user['_id'])):
                existed_reservation = True
                break
        
        if existed_reservation or proprity:
            success = f"Vous avez déjà fait la réservation !"
            reserved = True
            return render(request, 'event_detail.html', {
                'event': event, 
                'events': events, 
                'user': createur,  # Créateur pour l'affichage
                'createur': createur, 
                'nombre_reservation': nombre_reservation, 
                'proprity': proprity,
                'success': success,
                'reserved': reserved
            }) 
        
        # Créer la réservation
        reservation_result = db.reservations.insert_one({
            "date_heure": datetime.now(),
            "statut": event['statut'],
            "utilisateur": user['_id'],
            "evenement": event['_id']
        })
        reservation_id = reservation_result.inserted_id

        # Mettre à jour les collections
        db.users.update_one(
            {"_id": user['_id']},
            {"$push": {"reservations": reservation_id}}
        )

        db.events.update_one(
            {"_id": event['_id']},
            {"$push": {"reservations": reservation_id}}
        )
        
        success = f"Réservation réussie !"
        reserved = True
        # Recalculer le nombre de réservations après ajout
        nombre_reservation = len(event['reservations']) + 1
        
        return render(request, 'event_detail.html', {
            'event': event, 
            'events': events, 
            'user': createur,  # Créateur pour l'affichage
            'createur': createur, 
            'nombre_reservation': nombre_reservation, 
            'proprity': proprity,
            'success': success, 
            'reserved': reserved
        }) 
    elif not event:
        error = f"Opération non prise en charge"
        reserved = False
        return redirect("get_events")  
    else:
        return redirect("connexion")

def annuler_reserve_evenement(request, id):
    email = request.session.get('email')
    events = list(db.events.find())
    for ev in events:
        ev['id'] = str(ev['_id'])
    
    reserved = False
    event = db.events.find_one({"_id": ObjectId(id)})
    if event:
        event['id'] = str(event['_id'])
    
    user = db.users.find_one({"email": email})
    createur = db.users.find_one({"_id": event['createur']})
    
    # Corriger la logique de comparaison
    if createur and user and createur['_id'] == user['_id']:
        proprity = True
    else:
        proprity = False
    
    nombre_reservation = len(event['reservations'])
    main_reservation = None  # Initialiser la variable
    
    if event and user:
        # Trouver la réservation de l'utilisateur
        for reservation in list(db.reservations.find()):
            if ((reservation['evenement'] == event['_id']) and (reservation['utilisateur'] == user['_id'])):
                main_reservation = reservation
                break
        
        if not main_reservation:
            error = f"Vous ne pouvez pas supprimer !"
            reserved = False  # L'utilisateur n'a pas de réservation
            return render(request, 'event_detail.html', {
                'event': event, 
                'events': events, 
                'user': createur,  # Créateur pour l'affichage
                'createur': createur, 
                'nombre_reservation': nombre_reservation, 
                'proprity': proprity,
                'error': error, 
                'reserved': reserved
            }) 
        
        # Supprimer la réservation
        delete_result = db.reservations.delete_one({"_id": main_reservation['_id']})
        
        # Mettre à jour les collections
        db.users.update_one(
            {"_id": main_reservation['utilisateur']},
            {"$pull": {"reservations": main_reservation['_id']}}
        )
        
        db.events.update_one(
            {"_id": main_reservation['evenement']},
            {"$pull": {"reservations": main_reservation['_id']}}
        )
        
        success = f"Réservation supprimée !"
        reserved = False
        # Recalculer le nombre de réservations après suppression
        nombre_reservation = len(event['reservations']) - 1
        
        return render(request, 'event_detail.html', {
            'event': event, 
            'events': events, 
            'user': createur,  # Créateur pour l'affichage
            'createur': createur, 
            'nombre_reservation': nombre_reservation, 
            'proprity': proprity,
            'success': success, 
            'reserved': reserved
        }) 
    elif not event:
        error = f"Opération non prise en charge"
        reserved = False
        return redirect("get_events")  
    else:
        return redirect("connexion")
        
def delete_event(request, id):
    email = request.session['email']
    user = db.users.find_one({"email": email})
    
    # Récupérer l'événement AVANT de définir le créateur
    event = db.events.find_one({"_id": ObjectId(id)})
    if not event:
        messages.error(request, "L'événement n'existe pas.")
        return redirect("profil_utilisateur")
    
    createur = db.users.find_one({"_id": event['createur']})
    
    # Vérifier si l'utilisateur est le créateur
    if createur and user and createur['_id'] == user['_id']:
        event_id = event['_id']
        
        # Supprimer l'événement
        db.events.delete_one({"_id": event_id})
        
        # Mettre à jour l'utilisateur (corriger 'id' en '_id')
        db.users.update_one(
            {"_id": user['_id']},
            {"$pull": {"evenement_cree": event_id}}
        )
        
        # Supprimer TOUTES les réservations liées à cet événement
        db.reservations.delete_many({"evenement": event_id})
        
        messages.success(request, "Événement supprimé avec succès.")
        return redirect("profil_utilisateur")
    else:
        # Si l'utilisateur n'est pas le créateur, rediriger avec erreur
        events = list(db.events.find())
        for ev in events:
            ev['id'] = str(ev['_id'])
        
        event['id'] = str(event['_id'])
        proprity = False
        nombre_reservation = len(event['reservations'])
        error = f"Opération non prise en charge"
        reserved = False
        
        return render(request, 'event_detail.html', {
            'event': event, 
            'events': events, 
            'user': createur,  # Créateur pour l'affichage
            'createur': createur, 
            'nombre_reservation': nombre_reservation, 
            'proprity': proprity,
            'error': error, 
            'reserved': reserved
        })