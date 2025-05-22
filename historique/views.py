from bson import ObjectId
from django.shortcuts import render
from datetime import datetime
from mongo import db  
def get_historique(request, email):
    if db is not None:
        try:
            user = db.users.find_one({"email": email})
        except Exception as e:
            return render(request, 'historique.html', {'error': f"email invalide: {e}"})

        if not user:
            return render(request, 'historique.html', {'error': "Utilisateur non trouvé."})
        user_id = user['_id']
        events = []
        list_events = list(db.events.find({"creator": user_id}))
        for event in list_events:
            if event['date_heure'] < datetime.now():
                events.append(event)
        
        return render(request, 'historique.html', {
            'events': events
        })
    else:
        return render(request, 'historique.html', {'error': "Base de données non disponible."})