#import all necessary libraries
#due to time constraints, face_recognition was installed

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import requests
import json

import face_recognition
import cv2

def main():

    #get user token

    token = str(input('ENTER YOUR TOKEN: '))     #your token goes here

    url = 'https://hackattic.com/challenges/basic_face_detection/problem?access_token='+token



    #get the image URL from the JSON and download the image

    response = requests.get(url)

    jayson = json.loads(response.text)

    image_url = jayson['image_url']

    img_response = requests.get(image_url)

    if img_response.status_code == 200:

        with open("faces.jpg", 'wb') as f:
            f.write(img_response.content)
            f.close()

    # Load the image in as a numpy array
    img = cv2.imread('faces.jpg',0)


    #can sequentially run through all 64 images and run face recognition on each sub-image

    sub_img_width = 100    #hard-coded for this particular problem set

    sub_img_height = sub_img_width  #in this case the images are square

    img_rows = int(img.shape[1]/sub_img_width)
    img_cols = int(img.shape[0]/sub_img_height)

    position_lst = []    #instantiate empty list for positions

    for r in range(img_rows):

        for c in range(img_cols):
            itr_btm = (r+1)*100    #get bottom-most edge of sub-image, then get top-most edge

            itr_right = (c+1)*100    #get right-most edge of sub-image, then get left-most edge

            itr_img = img[itr_btm-100 : itr_btm , itr_right-100 : itr_right]    #get image for current iteration

            itr_face_loc = face_recognition.face_locations(itr_img)    #run facial recognition

            if len(itr_face_loc) == 0:    #skip to next iteration if no faces located
                pass

            else:

                position_lst.append([r,c])




    #post results to API and get response

    pos_json = {'face_tiles':position_lst}
    
    print(pos_json+'\n')

    solve_url = 'https://hackattic.com/challenges/basic_face_detection/solve?access_token='+token

    headers = {'Content-Type': 'application/json', 'Accept':'application/json'}    #post the data as a JSON to the API

    r = requests.post(solve_url, headers=headers, json=pos_json)

    print(r.text)


# execute only if run as the entry point into the program

if __name__ == '__main__':    
    main()