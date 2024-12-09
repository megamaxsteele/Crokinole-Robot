import sys
import cv2 as cv
import numpy as np
import picamera2
import keyboard

imageCenter = (1286,1470)

def main():
    
    #initial pciture to make sure camera is working correctly
    cam = picamera2.Picamera2()
    config = cam.create_still_configuration({'format':'RGB888'})
    cam.configure(config)


    cam.start()
    src = cam.capture_array()
    if src is None:
        print ('Error opening image!')
        print ('Usage: hough_circle.py [image_name -- default ' + default_file + '] \n')
        return -1
    

    while(True):
        ## Crop Image - commented out for other testing
        #imageHieght, ImageWidth = src.shape[:2]
        #src = src[ 700:imageHieght-1100,]
        if keyboard.is_pressed('0'):
            break

        if keyboard.is_pressed('enter'):
            src = cam.capture_array()
            ## [convert_to_gray]
            # Convert it to gray
            gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
            ## [convert_to_gray]

        
            ## [reduce_noise]
            # Reduce the noise to avoid false circle detection
            gray = cv.medianBlur(gray, 5)
            ## [reduce_noise]

            ## determines how many game pieces are on the board. Since game pieces are cicles form the top down view this works. 
            ##needs to be adjusted based on camera height
            rows = gray.shape[0]
            circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1.0, rows / 32,
                                    param1=90, param2=30,
                                    minRadius=30, maxRadius=135)
        
            


            ## eliminate the center circle
            imageHieght, ImageWidth = src.shape[:2]
            
            ret, gray = cv.threshold(src,200,255, cv.THRESH_BINARY)  
            
            

            ## [draw] 
            if circles is not None:
                circles = circles[0]
                circles = np.uint16(np.around(circles))



                nearestCoord = 0
                nearestDist = 4000

                for i in circles:
                    center = (i[0], i[1])

                    dist = np.linalg.norm(np.asarray(center)-np.asanyarray(imageCenter))

                    if(dist > 1):
                        if(dist < nearestDist):
                            nearestCoord = i
                            nearestDist = dist
                            print(i)
                            print(gray[tuple((nearestCoord[1],nearestCoord[0]))])
                        # circle center
                        cv.circle(src, center, 1, (0, 100, 100), 3)
                        # circle outline
                        radius = i[2]
                        cv.circle(src, center, radius, (255, 0, 255), 3)
                      

            ## [draw]

            ## [display]
            cv.imwrite("circle detection.jpg", src)
            cv.imwrite("gray.jpg", gray)
            #cv.imshow("detected circles", src)
        

    #cam.wait()
    cam.stop()

    return 0


if __name__ == "__main__":
    main()
