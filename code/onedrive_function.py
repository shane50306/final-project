import os


def download(filename):
    command = "onedrive-cli get " + filename + " " + filename + " 2> /dev/null"
    os.system(command)
    print 'Onedrive download complete'

def upload(filename):
    command = "onedrive-cli put " + filename + " 2> /dev/null"
    os.system(command)
    print 'Onedrive upload complete'

def delete(filename):
    command = "onedrive-cli rm " + filename + " 2> /dev/null"
    os.system(command)
    print 'Onedrive delete complete'

if __name__ == '__main__':
    filename = "0.jpg"
    upload(filename)
#    download(filename)
#    delete(filename)

