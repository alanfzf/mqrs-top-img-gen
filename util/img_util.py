import os
import requests
from PIL import Image, ImageFont, ImageDraw

#  w,h =draw.textsize(msg, font=fnt)
#  draw.text(
# ((radius-w)/2,120), msg, 
#            font=fnt, fill="green", 
#            stroke_width=3, 
#            stroke_fill='black')
#font 
FONT = ImageFont.truetype("./files/font/moon_get-Heavy.ttf", 25)
# base canvas dimensions
RADIUS = 130
CANVAS = (1280, 720)

def get_font_color(val):
    if val <= 3.0:
        return "#fb3232"
    elif val > 3.0 and val <=5.0:
        return "#fffd58"
    else: 
        return "#58ff68"

def get_text_format(val):
    text = '' if val <= 0 else f'{val:0.1f}'
    return text



def generate_avatars(profile_urls):
    for user, data in profile_urls.items():
        url = data.get('img_url', None)
        img = Image.new("RGB", (400,400), (255,255,255)) if url is None else Image.open(requests.get(url, stream=True).raw)
        img.save(f'./files/img_cache/{user}.jpg', 'JPEG')

def user_has_avatar(user):
    path = f'./files/img_cache/{user}.jpg'
    return os.path.exists(path)


def user_get_avatar(user):
    if not user_has_avatar(user):
        return Image.new('RGB', (RADIUS,RADIUS), (255, 255,255))
    else:
        return Image.open(f"./files/img_cache/{user}.jpg").resize((RADIUS, RADIUS), Image.Resampling.NEAREST)


def gen_score(uscores):
    circle = Image.new("L",(RADIUS, RADIUS),0)
    ImageDraw.Draw(circle).ellipse((0,0,RADIUS,RADIUS), fill=250)

    img = Image.new( mode = "RGBA", size = CANVAS, color=(0,0,0,0))
    draw = ImageDraw.Draw(img)

    sx,sy = 50,60
    incx, incy = RADIUS+20, RADIUS+20

    for i in range(0,4):
        sx = 50
        for j in range(0,8):
            if not(i == 3 and (j == 0 or j == 7)):
                usr = uscores.pop(0)
                num = usr.score or 0.0
                logo = user_get_avatar(usr.name)
                img.paste(logo, (sx,sy), circle)
                draw.text((sx,sy), get_text_format(num),
                          fill=get_font_color(num), font=FONT, 
                          stroke_width=2, stroke_fill='black'
                )
            sx = incx+sx
        sy = incy+sy

    return img
    
def gen_images(values):
    # create the circle
    for title, arrays in values.items():
        count = 1
        while len(arrays) != 0:
            array = arrays.pop(0)
            img = gen_score(array)
            img.save(f'./files/out/{title}_{count}.png', 'PNG')
            count += 1

    # create the canvas
