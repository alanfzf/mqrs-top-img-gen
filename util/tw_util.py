import re
import tweepy

API_BTOKEN = ''
TW_USER_PATTERN = re.compile("^(\w{1,15})$")

def valid_tw_user(user):
    match = bool(TW_USER_PATTERN.match(user))
    return match

def get_profile_pics(users):
    user_pics = {}

    if len(users) < 1:
        return user_pics

    client = tweepy.Client(bearer_token=API_BTOKEN, wait_on_rate_limit=True)
    resp = client.get_users(usernames=users, user_fields=['profile_image_url'])

    data = resp.data
    errors = resp.errors

    # users
    if data is not None:
        for user in data:
            uname = user.username
            url = user.profile_image_url.replace('_normal', '')
            user_pics[uname] = {"img_url": url, "status": "ok"}

    # not found users
    if errors is not None:
        for error in errors:
            user_pics[error["value"]] = {"status": error["detail"]}
    return user_pics
