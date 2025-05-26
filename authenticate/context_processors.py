from mongo import db
def utilisateur_connecte(request):
    return {
        'utilisateur_connecte': 'email' in request.session,
        'email_utilisateur': request.session.get('email', None),
        # 'photo_profil': db.users.find_one({'email':request.session.get('email', None)})['photo_profil']
    }