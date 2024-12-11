from jetson_jpeg import JpegEncoder

from pathlib import Path
import cv2

script_path = Path(__file__).resolve().parent

img = cv2.imread(script_path / 'image.jpg')
height, width, _ = img.shape
yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV_I420).flatten()

encoder = JpegEncoder()
quality = 80
jpeg = encoder.encode(yuv, width, height, quality)
with open(script_path / 'out.jpg', 'wb') as f:
    f.write(jpeg)
