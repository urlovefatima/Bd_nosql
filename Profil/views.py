from django.shortcuts import render
from mongo import db
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from bson.objectid import ObjectId
from django.conf import settings
from PIL import Image
import os

def profil_utilisateur(request):
    email = request.session.get('email')
    is_admin = False
    if not email:
        messages.error(request, "Vous devez être connecté pour accéder à votre profil.")
        return redirect('connexion')

    utilisateur = db.users.find_one({'email': email})

    if not utilisateur:
        messages.error(request, "Utilisateur introuvable.")
        return redirect('connexion')
    if db.admin.find_one({"email": email}):
        is_admin = True
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
    return render(request, 'profil.html', {'utilisateur': utilisateur, 'events': events, 'reserved_events': reserved_events, "is_admin": is_admin})
def consulted_profil(request, email):
    email_verify = request.session.get('email')
    if email_verify == email:
        return redirect("profil_utilisateur")
    utilisateur = db.users.find_one({"email": email})
    if not utilisateur:
        messages.error(request, "Utilisateur introuvable.")
        return redirect('accueil')
    consulted = True
    events = []
    for event in list(db.events.find({'createur': utilisateur['_id']})):
        if event['date_heure'] > datetime.now():
            events.append(event)
    events = sorted(events, key=lambda e: e['date_heure'])
    for ev in events:
            ev['id'] = str(ev['_id'])
    return render(request, 'profil.html', {'utilisateur': utilisateur, 'events': events, "consulted": consulted})


def infos_utilisateur(request):
    email = request.session.get('email')

    if not email:
        messages.error(request, "Vous devez être connecté pour accéder à votre profil.")
        return redirect('connexion')
    
    utilisateur = db.users.find_one({'email': email})
    id = utilisateur['_id']
    
    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        username = request.POST.get('username')
        email= request.POST.get('email')
        tel = request.POST.get('tel')
        date_de_naissance= request.POST.get('date_de_naissance')
        photo_profil=request.FILES.get('image')
        photo_profil_url = utilisateur.get('photo_profil')

        if photo_profil:
            try:
                img = Image.open(photo_profil)
                img.verify()

                file_path = os.path.join(settings.MEDIA_ROOT, photo_profil.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in photo_profil.chunks():
                        destination.write(chunk)

                photo_profil_url = f"/media/{photo_profil.name}"

            except (IOError, SyntaxError):
                return render(request, 'infos-user.html', {
                    'utilisateur': utilisateur,
                    'error': "Le fichier téléchargé n'est pas une image valide."
                })

        db.users.update_one(
            {'_id': ObjectId(id)},
            {'$set': {
            'nom': nom,
            'prenom': prenom,
            'username':username,
            'email': email,
            'tel': tel,
            'date_de_naissance': date_de_naissance,
            'photo_profil': photo_profil_url
            }}
        )
                    
        return redirect('infos-user')

    return render(request, 'infos-user.html', {'utilisateur': utilisateur})
    