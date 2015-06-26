
import httplib2
import pprint

from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage

# Copy your credentials from the console
CLIENT_ID = '776359830901-0u0trs3ekipsphkb1gh11qcuc6e7vt84.apps.googleusercontent.com'
CLIENT_SECRET = 'zZpVJeCFhynUf05I9GTHADsz'

# Check https://developers.google.com/drive/scopes for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'

# Redirect URI for installed apps
REDIRECT_URI = 'https://www.example.com/oauth2callback'

# Path to the file to upload
FILENAME = 'document.txt'

# Run through the OAuth flow and retrieve credentials

flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE,
                           redirect_uri=REDIRECT_URI)
authorize_url = flow.step1_get_authorize_url()
print 'Go to the following link in your browser: ' + authorize_url
code =  raw_input('Enter verification code: ').strip()
credentials = flow.step2_exchange(code)

storage = Storage('.google_credentials')
storage.put(credentials)
