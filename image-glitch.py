import random
from random import randint
import os
import time
import sys, getopt

def chunks(l, n):
	n = max(1, n)
	return [l[i:i + n] for i in range(0, len(l), n)]
	
def getUniqueName(stages,mods):
		return str(stages)+"X_"+("".join(mods))+"_"+str(time.time())

HEADER_SIZE = 54

# =======  DATA MODIFICAION FUNCTIONS ========
REV = "reverse"
BITMATH = "bit maths"
RAND_CHUNKS = "random chunks"

def reverse(data):
	return bytearray(reversed(data))

	#randomize order of n sized chunks
def randomizeChunks(data,n):
	dataChunks = chunks(data,n)
	random.shuffle(dataChunks)
	
	data = []
	for chunk in dataChunks:
		data+=chunk
	return bytearray(data)
	
def bitMaths(data):
	for i in range(len(data)):
		byte = float(data[i])
		factor = 1.5
		#factor = random.uniform(1.6,2)
		byte *= factor
		
		byte = int(round(byte))
		if(byte >= 256):
			byte -= 256
		elif(byte < 0):
			byte = 1
		#print factor,byte
		data[i] = byte
	return data


# ==============================================

def main(argv):
	usage = "image-glitch.py -i <inputfile> -n <images> -s <stages>"
	try:
		opts, args = getopt.getopt(argv,"hi:n:s:")
	except getopt.GetoptError:
		print "arg error\n"+usage
		sys.exit(2)
	if(len(argv) <  4):
		print("Wrong arg number")
		print usage
		exit()
	#filesToOutput = 10
	#stages = 10	
	for opt, arg in opts:
		if opt == '-h':
			print usage
			sys.exit()
		elif opt in "-i":
			filename = arg
		elif opt in "-n":
			filesToOutput = int(arg)
		elif opt in "-s":
			stages = int(arg)
	#print 'Input file is "', inputfile
	


	print "Files : %s \nStages: %d \nNo. of images to generate: %d" % (filename,stages,filesToOutput)
	#if (raw_input("Continue") != "y"): 
	#	print("cancelled.")
	#	exit()

	#filename = "picture.bmp"
	#raw_input("Enter filename:")
	byteArray = open(filename, "rb").read()
	byteCount = len(byteArray)
	print "the file has",byteCount,"bytes -",float(byteCount)/1000000,"mb" 

	mods = [BITMATH]

	dir = "Glitched "+getUniqueName(stages,mods)+"/"
	os.mkdir(dir)



	for j in range(filesToOutput):
		#int(raw_input("How many stages?"))
		newByteArray = byteArray
		
		for i in range(stages):
			#generate random byte range
			addrA = randint(HEADER_SIZE+1,byteCount-2)
			addrB = randint(addrA,byteCount-1)
			#split data
			beforeData = bytearray(newByteArray[0:addrA])
			modifiedData = bytearray(newByteArray[addrA:addrB])
			afterData = bytearray(newByteArray[addrB:])
			#print(int(modifiedData[30]))
			#data modification stage
			#modifiedData = reverse(modifiedData)
			if(BITMATH in mods):
				modifiedData = bitMaths(modifiedData)
			#modifiedData = randomizeChunks(modifiedData,50000)

			#reassemble array
			newByteArray = beforeData+modifiedData+afterData
		
		file = getUniqueName(stages,mods)+filename
		
		with open(dir+file, 'wb') as output:
			newFileByteArray = bytearray(newByteArray)
			output.write(newFileByteArray)
		print "file ",j," outputted"


if __name__ == "__main__":
	main(sys.argv[1:])





