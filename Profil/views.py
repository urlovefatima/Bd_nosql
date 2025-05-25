from django.shortcuts import render
from mongo import db
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime

def profil_utilisateur(request):
    email = request.session.get('email')

    if not email:
        messages.error(request, "Vous devez être connecté pour accéder à votre profil.")
        return redirect('connexion')

    utilisateur = db.users.find_one({'email': email})

    if not utilisateur:
        messages.error(request, "Utilisateur introuvable.")
        return redirect('connexion')
    from datetime import datetime

    events = []
    reserved_events = []

    for event in list(db.events.find({'createur': utilisateur['_id']})):
        if event['date_heure'] > datetime.now():
            events.append(event)

    for reserve in list(db.reservations.find({'utilisateur': utilisateur['_id']})):
        event_reserved = db.events.find_one({'_id': reserve['evenement']})
        if event_reserved and event_reserved['date_heure'] > datetime.now():
            reserved_events.append(event_reserved)

    events = sorted(events, key=lambda e: e['date_heure'])
    reserved_events = sorted(reserved_events, key=lambda e: e['date_heure'])
    for ev in events:
            ev['id'] = str(ev['_id'])
    for ev in reserved_events:
            ev['id'] = str(ev['_id'])
    return render(request, 'profil.html', {'utilisateur': utilisateur, 'events': events, 'reserved_events': reserved_events})
def consulted_profil(request, email):
    if request.method == 'POST':
        utilisateur = db.users.find_one({"email": email})
        if not utilisateur:
            messages.error(request, "Utilisateur introuvable.")
            return redirect('accueil')
        events = []
        for event in list(db.events.find({'createur': utilisateur['_id']})):
            if event['date_heure'] > datetime.now():
                events.append(event)
        events = sorted(events, key=lambda e: e['date_heure'])
    else:
        return render(request, 'profil.html')

    return render(request, 'profil.html', {'utilisateur': utilisateur, 'events': events, 'reserved_events': reserved_events})


def infos_utilisateur(request):
    email = request.session.get('email')

    if not email:
        messages.error(request, "Vous devez être connecté pour accéder à votre profil.")
        return redirect('connexion')

    utilisateur = db.users.find_one({'email': email})

    return render(request, 'infos-user.html', {'utilisateur': utilisateur})
