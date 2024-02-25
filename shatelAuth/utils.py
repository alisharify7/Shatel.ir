import uuid

from shatelCore.extensions import RedisServer



def generate_random_text(length: int = 120):
    """
        this function generate random text str(uuid)
    """
    uuids = [str(uuid.uuid4()).replace("-", "") for i in range((length // 32) + 1)]
    return "".join(uuids)[:length]


def set_activation_token_slug_redis(key:str, value:str, expire:int=900):
    """
        Set activation slug for user in redis
        set activation base on Token Slug and email value
        Args:
            key:str: activation slug
            value:str: users email address
            expire:int: expire timr for this entry (in seconds)

        example:
        "ActivateAccountToken:2c10e053b20243f6b4beab7524e1f0c843949b9e172d42568a0fd6430ad714cb875276962a6548ee9c3635c0e06e31116cdb97d400324a0b9bf3bc17"
        value: users email│

    """
    # 900 second is 15 minute
    keyRedis = f"ActivateAccountToken:{key}"

    return RedisServer.set(name=keyRedis, value=value, ex=expire)


def get_activation_token_slug_redis(key: str) -> str:
    """Getting an activation entry from redis db base on `Token Slug`
    return value of entry is users email address
    """
    keyRedis = f"ActivateAccountToken:{key}"
    result = RedisServer.get(name=keyRedis)
    if result:
        return result.decode()
    else:
        return result

def set_activation_email_slug_redis(key:str, value:str, expire:int=900):
    """
        Set activation slug for user in redis
        set activation base on Token Slug and email value
        Args:
            key:str: activation slug
            value:str: users email address
            expire:int: expire timr for this entry (in seconds)

        example:
        "ActivateAccountEmail:alisharifyofficial@gmail.com
        value: 2c10e053b20243f6b4beab7524e1f0c843949b9e172d42568a0fd6430ad714cb875276962a6548ee9c3635c0e06e31116cdb97d400324a0b9bf3bc17"
        value is reset password token
    """
    # 900 second is 15 minute
    keyRedis = f"ActivateAccountEmail:{key}"
    return RedisServer.set(name=keyRedis, value=value, ex=expire)


def get_activation_email_slug_redis(key:str):
    """Getting an activation entry from redis db base on `Users Email address`
    return value of entry is Reset password Token
    """
    keyRedis = f"ActivateAccountEmail:{key}"
    result = RedisServer.get(name=keyRedis)
    if result:
        return result.decode()
    else:
        return result


def delete_activation_token_slug_redis(key:str):
    """Delete activation entry from redis db base on `Token Slug`"""
    keyRedis = f"ActivateAccountToken:{key}"
    return RedisServer.delete(keyRedis)

def delete_activation_email_slug_redis(key:str):
    """
    Delete activation entry from redis db base on `User Email address`
    Call this method when users activate its account successfully
    """
    keyRedis = f"ActivateAccountEmail:{key}"
    return RedisServer.delete(keyRedis)

def get_activation_ttl_slug_redis(key:str):
    """returns an account activation token expire time in minute
    base of `User's Email address`

    Args:
        key: str: user's email address

    Returns:
        ttl: time to live : expire time of activation token in redis db
    """
    keyRedis = f"ActivateAccountEmail:{key}"
    result = RedisServer.ttl(name=keyRedis)
    if result > 0:
        return result // 60
    else:
        return result

def gen_and_set_activation_slug(email: str, length: int = 120):
    """
    Generate amd set unique activation code for each user in redis server
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        input:
            email: str
            length: int

        return:
            `Token <True>` if Code generated successfully and set in redis db
            `False` if tries 200 times and not getting a unique code for user

    this view generate a unique token for each user for activate there account throw url<GET>
        the redis key for each Activate token starts with `ActivateAccountToken:` and then Token Comes
            like : `ActivateAccountToken:uuid.uuid4()`

    Expire time for each activate token is 7200 second or 2 Hour

    """
    counter = 0
    token = generate_random_text(length=length)

    while True:
        if counter == 200:
            return False
        if get_activation_token_slug_redis(token):
            token = generate_random_text(length=length)
            continue
            counter += 1
        else:
            set_activation_token_slug_redis(key=token, value=email)
            set_activation_email_slug_redis(key=email, value=token)
            return token



def set_reset_slug_redis(token:str, email:str, expire:int=7200):
    """
    """
    # 60 second / 60*60 second in minute / 3600 one house in second /  7200 second 2 hour in minute

    tokenRedisPrefix = f"ResetPasswordToken:{token}" # show witch token belong to which email: get users email address from url in reset token
    emailTokenPrefix = f"ResetPasswordEmail:{email}" # show which email belong to which token: uses when a email address is send to server for sending reset password
    RedisServer.set(name=tokenRedisPrefix, value=email, ex=expire)
    RedisServer.set(name=emailTokenPrefix, value=token, ex=expire)


def get_reset_password_number(email:str):
    keyRedis = f"ResetPasswordCounter:{email}"
    result = RedisServer.get(name=keyRedis)
    if not result:
        return 0
    else:
        result = result.decode('utf-8')
        return int(result)

def set_reset_password_number(email:str, value:str):
    keyRedis = f"ResetPasswordCounter:{email}"
    return RedisServer.set(name=keyRedis, value=value, ex=(60*60)*7)

def increase_reset_password_number(email:str):
    keyRedis = f"ResetPasswordCounter:{email}"
    result = RedisServer.get(name=keyRedis)
    if not result:
        result = 1
    else:
        result = result.decode('utf-8')
        result = int(result) + 1

    return RedisServer.set(name=keyRedis, value=result, ex=(60*60)*7)



def get_reset_email_slug_redis(key:str):
    keyRedis = f"ResetPasswordEmail:{key}"
    result = RedisServer.get(name=keyRedis)
    if result:
        return result.decode()
    else:
        return result

def get_reset_token_slug_redis(key:str):
    keyRedis = f"ResetPasswordToken:{key}"
    result = RedisServer.get(name=keyRedis)
    if result:
        return result.decode()
    else:
        return result

def delete_reset_email_slug_redis(key:str):
    keyRedis = f"ResetPasswordEmail:{key}"
    return RedisServer.delete(keyRedis)

def delete_reset_token_slug_redis(key:str):
    keyRedis = f"ResetPasswordToken:{key}"
    return RedisServer.delete(keyRedis)

def gen_and_set_reset_slug(email: str, length: int = 120):
    """
    This function generate and set a unique token for user to resset its account password

    reset Tokens in Redis db :
            Starts with `ResetPasswordToken:` for keeping user reset token
            Starts with `lastRestToken:` for keeping user's last reset Password token

    """

    counter = 0

    while True:
        if counter == 200:
            return False
        token = generate_random_text(length=length)
        if get_reset_token_slug_redis(token):
            counter += 1
            continue
        else:
            set_reset_slug_redis(token=token, email=email, expire=7200)
            increase_reset_password_number(email=email)
            return token
