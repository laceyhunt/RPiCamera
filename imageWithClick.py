# captures video from webcam, continuously displays it,
#   and saves a snapshot as an image when 'q' is pressed
import cv2

cap = cv2.VideoCapture(0)       # create video capture using default camera (USB camera)

while(True):                    # start live frame loop
    ret, frame = cap.read()     # frame = current video feed frame
                                #   ret is bool value to determine success
    # rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA) # converts BGR to BGRA

    cv2.imshow('frame',frame)         # display current frame
                                #   also pass 'rgb' if conversion occurs ^
    if cv2.waitKey(1) & 0xFF == ord('q'):   # wait for key press every 1ms
                                            #   bitmask for returned ASCII value of pressed key
                                            #   and verify if 'q' was pressed
        out = cv2.imwrite('capture.jpg', frame) # saves frame as image
        break                   # exit loop and end

cap.release()                   # get rid of object to free up camera for other apps
cv2.destroyAllWindows()         # close OpenCV windows