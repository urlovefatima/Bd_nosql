from django.shortcuts import get_object_or_404, render
from bson import ObjectId
from mongo import db  

def get_events(request):
    if db is not None :
        events = list(db.events.find({}, {"_id": 0}))
        return render(request, 'events.html', {'events': events})
    else:
        return render(request, 'events.html', {'events': []})
def get_historique(request, pk):
    if db is not None:
        try:
            user_id = ObjectId(pk)
        except Exception as e:
            return render(request, 'historique.html', {'error': f"ID invalide: {e}"})

        user = db.users.find_one({"_id": user_id})
        if not user:
            return render(request, 'historique.html', {'error': "Utilisateur non trouvé."})

       
        events = list(db.events.find({"creator": user_id}))

        return render(request, 'historique.html', {
            'events': events,
            'user': user
        })
    else:
        return render(request, 'historique.html', {'error': "Base de données non disponible."})
    


