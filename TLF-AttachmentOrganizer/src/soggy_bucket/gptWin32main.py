import os
import shutil
import time
from datetime import datetime
from dotenv import load_dotenv
import win32com.client as win32
import onedrivesdk
from onedrivesdk.helpers import GetAuthCodeServer

# Load environment variables from .env file
load_dotenv()

# Function to download attachments from Outlook
def download_attachments(save_folder):
    outlook = win32.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.Folders.Item("your_email@example.com").Folders.Item("Inbox")
    messages = inbox.Items

    for message in messages:
        for attachment in message.Attachments:
            local_path = os.path.join(save_folder, attachment.FileName)
            if not os.path.exists(local_path):
                attachment.SaveAsFile(local_path)
                print(f'Saved {attachment.FileName} to {local_path}')

# Function to organize files by date
def organize_files_by_date(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            file_date = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d')
            date_folder = os.path.join(folder_path, file_date)
            if not os.path.exists(date_folder):
                os.makedirs(date_folder)
            shutil.move(file_path, os.path.join(date_folder, filename))
            print(f'Moved {filename} to {date_folder}')

# Function to upload files to OneDrive
def upload_to_onedrive(client, folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'rb') as f:
                client.item(drive='me', path='root:/'+file).upload(f)
            print(f'Uploaded {file} to OneDrive')

# Main function to run the pipeline
def main():
    # Set up OneDrive client
    onedrive_client_id = os.getenv('ONEDRIVE_CLIENT_ID')
    onedrive_client_secret = os.getenv('ONEDRIVE_CLIENT_SECRET')
    onedrive_tenant_id = os.getenv('ONEDRIVE_TENANT_ID')
    redirect_uri = 'http://localhost:8080/'
    client = onedrivesdk.get_default_client(client_id=onedrive_client_id, scopes=['wl.signin', 'wl.offline_access', 'onedrive.readwrite'])
    auth_url = client.auth_provider.get_auth_url(redirect_uri)
    code = GetAuthCodeServer.get_auth_code(auth_url, redirect_uri)
    client.auth_provider.authenticate(code, redirect_uri, onedrive_client_secret)

    # Define paths
    save_folder = 'path/to/your/save/folder'

    while True:
        print("Checking for new attachments...")
        download_attachments(save_folder)
        organize_files_by_date(save_folder)
        upload_to_onedrive(client, save_folder)
        
        print("Cycle complete. Waiting for the next check...")
        # Wait for a specified interval before checking again (e.g., 10 minutes)
        time.sleep(600)  # 600 seconds = 10 minutes

if __name__ == "__main__":
    main()
