def check_token(token: str):
    import hashlib, os
    h = hashlib.sha256()
    h.update(token.encode('utf-8'))
    sha256 = h.hexdigest()
    return sha256 == os.environ['NOOBGAM_PERSONAL_PASSWORD_SHA256']
