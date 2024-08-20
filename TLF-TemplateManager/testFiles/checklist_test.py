import win32com.client

# Open the Word application
word = win32com.client.Dispatch('Word.Application')
doc = word.Documents.Open(r'C:\Users\sakul\Documents\Testing#\checklist_testing.docx')

# Iterate through the Content Controls
for control in doc.ContentControls:
    # Print all available attributes and methods
    print(dir(control))
    
    # Check if 'Type' attribute exists
    if hasattr(control, 'Type'):
        if control.Type == 1:  # Type 1 corresponds to CheckBox Content Controls
            print(f"Checkbox with tag '{control.Tag}' is {'checked' if control.Checked else 'unchecked'}")
    else:
        print("Control does not have 'Type' attribute")

# Close the document and Word application
doc.Close(False)
word.Quit()
