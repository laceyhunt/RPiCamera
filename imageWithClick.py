# captures video from webcam, continuously displays it,
#   and saves a snapshot as an image when 'q' is pressed
import cv2
import datetime
import os

cap = cv2.VideoCapture(0)       # create video capture using default camera (USB camera)
window_name = 'Image'

while(True):                    # start live frame loop
    ret, window_name = cap.read()     # frame = current video feed frame
                                #   ret is bool value to determine success
    # rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA) # converts BGR to BGRA

    cv2.imshow('frame',window_name)         # display current frame
                                #   also pass 'rgb' if conversion occurs ^
    if cv2.waitKey(1) & 0xFF == ord('q'):   # wait for key press every 1ms
                                            #   bitmask for returned ASCII value of pressed key
                                            #   and verify if 'q' was pressed
        out = cv2.imwrite('capture.jpg', window_name) # saves frame as image
        break                   # exit loop and end

cap.release()                   # get rid of object to free up camera for other apps

image = cv2.imread("capture.jpg")
text = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
print(text)
font = cv2.FONT_HERSHEY_COMPLEX
org=(00,1000)
fontScale=1
color = (0,0,0)     # function to decide between black and white?
thickness=1.5
directory = "/home/pi/RPiCamera/images"
image = cv2.putText(image,text,org,font,fontScale,color,thickness,cv2.LINE_AA,False)
cv2.imshow(window_name,image)
os.chdir(directory)
print("Before saving image:")  
print(os.listdir(directory)) 
cv2.imwrite(text+".jpg",image)
print("After saving image:")  
print(os.listdir(directory)) 
# Wait for the user to press a key
cv2.waitKey(0)
 
# Close all windows
cv2.destroyAllWindows()