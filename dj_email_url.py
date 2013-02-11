# -*- coding: utf-8 -*-

import os

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse


# Register email schemes in URLs.
urlparse.uses_netloc.append('smtp')
urlparse.uses_netloc.append('console')
urlparse.uses_netloc.append('file')
urlparse.uses_netloc.append('memory')
urlparse.uses_netloc.append('dummy')


DEFAULT_ENV = 'EMAIL_URL'


SCHEMES = {
    'smtp': 'django.core.mail.backends.smtp.EmailBackend',
    'smtps': 'django.core.mail.backends.smtp.EmailBackend',
    'console': 'django.core.mail.backends.console.EmailBackend',
    'file': 'django.core.mail.backends.filebased.EmailBackend',
    'memory': 'django.core.mail.backends.locmem.EmailBackend',
    'dummy': 'django.core.mail.backends.dummy.EmailBackend'
}


def config(env=DEFAULT_ENV, default=None):
    """Returns a dictionary with EMAIL_* settings from EMAIL_URL."""

    conf = {}

    s = os.environ.get(env, default)

    if s:
        conf = parse(s)

    return conf


def parse(url):
    """Parses an email URL."""

    conf = {}

    url = urlparse.urlparse(url)

    # Remove query strings
    path = url.path[1:]
    path = path.split('?', 2)[0]

    # Update with environment configuration
    conf.update({
        'EMAIL_FILE_PATH': path,
        'EMAIL_HOST_USER': url.username,
        'EMAIL_HOST_PASSWORD': url.password,
        'EMAIL_HOST': url.hostname,
        'EMAIL_PORT': url.port,
    })

    if url.scheme in SCHEMES:
        conf['EMAIL_BACKEND'] = SCHEMES[url.scheme]

    if url.scheme == 'smtps':
        conf['EMAIL_USE_TLS'] = True
    else:
        conf['EMAIL_USE_TLS'] = False

    return conf