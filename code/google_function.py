from apiclient import errors
from apiclient.http import MediaFileUpload
from apiclient.http import MediaIoBaseDownload

import httplib2
from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
import urllib3
#import sys

#sys.stdout = open("/dev/null", "w")
urllib3.disable_warnings()


def build_service() :
	storage = Storage('.google_credentials')
	credentials = storage.get()


	http = httplib2.Http()
	http = credentials.authorize(http)

	service = build('drive', 'v2', http=http)
	return service




def retrieve_all_files(service):
  """Retrieve a list of File resources.

  Args:
    service: Drive API service instance.
  Returns:
    List of File resources.
  """
  result = []
  page_token = None
  while True:
    try:
      param = {}
      if page_token:
        param['pageToken'] = page_token
      files = service.files().list(**param).execute()

      result.extend(files['items'])
      page_token = files.get('nextPageToken')
      if not page_token:
        break
    except errors.HttpError, error:
      print 'An error occurred: %s' % error
      break
  return result




def delete_file(service, filename):

	result = []
	result = retrieve_all_files(service)
	for i in result :
		print i['id']
		original_name = i['originalFilename']
		if i['title'] == filename:
			tmp = i['id']
			break

	try:
		service.files().delete(fileId=tmp).execute()
                print 'Google delete complete'
	except errors.HttpError, error:
		print 'An error occurred: %s' % error




def insert_file(service, filename):
  """Insert new file.

  Args:
    service: Drive API service instance.
    title: Title of the file to insert, including the extension.
    description: Description of the file to insert.
    parent_id: Parent folder's ID.
    mime_type: MIME type of the file to insert.
    filename: Filename of the file to insert.
  Returns:
    Inserted file metadata if successful, None otherwise.
  """
  media_body = MediaFileUpload(filename, mimetype='text/plain', resumable=True)
  body = {
    'title': filename,
    'mimeType': 'text/plain'
  }


  try:
    file = service.files().insert(
        body=body,
        media_body=media_body).execute()

    print 'Google upload complete'
    return file
  except errors.HttpError, error:
    print 'An error occured: %s' % error
    return None



def download_file(service, filename):
	result = []
	result = retrieve_all_files(service)
	for i in result :

		if i['title'] == filename:

			tmp = i['id']
			break
	f = open (filename, 'wb')

	request = service.files().get_media(fileId=tmp)
	media_request = MediaIoBaseDownload(f, request)



	while True:
		try:
			download_progress, done = media_request.next_chunk()
		except errors.HttpError, error:
			print 'An error occurred: %s' % error
			return
		#if download_progress:
		#	print 'Download Progress: %d%%' % int(download_progress.progress() * 100)
		if done:
			print 'Google download complete'
			return
if __name__ == '__main__':
    FILENAME = '0.jpg'
    service = build_service()
    #insert_file(service, FILENAME)
    #download_file(service, FILENAME)
    delete_file(service, FILENAME)