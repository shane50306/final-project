import sys

def splitFile(inputFile):

	f = open(inputFile, 'rb')
	data = f.read()
	f.close()

        bytes = len(data)

	chunk_size= bytes/3


	f = open(inputFile+'.001', 'wb')
	f.write(data[0:chunk_size])
	f.close()

	f = open(inputFile+'.002', 'wb')
	f.write(data[chunk_size:chunk_size*2])
	f.close()

	f = open(inputFile+'.003', 'wb')
	f.write(data[chunk_size*2:])
	f.close()


def joinFiles(fileName):

	f = open(fileName, 'wb')

	f1 = open(fileName+'.001', 'rb')
	f.write(f1.read())
	f1.close

	f1 = open(fileName+'.002', 'rb')
	f.write(f1.read())
	f1.close

	f1 = open(fileName+'.003', 'rb')
	f.write(f1.read())
	f1.close

	f.close()

if __name__ == '__main__':
	#splitFile(sys.argv[1])
	joinFiles(sys.argv[1])