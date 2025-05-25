from django.shortcuts import redirect, render
from bson import ObjectId
from django.contrib import messages
from mongo import db  
from datetime import datetime
from collections import Counter
from django.http import JsonResponse

def app_info(request):
    # try:
    #     user_id = ObjectId(id)
    # except Exception:
    #     return render(request, 'admin.html', {'error': "ID utilisateur invalide."})

    # if db is None:
    #     return render(request, 'admin.html', {'error': "Problème de connexion à la base de données."})

    # user = db.users.find_one({"_id": user_id})

    # if not user:
    #     return render(request, 'admin.html', {'error': "Utilisateur introuvable."})

    # if user.get('email') != 'dfasyaka@ept.sn':
    #     return render(request, 'admin.html', {'error': "Vous n'avez pas les droits d'accès."})
    
    try:
        admin = db.admin.find_one({"email": "dfasyaka@ept.sn"})
    except Exception as e:
        return render(request, 'admin.html', {'error': f"Problème sur l'administrateur : {e}"})
        
    
    return render(request, 'admin.html', {
        'admin': admin,

    })

def dashboard(request):
    
    try:
        users = list(db.users.find({}))
        nomber_of_users = len(users)
    except Exception as e:
        return render(request, 'admin/dashboard.html', {'error': f"Problème sur les utilisateurs : {e}"})

    try:
        events = list(db.events.find({}, {"_id": 0}))
        nomber_of_events = len(events)
        events = list(db.events.find({}, {"localisation": 1, "_id": 0}))
        lieux_counts = Counter(event.get('localisation', 'Other') for event in events)

        total = sum(lieux_counts.values())

        lieux_percentages = [
            {'lieu': lieu, 'percentage': round((count / total) * 100, 1)}
            for lieu, count in lieux_counts.items() if (round((count/total)*100) > 10)
        ]
    except Exception as e:
        return render(request, 'admin/dashboard.html', {'error': f"Problème sur les événements : {e}"})

    try:
        reservations = list(db.reservations.find({}, {"_id": 0}))
        nomber_of_reservations = len(reservations)
    except Exception as e:
        return render(request, 'admin/dashboard.html', {'error': f"Problème sur les réservations : {e}"})
    try:

        reservations = list(db.reservations.find({}))

        event_reservation_counts = Counter([r['evenement'] for r in reservations])

        organisateur_reservation_counts = {}

        for user in users:
            user_id = user['_id']
            evenements = user.get("evenements_crees", [])
            
            total_reservations = 0
            for event_id in evenements:
                total_reservations += event_reservation_counts.get(event_id, 0)
            
            organisateur_reservation_counts[user_id] = total_reservations

        top_5 = sorted(organisateur_reservation_counts.items(), key=lambda x: x[1], reverse=True)[:5]
       
        top_names = []
        top_reservation_counts = []

        for user_id, count in top_5:
            user = db.users.find_one({"_id": user_id})
            if user:
                names = user.get("prenom", "")+' '+user.get("nom", "")
                top_names.append(names)
                top_reservation_counts.append(count)


    except Exception as e:
        return render(request, 'admin/dashboard.html', {'error': f"Erreur lors du calcul des top utilisateurs : {e}"})

    
    try:
        admin = db.admin.find_one({"email": "dfasyaka@ept.sn"})
    except Exception as e:
        return render(request, 'admin/dashboard.html', {'error': f"Problème sur l'administrateur : {e}"})
        
    
    return render(request, 'admin/dashboard.html', {
        'nomber_of_users': nomber_of_users,
        'nomber_of_events': nomber_of_events,
        'events': events,
        'users': users,
        'reservations': reservations,
        'admin': admin,
        'nomber_of_reservations': nomber_of_reservations,
        'lieux_percentages': lieux_percentages,
        'top_usernames': top_names,
        'top_reservation_counts': top_reservation_counts,


    })
