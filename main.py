from util import excel_util as excel
from util import tw_util as tw
from util import img_util as img


def get_users(data):
    users = excel.get_values_from_col(data, 1)
    bad_tw_users = list(filter(lambda v: not tw.valid_tw_user(v), users))
    user_copy = [user for user in users if user not in bad_tw_users]
    no_avatar = list(filter(lambda v: not img.user_has_avatar(v), user_copy))
    return no_avatar

# extract the data
data = excel.extract_data()

# generate the avatars
users = get_users(data)
avatars = tw.get_profile_pics(users)
img.generate_avatars(avatars)

# create all images
values = excel.get_formatted_data(data)
img.gen_images(values)
