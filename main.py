import cv2
#import numpy as np
import pandas as pd
import argparse

'''Argument parser to take smth from terminal'''
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help='Image path')
args = vars(ap.parse_args())
img_path = args['image']

'''Reading image with CV2'''
image = cv2.imread(img_path)


'''reading csv'''
index = ['color', 'color_name', 'HEX', 'R', 'G', 'B']  # пишем заголовки к Таблице
csv = pd.read_csv('color.csv', names=index, header=None)  # читаем csv как таблицу
print(csv)

clicked = False
hex = r = g = b = xpos = ypos = 0

def getColorDistance(r, g, b):
    min = 10000
    for i in range(len(csv)):
        d = abs(r - int(csv.loc[i, 'R'])) + abs(g - int(csv.loc[i, 'G'])) + abs(b - int(csv.loc[i, 'B']))
        if d <= min:
            min = d
        cname = csv.loc[i, 'color_name']
    return cname

def draw_function(event, x, y, flag, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, xpos, ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b, g, r = image[x, y]
        b = int(b)
        r = int(r)
        g = int(g)

cv2.namedWindow('Imag.')
cv2.setMouseCallback('Imag.', draw_function)


while True:
    cv2.imshow('Imag.', image)
    if clicked:
        cv2.rectangle(image, (20, 20), (700 , 60), (b, g, r), -1)
        text = getColorDistance(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b) + ' hex=' + str(hex)
        cv2.putText(image, text, (50, 50), 1, 0.8, (255, 255, 255), 1, cv2.LINE_AA)
        if(r + g + b) > 600:
            cv2.putText(image, text, (50, 50), 2, 1, (0, 0, 0), 2, cv2.LINE_AA)
        clicked = False
    if cv2.waitKey(20) and 0xFF == 27:
        break

cv2.destroyAllWindows()
