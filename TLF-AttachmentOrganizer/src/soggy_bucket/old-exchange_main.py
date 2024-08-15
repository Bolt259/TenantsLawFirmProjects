import os
import shutil
import time
from datetime import datetime
import pandas as pd
from exchangelib import Credentials, Account, DELEGATE, FileAttachment

# attachment collector
def collect_attachments(account, save_folder):
    for item in account.inbox.all().order_by('-datetime_recieved')[:100]:   # get latest 100 emails
        for attachment in item.attachments:
            if isinstance(attachment, FileAttachment):
                local_path = os.path.join(save_folder, attachment.name)
                if not os.path.exists(local_path):
                    with open(local_path, 'wb') as f:
                        f.write(attachment.content)
                    print(f'\nSaved {attachment.name} to {local_path}')   # make a logs system
    
# organize attachments by data within                    
def sort_files_in_(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.join(folder_path, filename)
        if os.path.isfile(file_path):
            # sort for specific file trait based on state
            
            '''
            if not os.path.exists(filetrait_folder):    # make a folder for this trait if needed
                os.makedirs(filetrait_folder)
            shutil.move(file_path, os.path.join(filetrait_folder, filename))

            print(f'\nMoved {filename} to {filetrait_folder}')   # make a logs system
            '''
            
# process files and create new ones using templates
def process_files(folder_path, template_path, output_folder):
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('changethis'):     # change file type check
                file_path = os.path.join(root, file)
                
                df = pd.read_csv(file_path)     # for csv file
                # process file data as needed to parse into template
                # maybe save it all into an intermediary file for transfer to the template
                
                # copy template into new file and parse data into template, rename file to relavant title
                
                
# pipeline driver
def main():
    # setup credentials
    credentials = Credentials("LukasS@tenantslawfirm.com", "SK1%UVb9Pd&e")

    # connect to account
    account = Account("LukasS@tenantslawfirm.com", credentials=credentials, autodiscover=True, access_type=DELEGATE)
    
    # define paths
    save_folder = r"C:\Users\sakul\Desktop\VS\Projects\TLF-AttachmentOrganizer\save_folder"
    template_path = r""
    output_folder = r"C:\Users\sakul\Desktop\VS\Projects\TLF-AttachmentOrganizer\output_folder"

    # ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    while True:
        print("\nGetting new attachments...")
        collect_attachments(account, save_folder)
        sort_files_in_(save_folder)
        process_files(save_folder, template_path, output_folder)
        
        time.sleep(350)      # wait 5 mins
        
        
if __name__ == "__main__":
    main()
