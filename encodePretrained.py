
import cv2
from imwatermark import WatermarkEncoder
bgr = cv2.imread('test.avi')
wm = 'test'
encoder = WatermarkEncoder()
encoder.set_watermark('bytes', wm.encode('utf-8'))
bgr_encoded = encoder.encode(bgr, 'rivaGan')
cv2.imwrite('test.avi', bgr_encoded)