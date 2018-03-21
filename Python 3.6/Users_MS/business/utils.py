import logging
import hashlib


def hash_password(password_raw):
    logging.debug("{utils} BEGIN function hash_password()")
    if password_raw is '':
        return ''
    logging.debug("{utils} BEGIN function hash_password()")
    m = hashlib.md5()
    m.update(password_raw.encode('utf-8'))
    return m.hexdigest()
