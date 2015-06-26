import sys
sys.path.append("code/")

import dropbox_function
import onedrive_function
import google_function
import split_file
import os
from threading import Thread

google_service = google_function.build_service()
dropbox_service = dropbox_function.getAccess()

"""
def init():
    google_service = google_function.build_service()
    dropbox_service = dropbox_function.getAccess()
"""

def download(filename):


    thread_google = Thread(target=google_function.download_file, args=(google_service, filename+'.001'))
    thread_dropbox = Thread(target=dropbox_function.download, args=(filename+'.002', dropbox_service))
    thread_ondrive = Thread(target=onedrive_function.download, args=(filename+'.003', ))

    thread_google.setDaemon(True)
    thread_dropbox.setDaemon(True)
    thread_ondrive.setDaemon(True)

    thread_google.start()
    thread_dropbox.start()
    thread_ondrive.start()

    thread_google.join()
    thread_dropbox.join()
    thread_ondrive.join()

    split_file.joinFiles(filename)

    command = 'rm ' + filename + ".00* .google_credentials -f"
    os.system(command)

    print 'Download complete'


def upload(filename):
    split_file.splitFile(filename)

    thread_google = Thread(target=google_function.insert_file, args=(google_service, filename+'.001'))
    thread_dropbox = Thread(target=dropbox_function.upload, args=(filename+'.002', dropbox_service))
    thread_ondrive = Thread(target=onedrive_function.upload, args=(filename+'.003',) )

    thread_google.setDaemon(True)
    thread_dropbox.setDaemon(True)
    thread_ondrive.setDaemon(True)

    thread_google.start()
    thread_dropbox.start()
    thread_ondrive.start()

    thread_google.join()
    thread_dropbox.join()
    thread_ondrive.join()

    command = 'rm ' + filename + ".00* .google_credentials -f"
    os.system(command)

    print 'Upload complete'

def delete(filename):
    thread_google = Thread(target=google_function.delete_file, args=(google_service, filename+'.001'))
    thread_dropbox = Thread(target=dropbox_function.delete, args=(filename+'.002', dropbox_service))
    thread_ondrive = Thread(target=onedrive_function.delete, args=(filename+'.003', ))

    thread_google.setDaemon(True)
    thread_dropbox.setDaemon(True)
    thread_ondrive.setDaemon(True)

    thread_google.start()
    thread_dropbox.start()
    thread_ondrive.start()

    thread_google.join()
    thread_dropbox.join()
    thread_ondrive.join()

    print 'Delete complete'

def help_message():
        print '\nWelcome to Cloud Service Load Balance System\n'
        print 'To upload the file, please put the file into upload directory'
        print 'All the file download from the CSLB System will be put into download directory\n'
        print 'Please type:'
        print "\t'ls' for listing the file on the CSLB System"
        print "\t'ls upload' for listing the file in upload directory"
        print "\t'ls download' for listing the file in download directory"
        print "\t'upload filename' for upload a file to CSLB System"
        print "\t'download filename' for download a file on the CSLB System to local"
        print "\t'delete filename' for delete a file on the CSLB System"
        print "\t'help' for display this message"
        print "\t'exit' for exit"

def interface():
    help_message()
    while True:
        input = raw_input('>')

        if input == '':
            continue

        command = input.split()[0]
        if command == 'ls':
            if len(input.split()) == 2:
                if input.split()[1] == 'upload':
                    os.chdir("upload/")
                    files = [f for f in os.listdir('.') if os.path.isfile(f)]
                    for f in files:
                        print f
                    os.chdir("../")
                elif input.split()[1] == 'download':
                    os.chdir("download/")
                    files = [f for f in os.listdir('.') if os.path.isfile(f)]
                    for f in files:
                        print f
                    os.chdir("../")
                else:
                    print 'Command error!'
            elif len(input.split()) == 1:
                for line in open(".cslb_file", "r"):
                    for name in line.split():
                        print name
            else:
                print 'Command error!'

        elif command == 'upload':
            if len(input.split()) != 2:
                print 'Command error!'
            else:
                con=0
                filename = input.split()[1]
                for line in open(".cslb_file", "r"):
                    if filename in line.split():
                        print 'A duplicate file, please rename!'
                        con=1
                        break
                if con ==1:
                    con=0
                elif os.path.exists("upload/"+filename):
                    os.chdir("upload/")
                    upload(filename)
                    os.chdir("../")
                    f=open(".cslb_file", "a+")
                    f.write(filename+' ')
                    f.close()
                else:
                    print 'File {} not exist in local!'.format(filename)

        elif command == 'download':
            con=0
            if len(input.split()) != 2:
                print 'Command error!'
            else:
                filename = input.split()[1]
                for line in open(".cslb_file", "r"):
                    if filename in line:
                        os.chdir("download/")
                        download(filename)
                        os.chdir("../")
                        con=1
                        break
                if con == 1:
                    con=0
                else:
                    print 'File {} not exist on CSLB System!'.format(filename)

        elif command == 'delete':
            con=0
            if len(input.split()) != 2:
                print 'Command error!'
            else:
                filename = input.split()[1]
                for line in open(".cslb_file", "r"):
                    if filename in line:
                        con=1
                        break
                if con == 1:
                    f1 = open('.cslb_file', 'r')
                    f2 = open('.cslb_file.tmp', 'w')
                    for line in f1:
                            f2.write(line.replace(filename, ' '))
                    f1.close()
                    f2.close()
                    os.system('mv .cslb_file.tmp .cslb_file')
                    delete(filename)
                    con=0
                else:
                    print 'File {} not exist on CSLB System!'.format(filename)

        elif command == 'help':
            help_message()

        elif command == 'exit':
            return

        else:
            print 'Command error!'


if __name__ == "__main__":
    interface()