def format_elapsed_time(timestamp_str):
    try:
        # Convertir la chaîne en timestamp puis en datetime
        event_time = datetime.fromtimestamp(int(timestamp_str))
        now = datetime.now()
        duration = now - event_time
        
        if duration.days > 0:
            return f"il y a {duration.days} jour{'s' if duration.days > 1 else ''}"
        elif duration.seconds >= 3600:
            hours = duration.seconds // 3600
            return f"il y a {hours} heure{'s' if hours > 1 else ''}"
        elif duration.seconds >= 60:
            minutes = duration.seconds // 60
            return f"il y a {minutes} minute{'s' if minutes > 1 else ''}"
        else:
            return f"il y a {duration.seconds} seconde{'s' if duration.seconds > 1 else ''}"
    except (ValueError, TypeError):
        return "à l'instant"

def user_section(request):
    try:
        users = list(db.users.find({}))
        nomber_of_users = len(users)
    except Exception as e:
        return render(request, 'admin/users.html', {'error': f"Problème sur les utilisateurs : {e}"})

    try:
        events = list(db.events.find({}, {"_id": 0}))
        nomber_of_events = len(events)
        events = list(db.events.find({}, {"localisation": 1, "_id": 0}))
        lieux_counts = Counter(event.get('localisation', 'Other') for event in events)

        total = sum(lieux_counts.values())

        lieux_percentages = [
            {'lieu': lieu, 'percentage': round((count / total) * 100, 1)}
            for lieu, count in lieux_counts.items() if (round((count/total)*100) > 10)
        ]
    except Exception as e:
        return render(request, 'admin/users.html', {'error': f"Problème sur les événements : {e}"})

    try:
        reservations = list(db.reservations.find({}, {"_id": 0}))
        nomber_of_reservations = len(reservations)
    except Exception as e:
        return render(request, 'admin/users.html', {'error': f"Problème sur les réservations : {e}"})
    try:

        reservations = list(db.reservations.find({}))

        event_reservation_counts = Counter([r['evenement'] for r in reservations])
        organisateur_reservation_counts = {}

        for user in users:
            user_id = user['_id']
            evenements = user.get("evenements_crees", [])
            
            total_reservations = 0
            for event_id in evenements:
                total_reservations += event_reservation_counts.get(event_id, 0)
            
            organisateur_reservation_counts[user_id] = total_reservations

        top_5 = sorted(organisateur_reservation_counts.items(), key=lambda x: x[1], reverse=True)[:5]
       
        top_names = []
        top_reservation_counts = []

        for user_id, count in top_5:
            user = db.users.find_one({"_id": user_id})
            if user:
                names = user.get("prenom", "")+' '+user.get("nom", "")
                top_names.append(names)
                top_reservation_counts.append(count)


    except Exception as e:
        return render(request, 'admin/users.html', {'error': f"Erreur lors du calcul des top utilisateurs : {e}"})

    
    try:
        admin = db.admin.find_one({"email": "dfasyaka@ept.sn"})
    except Exception as e:
        return render(request, 'admin/users.html', {'error': f"Problème sur l'administrateur : {e}"})
    messages_with_time = []
    for message in messages.get_messages(request):
        elapsed_time = format_elapsed_time(message.extra_tags)
        messages_with_time.append({
            'message': message.message,
            'elapsed_time': elapsed_time
        })
    
    return render(request, 'admin/users.html', {
            'nomber_of_users': nomber_of_users,
            'nomber_of_events': nomber_of_events,
            'events': events,
            'users': users,
            'reservations': reservations,
            'admin': admin,
            'nomber_of_reservations': nomber_of_reservations,
            'lieux_percentages': lieux_percentages,
            'top_usernames': top_names,
            'top_reservation_counts': top_reservation_counts,
            'formatted_messages': messages_with_time


        })
