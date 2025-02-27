from django.conf import settings, global_settings


"""
We want this plugin to work without any configurations
So, the value of the BUILD_DIR must be something
"""
DEFAULT = {
    'WS_CLIENT': '@vite/client',
    'DEV_MODE': getattr(settings, 'DEBUG', global_settings.DEBUG),
    'BUILD_DIR': getattr(settings, 'STATIC_ROOT', global_settings.STATIC_ROOT) or getattr(settings, 'BASE_DIR') / 'static',
    'BUILD_URL_PREFIX': getattr(settings, 'STATIC_URL', global_settings.STATIC_URL), # Production asset urls would be prefixed with this
    'SERVER': {
        'HTTPS': False,
        'HOST': '127.0.0.1',
        'PORT': 5173
    },
    'JS_ATTRS': {
        'type': 'module',
    },
    'CSS_ATTRS': {
        'rel' : 'stylesheet',
        'type': 'text/css'
    },
    'STATIC_LOOKUP': True
}


def get_config() -> dict:
    config = getattr(settings, 'DJANGO_VITE_PLUGIN', None)
    return _deep_copy(config, DEFAULT)


def _deep_copy(config, default):
    if type(config) != type(default):
        return default

    for key in default:
        if key not in config:
            config[key] = default[key]
        elif type(default[key]) == dict:
            config[key] = _deep_copy(config[key], default[key])

    return config
