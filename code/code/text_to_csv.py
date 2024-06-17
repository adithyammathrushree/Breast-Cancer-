import re
from itertools import islice
import csv


#--def listToString(sentence):
#--	s = ""
#--	for ele in sentence:
#--		s += ele
#--	print(type(s))
#--	return s

def convert(lst, var_lst):
	idx = 0
	for var_len in var_lst:
		yield lst[idx : idx + var_len]
		idx += var_len


def text_to_csv():
	with open('static/files/text.txt') as file:
		sentence = file.readlines() #type(sentence)=list

	s = ""            # type(s)=string
	for ele in sentence:
		s += ele
	#print(type(s))     #string
	#print(s)

	value = [float(value) for value in re.findall(r'-?\d+\.?\d*', s)]
	#print(type(value))               #1 d list
	#print(value)

	lst=value
	var_lst=[30]
	rows=list(convert(lst, var_lst))
	#print(type(rows))                 #2 d list
	#print(rows)


	#fields = ['Name', 'Branch', 'Year', 'CGPA'] 
   
	#rows = [[22.23, 4.43, 34.43, 22.2, 22.23, 4.43, 34.43, 22.2, 22.23, 4.43, 34.43, 22.2]]
  
	with open('static/files/image_extracted.csv', 'w') as f:
		# using csv.writer method from CSV package
		write = csv.writer(f)
		#write.writerow(fields)
		write.writerows(rows)