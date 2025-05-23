def utilisateur_connecte(request):
    return {
        'utilisateur_connecte': 'email' in request.session,
        'email_utilisateur': request.session.get('email', None)
    }