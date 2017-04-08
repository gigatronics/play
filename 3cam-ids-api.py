import cv2
import ids
import numpy as py
import matplotlib.pyplot as plt

# help(ids) and print(ids.camera_list()) to find out which ones are connected
print(ids.camera_list())

cam = ids.Camera(1)
cam.color_mode = ids.ids_core.COLOR_RGB8
cam.exposure = 5
cam.auto_exposure = True
cam.continuous_capture = True

cam1 = ids.Camera(3)
cam1.color_mode = ids.ids_core.COLOR_RGB8
cam1.exposure = 5
cam1.auto_exposure = True
cam1.continuous_capture = True

cam2 = ids.Camera(2)
cam2.color_mode = ids.ids_core.COLOR_RGB8
cam2.exposure = 5
cam2.auto_exposure = True
cam2.continuous_capture = True


while(1):
    img0, meta = cam.next()
    img1, meta = cam1.next()
    img2, meta = cam2.next()

    #cv2.imshow('cam0', cv2.pyrDown(img0))
    #cv2.imshow('cam1', cv2.pyrDown(img1))

    plt.subplot(221), plt.imshow(img0),plt.title('img0')
    plt.subplot(222), plt.imshow(img1),plt.title('img1')
    plt.subplot(223), plt.imshow(img2),plt.title('img2')
    plt.show()


#
    if cv2.waitKey(1) & 0xFF:
        break


bgr_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
#cv2.imwrite('test.jpg', bgr_img)

cv2.destroyAllWindows
