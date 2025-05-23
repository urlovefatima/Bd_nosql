from django.shortcuts import render, redirect
# from mongo import users_collection, reservations_collection, events_collection
from mongo import db
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from datetime import datetime
from bson import ObjectId
import re


# Create your views here.

def inscription(request):
    if request.method == 'POST':
        data = request.POST
        erreurs = []
        print(data)

        if db.users.find_one({"username": data['username']}):
            erreurs.append("Nom d'utilisateur déjà pris!")
        email = data.get('email', '')
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            erreurs.append("Email invalide.")
        password = data.get('password', '')
        if len(password) < 8:
            erreurs.append("Mot de passe trop court (minimum 8 caractères).")
        if not re.search(r"[A-Z]", password):
            erreurs.append("Mot de passe : au moins une majuscule.")
        if not re.search(r"[a-z]", password):
            erreurs.append("Mot de passe : au moins une minuscule.")
        if not re.search(r"[0-9]", password):
            erreurs.append("Mot de passe : au moins un chiffre.")

        confirmation = data.get('repeatPassword', '')
        if confirmation != password:
            erreurs.append("Les mots de passe ne correspondent pas")
        if erreurs:
            return render(request, 'inscription.html', {'erreurs': erreurs})
        
        user_doc = {
            "nom": data['nom'],
            "prenom": data['prenom'],
            "username": data['username'],
            "email": data['email'],
            "tel": data['telephone'],
            "date_de_naissance": data['bornday'],
            "mot_de_passe": make_password(data['password'])
        }
        print("insertion en cours")
        db.users.insert_one(user_doc)
        print("insertion reussie")
        messages.success(request, "Inscription réussie. Vous pouvez maintenant vous connecter.")
        return redirect('connexion')


    return render(request, 'inscription.html',  {'success': "Inscription réussie. Vous pouvez maintenant vous connecter."})


def connexion(request):
    if request.method == 'POST':
        data = request.POST
        email = data.get('email', '')
        password = data.get('password', '')

        if not email or not password:
            print("erreur")
            messages.error(request, "Email ou mot de passe manquant.")
            return render(request, 'connexion.html')

        user = db.users.find_one({'email': email})

        if user and check_password(password, user['mot_de_passe']):
            request.session['email'] = email
            messages.success(request, "Connexion réussie.")
            return redirect('accueil')
        else:
            print("erreur 2")
            messages.error(request, "Email ou mot de passe incorrect.")
            return render(request, 'connexion.html')
    else:
        return render(request, 'connexion.html')

def deconnexion(request):
    try:
        del request.session['email']
    except KeyError:
        pass
    messages.success(request, "Vous avez été déconnecté.")
    return redirect('connexion')


def accueil(request):
    events = list[db.events.find({})]
    return render(request, 'accueil.html', {'events': events})




def reserver_evenement(request, event_id):
    if request.method == "POST":
        user_email = request.session.get("email")
        if not user_email:
            messages.error(request, "Vous devez être connecté pour réserver.")
            return redirect("connexion")

        event = db.events.find_one({"_id": ObjectId(event_id)})
        if not event:
            messages.error(request, "Événement introuvable.")
            return redirect("liste_evenements")

        # Vérifie si l'utilisateur a déjà réservé
        already_reserved = db.reservations.find_one({
            "event_id": ObjectId(event_id),
            "user_email": user_email
        })
        if already_reserved:
            messages.warning(request, "Vous avez déjà réservé cet événement.")
            return redirect("liste_evenements")

        # Compter les réservations actuelles
        count = db.reservations.count_documents({"event_id": ObjectId(event_id)})

        if count >= event.get("max_places", 0):
            messages.error(request, "Il n'y a plus de places disponibles.")
            return redirect("liste_evenements")

        # Réservation
        db.reservations.insert_one({
            "event_id": ObjectId(event_id),
            "user_email": user_email,
            "timestamp": datetime.now()
        })
        messages.success(request, "Réservation réussie.")
        return redirect("liste_evenements")
    




def annuler_reservation(request, event_id):
    user_email = request.session.get("email")
    if not user_email:
        messages.error(request, "Vous devez être connecté pour annuler.")
        return redirect("connexion")

    result = db.reservations.delete_one({
        "event_id": ObjectId(event_id),
        "user_email": user_email
    })

    if result.deleted_count:
        messages.success(request, "Réservation annulée.")
    else:
        messages.warning(request, "Vous n'aviez pas réservé cet événement.")
    return redirect("liste_evenements")




def nombre_reservations(event_id):
    return db.reservations.count_documents({
        "event_id": ObjectId(event_id)
    })
