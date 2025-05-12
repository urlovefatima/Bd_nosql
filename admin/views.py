from django.shortcuts import render
from bson import ObjectId
from mongo import db  

def app_info(request, id):
    try:
        user_id = ObjectId(id)
    except Exception:
        return render(request, 'admin.html', {'error': "ID utilisateur invalide."})

    if db is None:
        return render(request, 'admin.html', {'error': "Problème de connexion à la base de données."})

    user = db.users.find_one({"_id": user_id})

    if not user:
        return render(request, 'admin.html', {'error': "Utilisateur introuvable."})

    if user.get('email') != 'dfasyaka@ept.sn':
        return render(request, 'admin.html', {'error': "Vous n'avez pas les droits d'accès."})

    try:
        users = list(db.users.find({}, {"_id": 0}))
    except Exception as e:
        return render(request, 'admin.html', {'error': f"Problème sur les utilisateurs : {e}"})

    try:
        events = list(db.events.find({}, {"_id": 0}))
    except Exception as e:
        return render(request, 'admin.html', {'error': f"Problème sur les événements : {e}"})

    try:
        reservations = list(db.reservations.find({}, {"_id": 0}))
    except Exception as e:
        return render(request, 'admin.html', {'error': f"Problème sur les réservations : {e}"})

    return render(request, 'events.html', {
        'events': events,
        'users': users,
        'reservations': reservations
    })
