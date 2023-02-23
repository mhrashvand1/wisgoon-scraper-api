from django.conf import settings

def get_abs_url(path):
    main_url = settings.PROJECT_SCHEMA + "://" + settings.PROJECT_HOST + ":" + settings.PROJECT_PORT
    if not path.startswith('/'):
        path = '/' + path
    if not path.endswith('/'):
        path += '/'
    return main_url + path