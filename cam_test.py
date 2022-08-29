# import the opencv library
import cv2
  
vid = cv2.VideoCapture(-1)
  
while(True):
      
    # Capture the video frame
    # by frame
    ret, frame = vid.read()
  
    # Display the resulting frame
    try:
        cv2.imshow('frame', frame)
    except Exception as e:
        print("cam not working")
        break
      
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()