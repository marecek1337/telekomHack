import os
import re
import subprocess
import sys
import pandas as pd
from openai import OpenAI

api_key = ""
client = OpenAI(api_key=api_key)

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
        print("No js code block found in the response.")
        return None


def process_request(u_input):
    """
    Procesuje požiadavku: identifikuje súbor, analyzuje jeho štruktúru, generuje kód a vracia spracovaný výstup.
    """
    try:
        # 1. Nastavenie korektnej cesty k priečinku data
        root_folder = os.path.abspath(os.path.join(os.getcwd(), "../data"))  # Prechod o úroveň vyššie, potom do data
        print(f"Root folder: {root_folder}")

        if not os.path.exists(root_folder):
            print(f"Folder {root_folder} does not exist.")
            return

        # 2. Získanie stromovej štruktúry priečinkov
        tree_structure = []
        
        for dirpath, dirnames, filenames in os.walk(root_folder):
            indent = dirpath.replace(root_folder, "").count(os.sep) * "│   "
            tree_structure.append(f"{indent}├── {os.path.basename(dirpath)}")
            for filename in filenames:
                tree_structure.append(f"{indent}│   ├── {filename}")
        
        # 3. Identifikácia súboru na základe užívateľského vstupu
        prompt = (
            f"Can you find the path to the file mentioned in this sentence: {u_input}? "
            f"Here is the folder structure:\n{tree_structure}\n\n"
            f"Respond in this format: targetfolder='path'"
        )
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a file system analysis assistant."},
                {"role": "user", "content": prompt},
            ],
        )
        file_path = None
        for line in response.choices[0].message.content.splitlines():
            if line.startswith("targetfolder="):
                file_path = line.split("=")[1].strip("'").strip('"')
                break

        if not file_path:
            print("Path to file not found in response.")
            return

        # Oprava zdvojenia "data" v ceste
        if file_path.startswith("data/"):
            file_path = file_path[len("data/"):]

        # 4. Načítanie súboru a zobrazenie ukážky
        full_path = os.path.join(root_folder, file_path)
        if not os.path.exists(full_path):
            print(f"File not found at path: {full_path}")
            return

        df = pd.read_csv(full_path)
        data_preview = df.head(10).to_string(index=False)

        # 5. Generovanie kódu na vykreslenie grafu
        graph_prompt = (
            f"Generate a JavaScript code to plot graphs using this dataset:\n\n{data_preview}\n\n"
            f"Here is the user query: {u_input}. "
            f"Ensure to return ONLY JavaScript code, without any explanation or comments."
        )
        graph_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a data visualization assistant."},
                {"role": "user", "content": graph_prompt},
            ],
        )

        # 6. Extrakcia JavaScript kódu
        js_code = re.search(r"```javascript(.*?)```", graph_response.choices[0].message.content, re.DOTALL)
        if js_code:
            js_code = js_code.group(1).strip()
        else:
            print("No JavaScript code block found in response.")
            return

        # 7. Inštalácia závislostí, ak je to potrebné (v prípade Pythonu)
        dependencies = re.findall(r"import (\w+)", js_code)
        for dependency in dependencies:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", dependency])
            except subprocess.CalledProcessError as e:
                print(f"Failed to install dependency {dependency}: {e}")

        # 8. Výstup
        print(js_code)
        return js_code

    except Exception as e:
        print(f"Error: {str(e)}")
        return None


# Spustenie procesu
process_request("potreboval by som data ohladom poctu ludi co zomreli pocas covidu")
