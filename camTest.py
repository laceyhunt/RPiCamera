from __future__ import print_function

import requests
import time 
import picamera
import state

import hashlib
import glob
import datetime
import os

from PIL import ImageFont, ImageDraw, Image
import traceback
import util
import datetime as dt
import MySQLdb as mdb

import config

# def SkyWeatherKeyGeneration(userKey):

#     catkey = "AZWqNqDMhvK8Lhbb2jtk1bucj0s2lqZ6" +userKey

#     md5result = hashlib.md5(catkey.encode())
#     #print ("hashkey =", md5result.hexdigest())
#     return md5result.hexdigest()

def takeSkyPicture():

    if (config.SWDEBUG):
        print ("--------------------")
        print ("SkyCam Picture Taken")
        print ("--------------------")
    camera = picamera.PiCamera()

    camera.exposure_mode = "auto"
    try:
        camera.rotation = config.Camera_Rotation
        
        camera.resolution = (1920, 1080)
        # Camera warm-up time
        time.sleep(2)

        camera.capture('images/testimage.jpg')
    except:
        if (config.SWDEBUG):
            print(traceback.format_exc()) 
            print ("--------------------")
            print ("SkyCam Picture Failed")
            print ("--------------------")
    finally:
        try:
            camera.close()
        except:
            if (config.SWDEBUG):
                print ("--------------------")
                print ("SkyCam Close Failed ")
                print ("--------------------")