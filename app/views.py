<<<<<<< HEAD
from django.shortcuts import render, redirect
from mongo import db 
from bson.objectid import ObjectId 
=======
from django.shortcuts import get_object_or_404, render
from bson import ObjectId
from mongo import db  
>>>>>>> 8a8a7e7cb8c338d3e55400d5d029ce7c08a02694

def get_events(request):
    if db is not None :
        events = list(db.events.find({}, {"_id": 0}))
        return render(request, 'events.html', {'events': events})
    else:
        return render(request, 'events.html', {'events': []})
<<<<<<< HEAD

def get_events_categories(request):
    if db is not None :
        categories = list(db.events.distinct("categorie"))
        events = list(db.events.find({}, {"_id": 0}))
        return render(request, 'categories.html', {'categories': categories, 'events': events})
    else:
        return render(request, 'categories.html', {'categories': [], 'events': []})
    

def delete_event(request):
    if request.method == "POST":
        event_id = request.POST.get("event_id")
        if event_id:
            db.events.delete_one({"_id": ObjectId(event_id)})
        return redirect("delete_event")

    events = list(db.events.find())
    for e in events:
        e["id"] = str(e["_id"])
    return render(request, "delete_event.html", {"events": events})

def create_event(request):
    if request.method== "POST":
        titre = request.POST.get("titre")
        categorie = request.POST.get("categorie")
        localisation = request.POST.get("localisation")
        date_heure = request.POST.get("date_heure")
        capacite = request.POST.get("capacite")
        description = request.POST.get("description")
=======
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
>>>>>>> 8a8a7e7cb8c338d3e55400d5d029ce7c08a02694
