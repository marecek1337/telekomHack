from django.http import JsonResponse
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import json
import os
import re
import subprocess
import sys
import pandas as pd
from openai import OpenAI



api_key = ""
client = OpenAI(api_key=api_key)

path_to_file = ""
tree = []

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
        global tree
        tree = tree_structure
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

        global path_to_file
        path_to_file = file_path
        # 4. Načítanie súboru a zobrazenie ukážky
        full_path = os.path.join(root_folder, file_path)
        if not os.path.exists(full_path):
            print(f"File not found at path: {full_path}")
            return

        df = pd.read_csv(full_path)
        data_preview = df.head(10).to_string(index=False)
        chart_code = """
        const dataset = {
          labels: ["1/22/20", "1/23/20", "1/24/20", "1/25/20", "1/26/20", "1/27/20", "1/28/20", "1/29/20", "1/30/20", "1/31/20", "2/1/20", "2/2/20", "2/3/20", "2/4/20", "2/5/20", "2/6/20", "2/7/20", "2/8/20", "2/9/20", "2/10/20", "2/11/20", "2/12/20", "2/13/20", "2/14/20", "2/15/20", "2/16/20", "2/17/20", "2/18/20", "2/19/20", "2/20/20", "2/21/20", "2/22/20", "2/23/20", "2/24/20", "2/25/20", "2/26/20", "2/27/20", "2/28/20", "2/29/20", "3/1/20", "3/2/20", "3/3/20", "3/4/20", "3/5/20", "3/6/20", "3/7/20", "3/8/20", "3/9/20"],
          datasets: [
            {
              label: "Afghanistan",
              data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              fill: false,
              borderColor: "red"
            },
            {
              label: "Albania",
              data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              fill: false,
              borderColor: "blue"
            },
            {
              label: "Algeria",
              data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              fill: false,
              borderColor: "green"
            }
          ]
        };

        const ctx = document.getElementById("myChart").getContext("2d");
        const myChart = new Chart(ctx, {
          type: "line",
          data: dataset,
          options: {
            responsive: true,
            plugins: {
              title: {
                display: true,
                text: "COVID-19 Deaths"
              }
            },
            scales: {
              x: {
                display: true,
                title: {
                  display: true,
                  text: "Date"
                }
              },
              y: {
                display: true,
                title: {
                  display: true,
                  text: "Deaths"
                }
              }
            }
          }
        });

                """
        # 5. Generovanie kódu na vykreslenie grafu
        graph_prompt = (
            f"Generate a JavaScript code to plot graphs using this dataset:\n\n{data_preview}\n\n"
            f"Here is the user query: {u_input}. "
            f"Ensure to return ONLY JavaScript code, without any explanation or comments and without dependencies."
            f"Here is the example that i excpect: \n\n{chart_code}"
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


        # 8. Výstup
        print(js_code)
        return js_code

    except Exception as e:
        print(f"Error: {str(e)}")
        return None


import pandas as pd
import os

def file_description():
    global path_to_file
    # path_to_file = "/home/istvan/Documents/Hackaton/telekomHack/data/people/time_series_covid19_deaths_global.csv"

    # Load the CSV file
    if not os.path.exists(path_to_file):
        print(f"File {path_to_file} does not exist.")
        return

    df = pd.read_csv(path_to_file)
    
    # Convert the DataFrame to a string representation
    data_string = df.to_string(index=False)
    
    # Estimate token count (1 token ≈ 4 characters in English text)
    max_chars = 128000 * 3 # Approximate maximum characters for 128,000 tokens
    truncated_data = data_string[:max_chars]

    prompt = (
        f"Give me a comprehensive text review of this file's contents. "
        f"Be sure to return only the review."
        f"Here is the data:\n\n{truncated_data}"
    )
    print("prompt generated")
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a data review assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    
    print(response.choices[0].message.content)
    return response.choices[0].message.content
file_description()

# def path_description():
#     global path_to_file
#     global tree

#     prompt = (
#         f"Give me a shor text review of this . "
#         f"Be sure to return only the review."
#         f"Here is the data:\n\n{truncated_data}"
#     )
    
#     print("prompt generated")
#     response = client.chat.completions.create(
#         model="gpt-4o",
#         messages=[
#             {"role": "system", "content": "You are a data review assistant."},
#             {"role": "user", "content": prompt},
#         ],
#     )
    


def current_date(request):
    # Ensure the request is a GET request
    if request.method == 'GET':
        # Get the current date and time
        now = datetime.now()
        current_date_str = now.strftime("%Y-%m-%d %H:%M:%S")
        process_request("potreboval by som data ohladom poctu ludi co zomreli pocas covidu")


        # Return the current date and time in a JSON response
        return JsonResponse({'current_date': current_date_str})
    else:
        # If the request is not a GET, return a 405 Method Not Allowed error
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def get_info(request):
    """
    Vracia jednoduchý text ako jednu položku v JSON formáte.
    """
    if request.method == 'GET':
        # Jednoduchý text ako jedna položka JSON
        info = {
            "message": "Hello, this is your single JSON response!"
        }
        return JsonResponse(info)
    else:
        # Ak nie je požiadavka typu GET
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def get_chart(request):
    """
    Vracia JavaScriptový kód na vykreslenie grafu v JSON formáte.
    """
    if request.method == 'GET':
        # JavaScriptový kód na graf
        chart_code = """
const dataset = {
  labels: ["1/22/20", "1/23/20", "1/24/20", "1/25/20", "1/26/20", "1/27/20", "1/28/20", "1/29/20", "1/30/20", "1/31/20", "2/1/20", "2/2/20", "2/3/20", "2/4/20", "2/5/20", "2/6/20", "2/7/20", "2/8/20", "2/9/20", "2/10/20", "2/11/20", "2/12/20", "2/13/20", "2/14/20", "2/15/20", "2/16/20", "2/17/20", "2/18/20", "2/19/20", "2/20/20", "2/21/20", "2/22/20", "2/23/20", "2/24/20", "2/25/20", "2/26/20", "2/27/20", "2/28/20", "2/29/20", "3/1/20", "3/2/20", "3/3/20", "3/4/20", "3/5/20", "3/6/20", "3/7/20", "3/8/20", "3/9/20"],
  datasets: [
    {
      label: "Afghanistan",
      data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      fill: false,
      borderColor: "red"
    },
    {
      label: "Albania",
      data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      fill: false,
      borderColor: "blue"
    },
    {
      label: "Algeria",
      data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      fill: false,
      borderColor: "green"
    }
  ]
};

const ctx = document.getElementById("myChart").getContext("2d");
const myChart = new Chart(ctx, {
  type: "line",
  data: dataset,
  options: {
    responsive: true,
    plugins: {
      title: {
        display: true,
        text: "COVID-19 Deaths"
      }
    },
    scales: {
      x: {
        display: true,
        title: {
          display: true,
          text: "Date"
        }
      },
      y: {
        display: true,
        title: {
          display: true,
          text: "Deaths"
        }
      }
    }
  }
});

        """

        # Vrátenie JavaScriptového kódu v JSON formáte
        return JsonResponse({"chart_code": chart_code})
    else:
        # Ak nie je požiadavka typu GET
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def get_summary(request):
    """
    Vracia jednoduchý text ako jednu položku v JSON formáte.
    """
    if request.method == 'GET':
        # Jednoduchý text ako jedna položka JSON
        info = {
            "message": "Hello, this is your single JSON response!"
        }
        return JsonResponse(info)
    else:
        # Ak nie je požiadavka typu GET
        return JsonResponse({'error': 'Method not allowed'}, status=405)

