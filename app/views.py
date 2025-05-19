from django.shortcuts import get_object_or_404, render, redirect
from bson import ObjectId
from mongo import db  

def get_events(request):
    if db is not None :
        events = list(db.events.find({}, {"_id": 0}))
        return render(request, 'events.html', {'events': events})
    else:
        return render(request, 'events.html', {'events': []})
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
