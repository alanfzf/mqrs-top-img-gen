import re

INVALID_CHARS_FILE = '[<>:"\\\/|?*]' 
TW_USER_PATTERN = r"^(@)?(\w{1,15})$"
TW_PROFILE_PIC_PATTERN = r'^https://pbs.twimg.com/profile_images/'

def remove_invalid_chars(string):
    return re.sub(INVALID_CHARS_FILE, '', string)

def get_font_color(val):
    if not is_number(val):
        return "#FFFFFF"
    if val <= 3.0:
        return "#FB3232"
    elif val > 3.0 and val <= 5.0:
        return "#FFFD58"
    else: 
        return "#58FF68"

def get_text_format(val):
    if is_number(val):
        return f'{val:0.1f}'
    else:
        return ''

def is_number(val):
    return isinstance(val, (int, float))

def validate_users(user_list):
    valid = []
    invalid = []

    for user in user_list:
        result = re.match(TW_USER_PATTERN, user)
        valid.append(result.group(2)) if result else invalid.append(user)

    if len(invalid) > 0:
        invalid = ', '.join(invalid)
        raise Exception(f"Invalid twitter usernames: {invalid}")

    return valid

def valid_url(url):
    return re.search(TW_PROFILE_PIC_PATTERN, url)
