from shatelCore.extensions import RedisServer
from shatelCore.utils import generate_random_string

def generate_newsletter_confirm_token():
    while True:
        token = generate_random_string(64//32)
        if not redis_exists_newsletter_token(token):
            return token


def redis_set_newsletter_token(newsletter_token, email):
    prefix = f"NewsLetterToken:{newsletter_token}"
    RedisServer.set(name=prefix, value=email, ex=7200)
    prefix = f"NewsLetterEmail:{email}"
    RedisServer.set(name=prefix, value=newsletter_token, ex=7200)


def redis_get_newsletter_token(newsletter_token):
    prefix = f"NewsLetterToken:{newsletter_token}"
    result = RedisServer.get(name=prefix)
    if result:
        return result.decode()
    else:
        return result
def redis_exists_newsletter_mail(email):
    prefix = f"NewsLetterEmail:{email}"
    return RedisServer.exists(prefix)

def redis_exists_newsletter_token(email):
    prefix = f"NewsLetterEToken:{email}"
    return RedisServer.exists(prefix)

def redis_ttl_newsletter_mail(email):
    prefix = f"NewsLetterEmail:{email}"
    result = RedisServer.ttl(name=prefix)
    if result > 0:
        return result // 60
    else:
        return result

def redis_delete_newsletter_token_email(newsletter_token, email):
    prefix = f"NewsLetterToken:{newsletter_token}"
    RedisServer.delete(prefix)
    prefix = f"NewsLetterEmail:{email}"
    RedisServer.delete(prefix)