from PIL import Image
import pytesseract
import os


def image_to_text():

	image = Image.open("static/uploads/image.png")           #image path

	text=pytesseract.image_to_string(image)        #'text' contains text from image
	#print(type(text)) #string
	#print(text)


	#open text file
	text_file = open("static/files/text.txt", "w")
 
	#write string to file
	n = text_file.write(text) 
 
	#close file
	text_file.close()
 
	#print(n) #n=number of characters written to text file