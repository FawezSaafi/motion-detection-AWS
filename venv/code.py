from PIL import Image
import webbrowser
import pytesseract

import numpy as np
import argparse
import cv2
#construire un argument parser permettant de mettre le nom de l image source a traiter
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help="path to the image")
args = vars(ap.parse_args())

#lire l'image
image = cv2.imread(args["image"])

#definir les limites de la couleur a detecter qui est le rouge
boundaries = [
    ([0, 0, 171], [132, 132, 255])

]
# [0, 0, 132], [125, 125, 255]

root_path = "C:\\Users\\DELL\\Desktop\\projet\\"

# parcours des pixels
for (lower, upper) in boundaries:

    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")

    # trouver les pixels qui sont dans l'interval boundaries et appliquer le masque

    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask=mask)
    cv2.imwrite(root_path + "Resultat.png", output)

    # pour afficher le resultat de cette etape : detecter les mots ecrits en rouge
    #cv2.imshow("images", np.hstack([image, output]))
    #cv2.waitKey(0)
    # END CODE SEIF

#appler le programme a executer
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"

#convertir une image contenant un mot a une chaine de caracteres
data = pytesseract.image_to_string(Image.open('Resultat.png'))

#l 'URL a visiter pour afficher le resultat de la recherche
#%3F represente un formatage ou on va inserer le mot lu a partir de l'image
line = 'http://api.wolframalpha.com/v1/simple?appid=VKY3JH-44A8L5PK3X&i=%3F'

index = line.find('%3F')
output_line = line[:index] + data + line[index:]

webbrowser.open(output_line)