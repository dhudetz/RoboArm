import numpy as np
import cv2
import glob

def calibrate():
    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((7*9,3), np.float32)
    objp[:,:2] = (np.mgrid[0:9,0:7].T.reshape(-1,2))*20

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    images = glob.glob('calibrate_images/*.jpg')

    for filename in images:
        img = cv2.imread(filename)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        #find chess board corners... ret is a bool for if it was found
        ret, corners = cv2.findChessboardCorners(gray,(7,9),None)
        if ret:
            objpoints.append(objp)

            corners2 = cv2.cornerSubPix(gray,corners,(5,5),(-1,-1),criteria)
            imgpoints.append(corners2)

            #draw and display the corners
            img = cv2.drawChessboardCorners(img,(7,9),corners2,ret)
            cv2.imshow('img',img)
            cv2.waitKey(1)

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints,
                                                    gray.shape[::-1],None,None)
    cv2.destroyAllWindows()
    return ret,mtx,dist