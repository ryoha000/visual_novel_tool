import cv2

image = cv2.imread("ac.png")
gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
ret, bw_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_OTSU)
rev_img = cv2.bitwise_not(bw_image)
count = cv2.countNonZero(rev_img)
w_count = cv2.countNonZero(rev_img)
# 反転画像の白の数
print(count)
print(bw_image.size)
if count / bw_image.size < 0.9:
    print('ほとんど黒')
