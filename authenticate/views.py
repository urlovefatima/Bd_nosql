from django.shortcuts import render, redirect
from mongo import db
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from datetime import datetime, timedelta
from bson import ObjectId
import re
import os
import uuid
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from PIL import Image
import io

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
        list_admin = ["dfasyaka@ept.sn"]
        user_doc = {
            "nom": data['nom'],
            "prenom": data['prenom'],
            "username": data['username'],
            "email": data['email'],
            "tel": data['telephone'],
            "date_de_naissance": data['bornday'],
            "mot_de_passe": make_password(data['password']),
            "photo_profil": "/media/profile_default.jpeg"
        }
        print("insertion en cours")
        if user_doc['email'] in list_admin:
            db.admin.insert_one(user_doc)
            db.users.insert_one(user_doc)
        else:
            db.users.insert_one(user_doc)
        print("insertion reussie")
        request.session['email'] = user_doc['email']
        messages.success(request, "Inscription réussie. Vous pouvez maintenant vous connecter.")
        return redirect('upload_photo')


    return render(request, 'inscription.html',  {'success': "Inscription réussie. Vous pouvez maintenant vous connecter."})


def upload_photo(request):
    if request.method == 'POST':
        erreurs = []
        
        # Vérifier si un fichier a été téléchargé
        if 'photo_profil' not in request.FILES:
            erreurs.append("Aucune photo sélectionnée.")
            return render(request, 'upload_photo.html', {'erreurs': erreurs})
        
        photo_file = request.FILES['photo_profil']
        
        # Vérifier si le fichier n'est pas vide
        if photo_file.size == 0:
            erreurs.append("Le fichier sélectionné est vide.")
            return render(request, 'upload_photo.html', {'erreurs': erreurs})
        
        # Vérifier la taille du fichier (5MB max)
        if photo_file.size > 5 * 1024 * 1024:  # 5MB
            erreurs.append("Le fichier est trop volumineux. Taille maximum: 5MB")
            return render(request, 'upload_photo.html', {'erreurs': erreurs})
        
        # Vérifier le type de fichier
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
        if photo_file.content_type not in allowed_types:
            erreurs.append("Type de fichier non autorisé. Utilisez JPG, PNG ou GIF.")
            return render(request, 'upload_photo.html', {'erreurs': erreurs})
        
        # Vérifier l'extension du fichier
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif']
        file_extension = os.path.splitext(photo_file.name)[1].lower()
        if file_extension not in allowed_extensions:
            erreurs.append("Extension de fichier non autorisée.")
            return render(request, 'upload_photo.html', {'erreurs': erreurs})
        
        try:
            
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            image = Image.open(photo_file)

            if image.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'P':
                    image = image.convert('RGBA')
                background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                image = background

            output = io.BytesIO()
            image.save(output, format='JPEG', quality=85, optimize=True)
            output.seek(0)

            file_path = f"profile_photos/{unique_filename}"
            saved_path = default_storage.save(file_path, ContentFile(output.read()))
            email = request.session.get('email')
            
            if not email:
                erreurs.append("Utilisateur non identifié. Veuillez vous reconnecter.")
                return render(request, 'upload_photo.html', {'erreurs': erreurs})
            
            
            photo_url = f"/media/{saved_path}"
            
            user_updated = db.users.update_one(
                {"email": email},
                {"$set": {"photo_profil": photo_url}}
            )
            
            
            if user_updated.matched_count == 0:
                admin_updated = db.admin.update_one(
                    {"email": email},
                    {"$set": {"photo_profil": photo_url}}
                )
                
                if admin_updated.matched_count == 0:
                    erreurs.append("Utilisateur non trouvé dans la base de données.")
                    
                    if default_storage.exists(saved_path):
                        default_storage.delete(saved_path)
                    return render(request, 'upload_photo.html', {'erreurs': erreurs})
            
            messages.success(request, "Photo de profil mise à jour avec succès!")
            return redirect('accueil')
            
        except Exception as e:
            erreurs.append(f"Erreur lors du traitement de l'image: {str(e)}")
            return render(request, 'upload_photo.html', {'erreurs': erreurs})
    
    return render(request, 'upload_photo.html')


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
    events = list(db.events.find())
    events_six = []
    for event in events:
        event['id'] = str(event['_id'])
        if event['date_heure'] >= datetime.now():
                events_six.append(event)
    events_six = sorted(events_six, key=lambda e: e['date_heure'])
    return render(request, 'accueil.html', {'events': events, "events_six": events_six})




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
