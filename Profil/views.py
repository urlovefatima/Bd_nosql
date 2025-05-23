from django.shortcuts import render
from mongo import db
from django.shortcuts import render, redirect
from django.contrib import messages

def profil_utilisateur(request):
    email = request.session.get('email')

    if not email:
        messages.error(request, "Vous devez être connecté pour accéder à votre profil.")
        return redirect('connexion')

    utilisateur = db.users.find_one({'email': email})

    if not utilisateur:
        messages.error(request, "Utilisateur introuvable.")
        return redirect('connexion')
    events = list[db.events.find({'createur': utilisateur['_id']})]
    reserved_events = list[db.reservations.find({'utilisateur':utilisateur['_id']})]

    return render(request, 'profil.html', {'utilisateur': utilisateur, 'events': events, 'reserved_events': reserved_events})
def consulted_profil(request, email):
    if request.method == 'POST':
        utilisateur = db.users.find_one({"email": email})
        if not utilisateur:
            messages.error(request, "Utilisateur introuvable.")
            return redirect('accueil')
        events = list[db.events.find({'createur': utilisateur['_id']})]
        reserved_events = list[db.reservations.find({'utilisateur':utilisateur['_id']})]
    
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