import xlsxwriter
import os
from tkinter import filedialog
from tkinter import *

def get_input():
	filelist = []
	num_files = 2
	counter = 1
	root = Tk()

	# allow users to select their input file
	while counter <= num_files:
		root = Tk()
		root.filename = filedialog.askopenfilename(initialdir = "/",title = "Select file " + str(counter)
			,filetypes = (("txt files","*.txt"),("all files","*.*")))
		filelist.append(root.filename)
		counter += 1

	return filelist

def validate_filelist(filelist):
	result = False
	# check if two unique files were entered.  If not, prompt for input again.
	while not result:
		if filelist[0] != filelist[1]:
			result = True
		else:
			print ("Same file has been selected twice!  Please select two different files for comparison.")
			filelist = get_input()

	return filelist

def build_dictionary(lines,server,compareDict):
	# read the input file and build a dictionary storing folder, file name, size, and date
	dictionary = compareDict
	folder = ''

	for line in lines:
		if line.strip().startswith('./'):
			if len(line) > 2:
				folder = line.strip()[2:]
		elif len(line) > 20:
			splitlines = line.split()
			size = splitlines[4]
			filename = splitlines[-1]
			filedate = ' '.join(splitlines[5:-1])
			servername = server.split('.')[0].split('/')[-1:][0]
			
			# if the filename doesn't exist, initialize the nested dictionary
			if folder not in dictionary.keys():
				dictionary[folder] = {}
			if filename not in dictionary[folder].keys():
				dictionary[folder][filename] = {}

			#print (filename, servername, size, filedate)
			dictionary[folder][filename][servername] = [size, filedate]

	return dictionary

def compare_files(compareDict, filelist):
	# create the headers for the individual sheets
	servername1 = filelist[0].split('.')[0].split('/')[-1:][0]
	servername2 = filelist[1].split('.')[0].split('/')[-1:][0]
	printMatch = [['Folder','Filename', 'File Size', 'File Date']]
	printNotMatch = [['Folder','Filename', servername1 + ' File Size', servername1 + ' File Date',
					servername2 + ' File Size', servername2 + ' File Date']]
	printSolo = [['Server', 'Folder', 'Filename', 'File Size', 'File Date']]

	for folder, stuff in compareDict.items():
		for filename, values in stuff.items():
			if len(values) == 2:
				# if a filename is present in both servers, check if the size and date matches.
				# if the size and date match, write to Match
				if values[servername1] == values[servername2]:
					size = values[servername1][0]
					date = values[servername1][1]
					temp = [folder,filename, size, date]
					printMatch.append(temp)
				
				# if the size and date don't match, write to NotMatch	
				else:
					size1 = values[servername1][0]
					date1 = values[servername1][1]
					size2 = values[servername2][0]
					date2 = values[servername2][1]
					temp2 = [folder,filename, size1, date1, size2, date2]
					printNotMatch.append(temp2)

			# if the file only exists in one server, write to Solo
			else:
				for servername, data in values.items():
					server = servername.split('.')[0]
					size = data[0]
					date = data[1]
					temp3 = [server, folder, filename, size, date]
					printSolo.append(temp3)
					#print(servername.split('.')[0] + ',' + filename + ',' + data[0] + ',' + data[1] + '\n')

	return printMatch, printNotMatch, printSolo

def print_list(lists, worksheet):
	row = 0
	col = 0
	# for each item in the list, write to the appropriate excel worksheet
	for array in lists:
		i = 0
		while i < len(array):
			worksheet.write(row, col + i, array[i])
			if row == 0:
				worksheet.set_column(row,i,20)
			i += 1
		row += 1

	return None


########################################################################

compareDict = {}
outfile = 'Validation.xlsx'

# get files to compare data
filelist = get_input()

# validate input files
filelist_clean = validate_filelist(filelist)

# build dictionary
for file in filelist_clean:
	with open(file, 'r') as f:
		lines = f.readlines()
		compareDict = build_dictionary(lines,file,compareDict)
#print (compareDict)

# perform comparison
printMatch, printNotMatch, printSolo = compare_files(compareDict, filelist_clean)

# print results to excel
if printMatch or printNotMatch or printSolo:
	print ("Writing to " + outfile + "...")
	workbook = xlsxwriter.Workbook(outfile)

	if printMatch:
		match = workbook.add_worksheet('Matched')
		print_list(printMatch, match)

	if printNotMatch:
		notmatch = workbook.add_worksheet('Not Matched')
		print_list(printNotMatch, notmatch)

	if printSolo:
		solo = workbook.add_worksheet('Error')
		print_list(printSolo, solo)
	
	workbook.close()
