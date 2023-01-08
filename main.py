import requests
from html2image import Html2Image
from PIL import Image

hti = Html2Image()

link_presentation = input('Enter URL of the presentation with ".../svg/" at the end\n')
width = int(input('Enter a width\n'))
height = int(input('Enter a height\n'))
hti.output_path = input('Enter output path\n')

images = list()
slide_number = 1
status = True
while status:
    slide_link = link_presentation + str(slide_number)
    slide = requests.get(slide_link)

    print(slide.status_code)
    if slide.status_code == 200:
        hti.screenshot(html_str=slide.text, save_as=f'slide_{slide_number}.jpeg', size=(width, height))
        images.append(Image.open(f'slide_{slide_number}.jpeg'))
        slide_number += 1
    else:
        status = False
        try:
            img = Image.open("slide_1.jpeg")
            img = img.crop((0, 0, width, height * (slide_number-1)))

            for i in images:
                img.paste(i, (0, height * images.index(i)))

            img.save("full_presentation.png")

        except IOError as e:
            print(e)
            pass
