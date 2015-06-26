#!/usr/bin/env python2.7
import dropbox
import json
from pprint import pprint


def getAccess():

	f = open(".token","r")
	raw_data = f.readline()
	f.close()
	data = json.loads(raw_data)
	data = json.loads(data)

	client = dropbox.client.DropboxClient(data['access_token'])

	return client

def errorHandle(err):

	message = err.body

	print message['error']

def checkMetadata(file_name,client):

	try:
		file_meta = client.metadata('/' + str(file_name))

		# print "metadata : ",file_meta
		return 1
	except dropbox.rest.ErrorResponse as err:
		errorHandle(err)
		return 0


def upload(file_name ,client):

	f = open(file_name,'rb')
	response = client.put_file('/' + str(file_name),f)
        print 'Dropbox upload complete'

	# print "uploaded : ",response
	#print "Dropbox upload " + file_name +" successed."


def download(file_name,client):
	# first check the file if exist
	if checkMetadata(file_name,client):
		try:
			f, metadata = client.get_file_and_metadata('/' + str(file_name))

			out = open(file_name,'wb')
			out.write(f.read())
			out.close()
                        print 'Dropbox download complete'
			# print metadata
			#print "Dropbox download " + file_name + " successed."
		except dropbox.rest.ErrorResponse as err:
			errorHandle(err)


def delete(file_name,client):

	# first check the file if exist
	if checkMetadata(file_name,client):
		try:
			client.file_delete('/' + str(file_name))
                        print 'Dropbox delete complete'
			#print "Dropbox file deleted."
		except dropbox.rest.ErrorResponse as err:
			errorHandle(err)

def initial_dropbox():

	app_key = 'lkuio8x2i9t7qdd'
	app_sec = 'tbn6xfbbqnaw9d3'
	saved_token_in = '.token'

	flow = dropbox.client.DropboxOAuth2FlowNoRedirect( app_key, app_sec )

	haved_auth_file = 1


	try:
		f = open(saved_token_in,"r")
	except IOError:
		haved_auth_file = 0

	if  haved_auth_file == 0:
		# Doesn't have token file

		auth_url = flow.start()

		print '1. Go to: ' + auth_url
		print '2. Click "Allow" (you might have to log in first)'
		print '3. Copy the authorization code.'
		code =raw_input("Enter the authorization code here: ").strip()

		try:
			access_token,user_id = flow.finish(code)
		except:
			# if get any exception
			dropbox_ok = False
			return dropbox_ok

		client = dropbox.client.DropboxClient(access_token)
		print 'linked account: ',client.account_info()

		f = open(saved_token_in,"w")
		record = json.dumps({"client_info":client.account_info(),"access_token":access_token})
		json.dump(record,f)
		f.close()

		dropbox_ok = True
		return dropbox_ok

	else:
		# haved saved the token file
		dropbox_ok = True
		return	dropbox_ok


if __name__ == "__main__":

	if initial_dropbox() == True:

		# get access token
		client = getAccess()

		# test upload
		print "Test upload"
		file_name = raw_input("File name : ")
		upload(file_name,client)
#
#		# test download
		print "Test download"
		file_name = raw_input("File name : ")
		download(file_name,client)

		# test check file
#		print "Test check file"
#		file_name = raw_input("File name : ")
#		checkMetadata(file_name,client)

		# test delete
		print "Test delete"
		file_name = raw_input("File name : ")
		delete(file_name, client)