def event_section(request):
    try:
        users = list(db.users.find({}))
        nomber_of_users = len(users)
    except Exception as e:
        return render(request, 'admin/events_admin.html', {'error': f"Problème sur les utilisateurs : {e}"})

    try:
        events = list(db.events.find())
        for ev in events:
            ev['id'] = str(ev['_id'])
        nomber_of_events = len(events)
        lieux_counts = Counter(event.get('localisation', 'Other') for event in events)

        total = sum(lieux_counts.values())

        lieux_percentages = [
            {'lieu': lieu, 'percentage': round((count / total) * 100, 1)}
            for lieu, count in lieux_counts.items() if (round((count/total)*100) > 10)
        ]
    except Exception as e:
        return render(request, 'admin/events_admin.html', {'error': f"Problème sur les événements : {e}"})

    try:
        reservations = list(db.reservations.find({}, {"_id": 0}))
        nomber_of_reservations = len(reservations)
    except Exception as e:
        return render(request, 'admin/events_admin.html', {'error': f"Problème sur les réservations : {e}"})
    try:

        reservations = list(db.reservations.find({}))

        event_reservation_counts = Counter([r['evenement'] for r in reservations])

        organisateur_reservation_counts = {}

        for user in users:
            user_id = user['_id']
            evenements = user.get("evenements_crees", [])
            
            total_reservations = 0
            for event_id in evenements:
                total_reservations += event_reservation_counts.get(event_id, 0)
            
            organisateur_reservation_counts[user_id] = total_reservations

        top_5 = sorted(organisateur_reservation_counts.items(), key=lambda x: x[1], reverse=True)[:5]
       
        top_names = []
        top_reservation_counts = []

        for user_id, count in top_5:
            user = db.users.find_one({"_id": user_id})
            if user:
                names = user.get("prenom", "")+' '+user.get("nom", "")
                top_names.append(names)
                top_reservation_counts.append(count)


    except Exception as e:
        return render(request, 'admin/events_admin.html', {'error': f"Erreur lors du calcul des top utilisateurs : {e}"})

    
    try:
        admin = db.admin.find_one({"email": "dfasyaka@ept.sn"})
    except Exception as e:
        return render(request, 'admin/events_admin.html', {'error': f"Problème sur l'administrateur : {e}"})
    messages_with_time = []
    for message in messages.get_messages(request):
        elapsed_time = format_elapsed_time(message.extra_tags)
        messages_with_time.append({
            'message': message.message,
            'elapsed_time': elapsed_time
    })
    
    return render(request, 'admin/events_admin.html', {
        'nomber_of_users': nomber_of_users,
        'nomber_of_events': nomber_of_events,
        'events': events,
        'users': users,
        'reservations': reservations,
        'admin': admin,
        'nomber_of_reservations': nomber_of_reservations,
        'lieux_percentages': lieux_percentages,
        'top_usernames': top_names,
        'top_reservation_counts': top_reservation_counts,
        'formatted_messages': messages_with_time


    })
    

def search_events(request):
    """
    Vue pour rechercher des événements selon un mot-clé.
    """
    keyword = request.GET.get('keyword', '').strip()
    
    if not keyword:
        return redirect('event_section')
    
    try:
        # Créer une requête de recherche avec regex pour une recherche insensible à la casse
        search_query = {"$or": [
            {"titre": {"$regex": keyword, "$options": "i"}},
            {"description": {"$regex": keyword, "$options": "i"}},
            {"localisation": {"$regex": keyword, "$options": "i"}},
            {"categorie": {"$regex": keyword, "$options": "i"}}
        ]}
        
        # Rechercher les événements correspondant au mot-clé
        events = list(db.events.find(search_query))
        for ev in events:
            ev['id'] = str(ev['_id'])
        
        nomber_of_events = len(events)
        
        admin = db.admin.find_one({"email": "dfasyaka@ept.sn"})
        
        messages_with_time = []
        for message in messages.get_messages(request):
            elapsed_time = format_elapsed_time(message.extra_tags)
            messages_with_time.append({
                'message': message.message,
                'elapsed_time': elapsed_time
            })
        
        search_message = f"Recherche pour '{keyword}': {nomber_of_events} événement(s) trouvé(s)"
        messages.info(request, search_message)
        
        return render(request, 'admin/events_admin.html', {
            'nomber_of_events': nomber_of_events,
            'events': events,
            'admin': admin,
            'formatted_messages': messages_with_time,
            'search_keyword': keyword
        })
    
    except Exception as e:
        messages.error(request, f"Erreur lors de la recherche: {e}")
        return redirect('event_section')


