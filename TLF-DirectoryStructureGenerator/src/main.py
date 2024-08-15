import os

def create_structure(base_path, structure):
    for item in structure:
        path = os.path.join(base_path, item['name'])
        if item['type'] == 'folder':
            os.makedirs(path, exist_ok=True)
            if 'contents' in item:
                create_structure(path, item['contents'])
        elif item['type'] == 'file':
            with open(path, 'w') as f:
                f.write(item.get('content', ''))
        print(f"Created {'directory' if item['type'] == 'folder' else 'file'}: {path}")

def main():
    structure = []
    while True:
        name = input("Enter the name of the folder/file (or 'done' to finish): ")
        if name.lower() == 'done':
            break
        type_flag = input("Is this a folder or a file? (f for folder, fi for file): ").strip().lower()
        depth = int(input("Enter the depth (0 for root level): ").strip())
        
        item = {'name': name, 'type': 'folder' if type_flag == 'f' else 'file'}
        
        if depth == 0:
            structure.append(item)
        else:
            current_level = structure
            for _ in range(depth - 1):
                if 'contents' not in current_level[-1]:
                    current_level[-1]['contents'] = []
                current_level = current_level[-1]['contents']
            if 'contents' not in current_level[-1]:
                current_level[-1]['contents'] = []
            current_level[-1]['contents'].append(item)
        
        if type_flag == 'fi':
            content = input(f"Enter content for the file '{name}' (or leave empty for none): ")
            item['content'] = content
    
    base_path = input("Enter the base path where the structure should be created: ").strip()
    create_structure(base_path, structure)
    print("Directory structure created successfully.")

if __name__ == "__main__":
    main()
