import cv2
import numpy as np
import glob

# drone'un fotoğraf çekeceği alanı belirleme
img_dir = "path/to/image/directory"
data_path = os.path.join(img_dir,'*.jpg')
files = glob.glob(data_path)

# kamera kalibrasyonu yapma
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objp = np.zeros((9*6,3), np.float32)
objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)

objpoints = []
imgpoints = []

for file in files:
    img = cv2.imread(file)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, (9,6),None)
    
    if ret == True:
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners2)
        
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)

# fotoğrafları birleştirerek harita oluşturma
stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()
(status, stitched) = stitcher.stitch(images, showMatches=True)

if status == 0:
    cv2.imshow("Stitched", stitched)
    cv2.waitKey(0)
    
else:
    print("[INFO] image stitching failed ({})".format(status))