def search_users(request):
    """
    Vue pour rechercher des utilisateurs selon un mot-clé.
    """
    keyword = request.GET.get('keyword', '').strip()
    
    if not keyword:
        return redirect('user_section')
    
    try:
        # Créer une requête de recherche avec regex pour une recherche insensible à la casse
        search_query = {"$or": [
            {"nom": {"$regex": keyword, "$options": "i"}},
            {"prenom": {"$regex": keyword, "$options": "i"}},
            {"email": {"$regex": keyword, "$options": "i"}},
            {"telephone": {"$regex": keyword, "$options": "i"}},
            {"adresse": {"$regex": keyword, "$options": "i"}}
        ]}
        
        users = list(db.users.find(search_query))
        nomber_of_users = len(users)
        
        admin = db.admin.find_one({"email": "dfasyaka@ept.sn"})
        
        messages_with_time = []
        for message in messages.get_messages(request):
            elapsed_time = format_elapsed_time(message.extra_tags)
            messages_with_time.append({
                'message': message.message,
                'elapsed_time': elapsed_time
            })
        
        search_message = f"Recherche pour '{keyword}': {nomber_of_users} utilisateur(s) trouvé(s)"
        print(search_message)
        messages.info(request, search_message)
        
        return render(request, 'admin/users.html', {
            'nomber_of_users': nomber_of_users,
            'users': users,
            'admin': admin,
            'formatted_messages': messages_with_time,
            'search_keyword': keyword
        })
    
    except Exception as e:
        messages.error(request, f"Erreur lors de la recherche: {e}")
        return redirect('user_section')
        
def delete_user(request, email):
    if request.method == 'POST':
        user = db.users.find_one({"email": email})
        if user:
            deletion_time = datetime.now()
            
            timestamp = int(deletion_time.timestamp())
            
            db.users.delete_one({"email": email})
            notification = f"L'utilisateur avec l'email {email} a été supprimé avec succès."
            
            messages.success(request, notification, extra_tags=str(timestamp))
            return redirect('user_section')
        else:
            error = f"L'utilisateur avec l'email {email} n'existe pas."
            return render(request, 'admin/users.html', {'error': error})
def delete_event(request, id):
    if request.method == 'POST':
        
        event = db.events.find_one({"_id": ObjectId(id)})
        if event:
            deletion_time = datetime.now()
            
            timestamp = int(deletion_time.timestamp())
            
            db.events.delete_one({"_id": ObjectId(id)})
            notification = f"Vous avez supprime l'événement {event['titre']}"
            
            messages.success(request, notification, extra_tags=str(timestamp))
            return redirect('event_section')
        else:
            error = f"L'événement n'existe pas."
            return render(request, 'admin/events_admin.html', {'error': error})
    
        
def stats_view(request):
    try:
        events = list(db.events.find({}, {"localisation": 1, "categorie": 1, "_id": 0}))
        lieux = [e["localisation"] for e in events if "localisation" in e]
        lieu_stats = Counter(lieux)
        categories = [e["categorie"] for e in events if "categorie" in e]
        categorie_stats = Counter(categories)
        

        return JsonResponse({
            "lieux": {
                "labels": list(lieu_stats.keys()),
                "data": list(lieu_stats.values())
            },
            "categories": {
                "labels": list(categorie_stats.keys()),
                "data": list(categorie_stats.values())
            }
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
