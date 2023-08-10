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

        # now add timestamp to jpeg
        pil_im = Image.open('static/skycamera.jpg')
      
        draw = ImageDraw.Draw(pil_im)
        
        # Choose a font
        font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 25)

        # set up units
        #wind
        val = util.returnWindSpeed(state.WindSpeed)
        WindStval = "{0:0.1f}".format(val) + util.returnWindSpeedUnit()
        val = util.returnWindSpeed(state.WindGust)
        WindGtval = "{0:0.1f}".format(val) + util.returnWindSpeedUnit()
        val = util.returnTemperatureCF(state.OutdoorTemperature)
        OTtval = "{0:0.1f} ".format(val) + util.returnTemperatureCFUnit()

        myText = "SkyWeather2 V%s %s Wind Speed: %s Wind Gust: %s Temp: %s " % (config.SWVERSION,dt.datetime.now().strftime('%d-%b-%Y %H:%M:%S'),WindStval, WindGtval, OTtval)
        print("mySkyCameraText=", myText)

        # Draw the text
        color = 'rgb(255,255,255)'
        #draw.text((0, 0), myText,fill = color, font=font)

        # get text size
        text_size = font.getsize(myText)

        # set button size + 10px margins
        button_size = (text_size[0]+20, text_size[1]+10)

        # create image with correct size and black background
        button_img = Image.new('RGBA', button_size, "black")
     
        # put text on button with 10px margins
        button_draw = ImageDraw.Draw(button_img)
        button_draw.text((10, 5), myText, fill = color, font=font)

        # put button on source image in position (0, 0)

        pil_im.paste(button_img, (0, 0))
        bg_w, bg_h = pil_im.size 
        # WeatherSTEM logo in lower left
        size = 64
        WSLimg = Image.open("static/WeatherSTEMLogoSkyBackground.png")
        WSLimg.thumbnail((size,size),Image.ANTIALIAS)
        pil_im.paste(WSLimg, (0, bg_h-size))

        # SkyWeather log in lower right
        SWLimg = Image.open("static/SkyWeatherLogoSymbol.png")
        SWLimg.thumbnail((size,size),Image.ANTIALIAS)
        pil_im.paste(SWLimg, (bg_w-size, bg_h-size))

        # Save the image
        pil_im.save('dash_app/assets/skycamera.jpg', format= 'JPEG')
        pil_im.save('static/skycamera.jpg', format= 'JPEG')
        pil_im.save('static/skycameraprocessed.jpg', format= 'JPEG')

        cameraID = "SkyCamPi"
        currentpicturefilename = "static/CurrentPicture/"+cameraID+".jpg"
        currentpicturedashfilename = "dash_app/assets/"+cameraID+"_1.jpg"
        for name in glob.glob("dash_app/assets/"+cameraID+"_*.jpg"):
            os.remove(name)
        
        # put together the file name
        fileDate = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        fileDay = datetime.datetime.now().strftime("%Y-%m-%d")

        singlefilename =cameraID+"_1_"+fileDate+".jpg"
        dirpathname="static/SkyCam/" + cameraID+ "/"+fileDay

        os.makedirs(dirpathname, exist_ok=True)
        os.makedirs("static/CurrentPicture", exist_ok=True)
        filename = dirpathname+"/"+singlefilename


        pil_im.save(filename, format= 'JPEG')
        pil_im.save(currentpicturefilename, format= 'JPEG')
        pil_im.save(currentpicturedashfilename, format= 'JPEG')

        FileSize =os.path.getsize(currentpicturefilename)

        if (config.enable_MySQL_Logging == True):
            # open mysql database
            # write log
            # commit
            # close
            try:
    
                con = mdb.connect(
                    "localhost",
                    "root",
                    config.MySQL_Password,
                    "WeatherSenseWireless" 
                )

                cur = con.cursor()
    
                fields = "cameraID, picturename, picturesize, messageID, resends,resolution"

                values = "\'%s\', \'%s\', %d, %d, %d, %d" % (cameraID, singlefilename, FileSize, 1, 0, 0)  
                query = "INSERT INTO SkyCamPictures (%s) VALUES(%s )" % (fields, values)
                print("query=", query)
                cur.execute(query)
                con.commit()
            except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0], e.args[1]))
                con.rollback()
                # sys.exit(1)
    
            finally:
                cur.close()
                con.close()
    
                del cur
                del con


        time.sleep(2)

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


    if (config.USEWEATHERSTEM == True):
        sendSkyWeather()


import base64


def sendSkyWeather():

    # defining the api-endpoint  
    API_ENDPOINT = "https://skyweather.weatherstem.com/"
  

    with open("static/skycamera.jpg", "rb") as image_file:
       encoded_string = base64.b64encode(image_file.read())
       encoded_string = encoded_string.decode('utf-8')

    if (config.SWDEBUG):
        print ("--------------------")
        print ("SkyCam Package Sending")
        print ("--------------------")
        print ("API Key:",state.WeatherSTEMHash)
    if(state.barometricTrend == True):
        bptrendvalue = "Rising"
    else:
        bptrendvalue = "Falling"
   
    currentTime = time.time()

    print("------->Sea Level", state.BarometricPressureSeaLevel*10.0)
    data = {
                "SkyWeatherVersion": config.SWVERSION,
                "SkyWeatherHardware": config.STATIONHARDWARE,
                "api_key": state.WeatherSTEMHash,

	"device":{
                "key":  config.STATIONKEY,
                "MAC":config.STATIONMAC,
	},
	"utc":currentTime,
	"cameras":[
		{
			"name":"Sky Camera",
                        "image": encoded_string
		}
		
	]
    }
    # import json
  
    # sending post request and saving response as response object 
    r = requests.post(url = API_ENDPOINT, json = data) 
    #print (data )
    # extracting response text  
    pastebin_url = r.text 
    if (config.SWDEBUG):
        print("The pastebin URL is (r.text):%s"%pastebin_url) 



        