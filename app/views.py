from django.shortcuts import render, redirect
from mongo import db 
from bson.objectid import ObjectId 
from .forms import EventForm
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings
from PIL import Image
from datetime import datetime, timedelta


def get_events(request):
    if db is not None :
        events = list(db.events.find())
        for ev in events:
            ev['id'] = str(ev['_id'])
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
    
def get_events_gratuits(request):
    if db is not None :
        events = list(db.events.find({"statut":"Gratuit"}, {"_id": 0}))
        return render(request, 'events_gratuits.html', {'events': events})
    else:
        return render(request, 'events_gratuits.html', { 'events': []})

def get_events_payants(request):
    if db is not None :
        events = list(db.events.find({"statut":"Payant"}, {"_id": 0}))
        return render(request, 'events_payants.html', {'events': events})
    else:
        return render(request, 'events_payants.html', { 'events': []})
    

# def get_events_aujourdhui(request):
#     if db is not None:
#         events = list(db.events.find({
#             "date_heure": {
#                 "$gte": datetime(datetime.now().year, datetime.now().month, datetime.now().day, 0, 0, 0),
#                 "$lt": datetime(datetime.now().year, datetime.now().month, datetime.now().day, 23, 59, 59, 999999)
#             }
#         }, { "_id": 0 }))
#         return render(request, 'events_aujourdhui.html', {'events': events})
#     else:
#         return render(request, 'events_aujourdhui.html', {'events': []})
    
def get_events_aujourdhui(request):
    if db is not None:
        events = list(db.events.find({
            "date_heure": {
                "$gte": datetime.now(),
                "$lt": datetime(datetime.now().year, datetime.now().month, datetime.now().day, 23, 59, 59, 999999)
            }
        }, {"_id": 0}))
        return render(request, 'events_aujourdhui.html', {'events': events})
    else:
        return render(request, 'events_aujourdhui.html', {'events': []})
    

def get_events_semaine(request):
    if db is not None:
        events = list(db.events.find({
            "date_heure": {
                "$gte": datetime.now(),
                "$lt": datetime.now() + timedelta(days=6-datetime.now().weekday())
            }
        }, {"_id": 0}))
        return render(request, 'events_semaine.html', {'events': events})
    else:
        return render(request, 'events_semaine.html', {'events': []})
    
def get_events_mois(request):
    if db is not None:
        events = list(db.events.find({
            "date_heure": {
                "$gte": datetime.now(),
                "$lt": datetime(datetime.now().year, datetime.now().month+1, 1) if datetime.now().month < 12 
                      else datetime(datetime.now().year+1, 1, 1)
            }
        }, {"_id": 0}))
        return render(request, 'events_mois.html', {'events': events})
    else:
        return render(request, 'events_mois.html', {'events': []})


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
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            titre = form.cleaned_data['titre']
            categorie = form.cleaned_data['categorie']
            localisation = form.cleaned_data['localisation']
            date_heure = form.cleaned_data['date_heure']
            capacite = form.cleaned_data['capacite']
            description = form.cleaned_data['description']
            image = form.cleaned_data['image']


            image = form.cleaned_data['image']
            image_url = f"media/{image.name}"
            with open(image_url, 'wb+') as f:
                for chunk in image.chunks():
                    f.write(chunk)
            try:
                img = Image.open(image)
                img.verify()
            except (IOError, SyntaxError):
                return render(request, 'create_event.html', {
                    'form': form,
                    'error': "Le fichier téléchargé n'est pas une image valide."
                })

            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT))
            image_name = fs.save(image.name, image)
            image_url = fs.url(image_name)  

            
            db.events.insert_one({
                'titre': titre,
                'categorie': categorie,
                'localisation': localisation,
                'date_heure': date_heure,
                'capacite': capacite,
                'description': description,
                'image_url': image_url,
            })
            
            return redirect('events')
    else:
        form = EventForm()
    
    return render(request, 'create_event.html', {'form': form})
            
