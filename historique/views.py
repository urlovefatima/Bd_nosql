from bson import ObjectId
from django.shortcuts import render, redirect
from datetime import datetime
from mongo import db  
def get_historique_event(request, email):
    email_verifie = request.session.get('email')
    if db is not None:
        try:
            user = db.users.find_one({"email": email})
        except Exception as e:
            return render(request, 'profil.html', {'error': f"email invalide: {e}"})

        if not user or (email_verifie != email):
            return redirect("connexion")
        
        user_id = user['_id']
        events_created = []
        list_events = db.events.find({"createur": user_id})
        for event in list_events:
            if event['date_heure'] < datetime.now():
                events_created.append(event)
        events_created = sorted(events_created, key=lambda e: e['date_heure'], reverse=True)
        for event in events_created:
            event['id'] = str(event['_id'])
        print(events_created)
        return render(request, 'historique_events.html', {
            'events_created': events_created
        })
    else:
        return render(request, 'profil.html', {'error': "Base de données non disponible."})
def get_historique_event_reserved(request, email):
    if db is not None:
        try:
            user = db.users.find_one({"email": email})
        except Exception as e:
            return render(request, 'profil.html', {'error': f"email invalide: {e}"})

        if not user:
            return render(request, 'profil.html', {'error': "Utilisateur non trouvé."})
        user_id = user['_id']
        events_reserve = []
        list_reserve = list(db.reservations.find({'utilisateur': user_id}))
        for reserve in list_reserve:
            event_reserved = db.events.find_one({'_id': reserve['evenement']})
            if event_reserved['date_heure'] < datetime.now():
                events_reserve.append(event_reserved)
        events_reserve = sorted(events_reserve, key=lambda e: e['date_heure'], reverse=True)
        return render(request, 'historique_reserve.html', {
            'events_reserve': events_reserve
        })
    else:
        return render(request, 'profil.html', {'error': "Base de données non disponible."})