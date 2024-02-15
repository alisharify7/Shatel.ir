import uuid

from shatelCore.extensions import RedisServer


def generate_random_text(length: int = 120):
    """
        this function generate random text str(uuid)

    """
    uuids = [str(uuid.uuid4()).replace("-", "") for i in range((length // 32) + 1)]
    return "".join(uuids)[:length]


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
    redis_prefix_name = "ActivateAccountToken:"
    counter = 0
    token = generate_random_text(length=length)

    while True:
        if counter == 200:
            return False
        if RedisServer.get(f"{redis_prefix_name}{token}"):
            token = generate_random_text(length=length)
            continue
            counter += 1
        else:
            RedisServer.set(name=f"{redis_prefix_name}{token}", value=email,
                            ex=7200)  # 60 second / 60*60 second in minute / 3600 one house in second /  7200 second 2 hour in minute

            return token


def gen_and_set_reset_slug(email: str, length: int = 120):
    """
    This function generate and set a unique token for user to resset its account password

    reset Tokens in Redis db :
            Starts with `ResetPasswordToken:` for keeping user reset token
            Starts with `lastRestToken:` for keeping user's last reset Password token

    """

    redis_prefix_name = "ResetPasswordToken:"
    redis_mail_prefix_name = "lastRestToken:"
    counter = 0

    while True:
        if counter == 200:
            return False
        token = generate_random_text(length=length)
        if RedisServer.get(f"{redis_prefix_name}{token}"):
            counter += 1
            continue
        else:
            # 60 second / 60*60 second in minute / 3600 one house in second /  7200 second 2 hour in minute
            RedisServer.set(name=f"{redis_mail_prefix_name}{email}", value=token,
                            ex=7200)  # set lastest Reset Token of user

            RedisServer.set(name=f"{redis_prefix_name}{token}", value=email,
                            ex=7200)  # set Token in db
            return token
