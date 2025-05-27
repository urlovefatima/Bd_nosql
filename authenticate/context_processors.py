from mongo import db

def utilisateur_connecte(request):
    utilisateur = None
    photo_profil = None

    if 'email' in request.session:
        try:
            utilisateur = db.users.find_one({"email": request.session['email']})
            photo_profil = utilisateur['photo_profil'] if utilisateur['photo_profil'] else None
        except db.DoesNotExist:
            pass

    return {
        'utilisateur_connecte': utilisateur is not None,
        'email_utilisateur': request.session.get('email'),
        'photo_profil': photo_profil,
    }
