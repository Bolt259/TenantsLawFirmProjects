from pathlib import Path
import win32com.client as win32

# Create output folder
output_dir = Path.cwd() / "Testing-Output"
output_dir.mkdir(parents=True, exist_ok=True)

# Connect to Outlook
outlook = win32.Dispatch("Outlook.Application").GetNamespace("MAPI")

# Access a specific email account by name
account_name = "LukasS@tenantslawfirm.com"
for account in outlook.Folders:
    print(f"{account.Name}")
exit(1)

# Create folder for all messages    
all_folder = output_dir / "this_new_ass_folder"
all_folder.mkdir(parents=True, exist_ok=True)

# Get messages
messages = inbox.Items

for message in messages:
    attachments = message.Attachments
    for attachment in attachments:
        attachment.SaveAsFile(all_folder / str(attachment))

print("Attachments saved successfully.")
