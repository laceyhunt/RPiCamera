import cv2
import datetime
#path = r'/home/pi/RPiCamera/capture.jpg'
image = cv2.imread("capture.jpg")
window_name = 'Image'
text = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
print(text)
font = cv2.FONT_HERSHEY_COMPLEX
org=(00,185)
fontScale=1
color = (255,0,0)     # function to decide between black and white?
thickness=2
image = cv2.putText(image,text,org,font,fontScale,color,thickness,cv2.LINE_AA,False)
#image = cv2.putText(image, text, org, font, fontScale,color, thickness, cv2.LINE_AA, True) 
cv2.imshow(window_name,image)
cv2.imwrite(text+".jpg",image)
# Wait for the user to press a key
cv2.waitKey(0)
 
# Close all windows
cv2.destroyAllWindows()