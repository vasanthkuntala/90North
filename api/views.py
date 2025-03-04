from django.shortcuts import redirect
from django.http import JsonResponse,FileResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import io
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from googleapiclient.http import MediaIoBaseDownload

from django.conf import settings
from urllib.parse import urlencode
from io import BytesIO 

def google_auth(request):
    """
    Redirects the user to the Google OAuth consent screen.
    """
    params = {
        'client_id': settings.GOOGLE_CLIENT_ID,
        'redirect_uri': settings.GOOGLE_REDIRECT_URI,
        'response_type': 'code',
        'scope': ' '.join(settings.GOOGLE_SCOPES),
        'access_type': 'offline',
        'prompt': 'consent',
    }
    auth_url = f"{settings.GOOGLE_AUTH_URL}?{urlencode(params)}"
    return redirect(auth_url)


def google_callback(request):
    """
    Exchanges the Google authorization code for an access token.
    """
    code = request.GET.get('code')
    if not code:
        return JsonResponse({'error': 'Authorization code not found'}, status=400)

    token_data = {
        'code': code,
        'client_id': settings.GOOGLE_CLIENT_ID,
        'client_secret': settings.GOOGLE_CLIENT_SECRET,
        'redirect_uri': settings.GOOGLE_REDIRECT_URI,
        'grant_type': 'authorization_code'
    }

    response = requests.post(settings.GOOGLE_TOKEN_URL, data=token_data)
    token_json = response.json()

    if 'access_token' in token_json:
        return JsonResponse(token_json)
    else:
        return JsonResponse({'error': 'Failed to retrieve access token', 'details': token_json}, status=400)
    
@csrf_exempt
def drive_upload(request):
    """
    Uploads a file to Google Drive using a file sent via POST (form-data).
    Expects a form-data field named 'token' for the access token and 'file' for the uploaded file.
    """
    if request.method == 'POST':
        token = request.POST.get('token')
        if not token:
            return JsonResponse({'error': 'No token provided'}, status=400)

        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No file provided'}, status=400)

        uploaded_file = request.FILES['file']
   
        file_stream = BytesIO(uploaded_file.read())
    
        file_metadata = {'name': uploaded_file.name}
      
        media = MediaIoBaseUpload(file_stream, mimetype=uploaded_file.content_type, chunksize=1024*1024)

        try:
            creds = Credentials(token)
            drive_service = build('drive', 'v3', credentials=creds)
            file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            return JsonResponse({'file_id': file.get('id')})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)


@csrf_exempt
def drive_download(request):
    """
    Downloads a file from Google Drive and returns it as a file response.
    Expects a GET request with 'token' and 'file_id' as query parameters.
    """
    if request.method == 'GET':
        token = request.GET.get('token')
        file_id = request.GET.get('file_id')
        if not token or not file_id:
            return JsonResponse({'error': 'Token or file_id missing'}, status=400)

        try:
            
            creds = Credentials(token)
            drive_service = build('drive', 'v3', credentials=creds)

          
            file_metadata = drive_service.files().get(fileId=file_id, fields='name, mimeType').execute()
            file_name = file_metadata.get('name')
            mime_type = file_metadata.get('mimeType', 'application/octet-stream')

            request_download = drive_service.files().get_media(fileId=file_id)
            file_buffer = io.BytesIO()
            downloader = MediaIoBaseDownload(file_buffer, request_download)

            done = False
            while not done:
                status, done = downloader.next_chunk()
               
            file_buffer.seek(0)

           
            response = FileResponse(file_buffer, content_type=mime_type)
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return response

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)
