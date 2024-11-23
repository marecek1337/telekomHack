from src.ai import ask
import os

def get_tree_structure(root_folder, indent=""):
    tree = []
    items = os.listdir(root_folder)
    for index, item in enumerate(items):
        # Check if it's the last item for this level
        is_last = index == len(items) - 1
        
        # Build the tree prefix
        prefix = "└── " if is_last else "├── "
        tree.append(f"{indent}{prefix}{item}")
        
        # If the item is a directory, recursively get its structure
        item_path = os.path.join(root_folder, item)
        if os.path.isdir(item_path):
            # Increase indentation for subdirectories
            sub_indent = "    " if is_last else "│   "
            tree.extend(get_tree_structure(item_path, indent + sub_indent))
    
    return tree

def save_tree_structure_to_file(root_folder, output_file):
    tree = get_tree_structure(root_folder)
    with open(output_file, "w") as file:
        file.write("\n".join(tree))
    print(f"Tree structure saved to {output_file}")

def get_path(response):
    # Extract the line starting with "targetfolder="
    for line in response.splitlines():
        if line.startswith("targetfolder="):
            # Extract the path from the response
            path = line.split("=")[1].strip("'").strip('"')
            print(f"Extracted path: {path}")
            return path
    print("Path not found in the response.")
    return None

def main():
    # get tree structure
    tree = get_tree_structure(f"{os.getcwd()}/data")

    # ask(input("Your prompt: "))
    answer = ask(f"can u find the path to the file where data from macbook is saved? here is the structure: {tree}. Print it out like this targetfolder='path'")
    get_path(answer)

if __name__ == "__main__":
    main()