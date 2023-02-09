from config.settings import PROJECT_HOST, PROJECT_PORT, PROJECT_SCHEMA


def get_abs_url(path):
    main_url = PROJECT_SCHEMA + "://" + PROJECT_HOST + ":" + PROJECT_PORT
    if not path.startswith('/'):
        path = '/' + path
    if not path.endswith('/'):
        path += '/'
    return main_url + path