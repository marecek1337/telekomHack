from ai import ask
from plot import plot
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

def get_path(u_input):
    # get tree structure
    tree = get_tree_structure(f"{os.getcwd()}/data")
    ai_answer = ask(f"Can u find the path to the file mentioned in this sentence: {u_input}? here is the folder structure: {tree}. Print it out like this targetfolder='path'")
    
    # Extract the line starting with "targetfolder="
    for line in ai_answer.splitlines():
        if line.startswith("targetfolder="):
            # Extract the path from the response
            path = line.split("=")[1].strip("'").strip('"')
            print(f"Extracted path: {path}")
            return path
    print("Path not found in the response.")
    get_path(u_input)


def main():
    u_input = input("> ")
    # path to get file from
    path = get_path(u_input)
    # plot graph using specified file
        

    # body #

if __name__ == "__main__":
    main()
# potreboval by som data ohladom poctu ludi co zomreli pocas covidu