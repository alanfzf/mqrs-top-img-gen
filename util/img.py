from PIL import Image, ImageFont, ImageDraw
from .dirs import get_font_file , get_output_file
from .format import get_font_color, get_text_format

RADIUS = 130
CANVAS = (1280, 720)
FONT = ImageFont.truetype(get_font_file(), 25)
FONT_2 = ImageFont.truetype(get_font_file(), 16)


class ScoreGenerator():

    def __init__(self, user_scores, user_images):
        self.scores = user_scores
        self.images = user_images

    def get_avatar(self, user):
        image = self.images.get(user, None)
        return Image.open(image).resize((RADIUS, RADIUS), Image.Resampling.NEAREST)

    def generate_images(self):
        for title, arrays in self.scores.items():
            count = 1
            while len(arrays) != 0:
                img = self.gen_score(arrays.pop(0))
                img.save(get_output_file(title, count), 'PNG')
                count += 1


    def generate_names(self):
        users = list(self.images.keys())
        chunk_size = 30
        chunks = [users[i:i+chunk_size] for i in range(0, len(users), chunk_size)]
        count = 1

        for chunk in chunks:
            img = self.gen_names(chunk)
            img.save(get_output_file('NOMBRES', count), 'PNG')
            count += 1

    def gen_score(self, uscores):
        circle = Image.new("L",(RADIUS, RADIUS),0)
        ImageDraw.Draw(circle).ellipse((0,0,RADIUS,RADIUS), fill=250)

        img = Image.new(mode = "RGBA", size = CANVAS, color=(0,0,0,0))
        draw = ImageDraw.Draw(img)

        sx,sy = 50,60
        incx, incy = RADIUS+20, RADIUS+20

        try:
            # start the iteration
            for i in range(0,4):
                sx = 50
                for j in range(0,8):
                    if not(i == 3 and (j == 0 or j == 7)):
                        if len(uscores) < 1:
                            raise StopIteration

                        usr = uscores.pop(0)
                        num = usr.get('score', None)
                        uname = usr.get('user', None)
                        logo = self.get_avatar(uname)
                        img.paste(logo, (sx,sy), circle)
                        draw.text((sx,sy), get_text_format(num), 
                                  fill=get_font_color(num), 
                                  font=FONT, stroke_width=2, 
                                  stroke_fill='black')
                    sx = incx+sx
                sy = incy+sy

        except StopIteration:
            pass

        return img


    def gen_names(self, users):
        circle = Image.new("L", (RADIUS, RADIUS), 0)
        ImageDraw.Draw(circle).ellipse((0, 0, RADIUS, RADIUS), fill=250)
        img = Image.new(mode="RGBA", size=CANVAS, color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        sx, sy = 50, 60
        incx, incy = RADIUS + 20, RADIUS + 20

        try:
            # Start the iteration
            for i in range(0, 4):
                sx = 50
                for j in range(0, 8):
                    if not (i == 3 and (j == 0 or j == 7)):
                        if len(users) < 1:
                            raise StopIteration

                        name = users.pop(0)
                        logo = self.get_avatar(name)
                        img.paste(logo, (sx, sy), circle)

                        text = name = f'{name[:12]}.' if len(name) > 12 else name
                        text = text.lower()
                            
                        text_width, text_height = draw.textsize(text, font=FONT_2)
                        text_x = sx + (RADIUS - text_width) // 2
                        text_y = (sy + (RADIUS - text_height) // 2)+60

                        # Draw the text centered inside the logo
                        draw.text((text_x, text_y), text,
                                  fill='#FFFFFF',
                                  font=FONT_2, stroke_width=1,
                                  stroke_fill='black')

                    sx = incx + sx
                sy = incy + sy

        except StopIteration:
            pass

        return img
