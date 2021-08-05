def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'google-oauth2':
        return

    api_url = 'https://docs.googleapis.com/v1/documents/'

