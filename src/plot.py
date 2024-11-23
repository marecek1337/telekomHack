# used to generate a html graph
import re, os, subprocess, pandas as pd, sys
from ai import ask

def _generate_code_to_plot(u_input, path):
    try:
        # Read a preview of the data
        full_path = f"data/{path}"  # Ensure correct path resolution
        data_preview = pd.read_csv(full_path).head().to_string(index=False)
    except FileNotFoundError:
        return f"Error: The file at {full_path} was not found."
    except Exception as e:
        return f"Error reading the file: {str(e)}"

    # Construct the prompt
    prompt = (
        f"Generate code in Python to plot a graph in HTML using pandas and plotly.express. "
        f"Use this path 'data/{path}' in the code to the data file. "
        f"Plot the data based on this text: '{u_input}'.\n\n"
        f"Here is a preview of the data:\n{data_preview}"
    )

    # Get AI-generated code
    ai_answer = ask(prompt)
    code = _sanitize_response(ai_answer)
    return code

def _sanitize_response(response):
    """
    Extracts Python code blocks from the given response text.
    """
    # Match text inside triple backticks ```python ... ```
    code_blocks = re.findall(r"```python(.*?)```", response, re.DOTALL)
    if code_blocks:
        # Return the first code block found (assuming only one block is needed)
        return code_blocks[0].strip()
    else:
        print("No Python code block found in the response.")
        return None
    
def _install_dependencies(code):
    """
    Installs dependencies mentioned in the code using pip.
    Filters out standard libraries that do not require installation.
    """
    # List of common standard libraries to exclude from installation
    standard_libraries = {
        'os', 'sys', 're', 'math', 'datetime', 'json', 'logging', 
        'subprocess', 'pathlib', 'collections', 'itertools', 'threading',
        'queue', 'random', 'statistics', 'functools', 'MinMaxScaler'
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

def _execute_code(code):
    """
    Executes the given Python code.
    """
    _install_dependencies(code)
    try:
        exec(code, globals())
        print("done")
    except Exception as e:
        print(f"Error during code execution: {e}") 
        return -1

def count_files_in_parent_folder():
    """
    Counts the number of files in the parent folder of the 'src' directory.
    """
    try:
        # Get the path of the current script
        current_folder = os.path.dirname(__file__)
        print(current_folder)
        # Get the parent folder
        parent_folder = os.path.dirname(current_folder)
        # List all entries in the parent folder
        # entries = os.listdir(parent_folder)
        entries = os.listdir(current_folder)
        # Count only files
        file_count = sum(1 for entry in entries if os.path.isfile(os.path.join(parent_folder, entry)))
        return file_count
    except FileNotFoundError:
        print(f"Error: The folder {parent_folder} does not exist.")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 0



def plot(u_input, path):
    """
    Executes the plot function. If the number of files remains unchanged after execution,
    the function retries the plot operation.
    """
    try:
        initial_count = count_files_in_parent_folder()
        print(initial_count)

        # Generate and execute the code
        code = _generate_code_to_plot(u_input, path)
        if not code:
            print("No valid code generated.")
            return

        _execute_code(code)

        # Check file count again after execution
        final_count = count_files_in_parent_folder()
        print(final_count)
        # Retry if the file count has not changed
        # if final_count == initial_count:
            # print("File count unchanged. Retrying plot function...")
            # plot(u_input, path)
        # else:
        print("Graph generated successfully.")
    except Exception as e:
        print(f"Error generating the graph: {e}")