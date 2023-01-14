from PIL import Image, ImageEnhance
import matplotlib.image as mpimg

image = mpimg.imread('test1.jpg')
# Opening Image
im = Image.fromarray(image)
  
# Creating object of Color class
im3 = ImageEnhance.Color(im)
  
# showing resultant image
im3.enhance(3).show()
