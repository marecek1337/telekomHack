import os, re, sys, subprocess, pandas as pd, shutil
from openai import OpenAI
api_key = ""
client = OpenAI(api_key=api_key)
print(f"Using API Key: {client.api_key}")
# def get_key():
#     try:
#         with open("config.json", 'r') as file:
#             config_data = json.load(file)
#             return config_data.get("key")
#     except:
#         print("openai.py -> get_key: error opening/reading the file")

def send_to_chatgpt(prompt):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a data analysis assistant and Python code expert."},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content


# generate graphs and save it to directory graph/ as .png
#
def generate_graphs(file_path, given_prompt):
    try:
        df = pd.read_csv(file_path)
        print("\nFirst 5 rows of data:")
        print(df.head())

        prompt = f"""
        Here is my dataset:\n\n{df.head(10).to_string(index=False)}\n\n
        Using this dataset and this given prompt: {given_prompt}, provide Python code to generate suitable 5 graphs for data scientist salary analysis. And then save them to directory graphs/ as html
        First **Return ONLY Python code** without any explanation, comments, or extra text. Ensure the code is ready to execute as is.
        We already have data in pandas dataset df you NEED to use df as dataset
        also before generating graphs, check if they need normilisation and if they do, normilize
        use ONLY plotly
        dont use sklearn
        as code make a description of each graphic like this:


        graphs:

        FILENAMEOFTHEGRAPH.png: This graph represents


        write it to the file description/descriptions_graphs.txt
        also make a comprehensive description like data scientist and write it to the description/description.txt
        """
        print("\nSending to ChatGPT...")
        gpt_response = send_to_chatgpt(prompt)
        gpt_response = gpt_response[9:(len(gpt_response) - 4)]
        print("\nAnswer of ChatGPT:")
        print(gpt_response)
        from plot import _install_dependencies
        _install_dependencies(gpt_response)
        exec(gpt_response)



    except Exception as e:
        print(f"Error: {e}")


def ask(str, file_path=None):
    '''
    ask gpt a question
    specify the file so gpt will craft a code to plot a graph
    '''
    if file_path:
        try:
            with open(file_path, "r") as file:
                file_content = file.read()
                # Append file content
                str += f"\n{file_content}"
        except:
            pass
    
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", 
             "content": str}
        ]
    )
    return completion.choices[0].message.content

def _install_dependencies(code):
    """
    Installs dependencies mentioned in the code using pip.
    Filters out standard libraries that do not require installation.
    """
    # List of common standard libraries to exclude from installation
    standard_libraries = {
        'os', 'sys', 're', 'math', 'datetime', 'json', 'logging', 
        'subprocess', 'pathlib', 'collections', 'itertools', 'threading',
        'queue', 'random', 'statistics', 'functools', 'MinMaxScaler', 'make_subplots'
    }
    
    # Match import statements
    imports = re.findall(r"import (\w+)", code)
    for lib in imports:
        if lib in standard_libraries:
            print(f"Skipping standard library: {lib}")
            continue
        print(f"Installing dependency: {lib}")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {lib}: {e}")



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

counter = 0

def get_path(u_input):
    global counter
    counter += 1
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
    if counter == 10:
        return None
    return get_path(u_input)


def delete_folder(folder_path):
    try:
        shutil.rmtree(folder_path)
        print(f"Deleted folder and its contents: {folder_path}")
    except FileNotFoundError:
        print(f"Folder not found: {folder_path}")
    except Exception as e:
        print(f"Error deleting folder {folder_path}: {e}")

def _generate_code_to_plot(u_input, path):
    # Get the absolute path to the parent folder of 'src'
    base_dir = os.path.dirname(os.path.dirname(__file__))  # Parent directory of 'src'
    
    # Construct the full path to the 'data' folder
    data_folder = os.path.join(base_dir, "data")
    full_path = os.path.join(data_folder, path)  # Full path to the data file
    print(full_path)
    
    try:
        # Read a preview of the data
        data_preview = pd.read_csv(full_path).head().to_string(index=False)
    except FileNotFoundError:
        return f"Error: The file at {full_path} was not found."
    except Exception as e:
        return f"Error reading the file: {str(e)}"

    # Construct the prompt
    
    prompt = (
        f"Generate code in javascript to plot a graph. "
        f"First **Return ONLY javascript code** without any explanation, comments, or extra text. Ensure the code is ready to execute as is."
        f"file with data for the graph is located here {full_path}. "
        f"Plot the data based on this text: '{u_input}'.\n\n"
        f"Here is a preview of the data:\n{data_preview}"
    )
    code = ask(prompt, full_path)
    return code    

def _sanitize_response(response):
    """
    Extracts Python code blocks from the given response text.
    """
    # Match text inside triple backticks ```python ... ```
    code_blocks = re.findall(r"```javascript(.*?)```", response, re.DOTALL)
    if code_blocks:
        # Return the first code block found (assuming only one block is needed)
        return code_blocks[0].strip()
    else:
        print("No Python code block found in the response.")
        return None

def execute(u_input):
    # u_input = input("> ")
    # path to get file from
    # try:
    #     delete_folder("graphs")
    # except:
    #     pass

    path = get_path(u_input)

    if not path:
        print("File with similar name not found")

    code = _generate_code_to_plot(u_input, path)
    try:
        code = _sanitize_response(code)
    except:
        pass

    print(code)
    return code
    # plot graph using specified file
    # from generate_graph import generate_graphs
    # # generate_graphs(path, u_input)

execute('potreboval by som data ohladom poctu ludi co zomreli pocas covidu')

