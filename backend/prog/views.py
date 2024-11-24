import ssl
from urllib.request import urlopen
from django.http import HttpResponse
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
            f"Generate a JavaScript code to plot graphs using this dataset alter data a bit if they are boring or doesnt make sence:\n\n{data_preview}\n\n"
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

def file_description(user_input):
    """
    Načíta popis súboru na základe dynamicky získanej cesty k súboru.
    """
    try:
        # Zavolaj process_request na získanie cesty k súboru
        process_request(user_input)

        # Skontroluj, či bola cesta k súboru úspešne nastavená
        global path_to_file
        if not path_to_file:
            print("File path could not be determined.")
            return "File path could not be determined."

        # Načítanie CSV súboru
        full_path = os.path.join(os.getcwd(), "../data", path_to_file)
        if not os.path.exists(full_path):
            print(f"File {full_path} does not exist.")
            return "File could not be found at the determined path."

        print(f"Loading file: {full_path}")
        df = pd.read_csv(full_path)
        print("File loaded successfully.")

        # Konvertovanie dát na string
        data_string = df.to_string(index=False)
        max_chars = 128000 * 3  # Limit na maximálny počet znakov
        truncated_data = data_string[:max_chars]

        # Generovanie promptu
        prompt = (
            f"Summarize the following data briefly and clearly without any formatting. "
            f"Keep the summary concise and factual. "
            f"Here is the data:\n\n{truncated_data}"
        )
        print("Prompt generated.")

        # Odoslanie na OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a data summarization assistant."},
                {"role": "user", "content": prompt},
            ],
        )
        print("OpenAI response received.")
        return response.choices[0].message.content

    except Exception as e:
        print(f"Error in file_description: {str(e)}")
        return None



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
    Vracia výstup z funkcie file_description ako JSON odpoveď.
    """
    try:
        if request.method == 'POST':
            # Získanie query z tela POST požiadavky
            data = json.loads(request.body)
            user_input = data.get('query')
        elif request.method == 'GET':
            # Získanie query z GET parametrov
            user_input = request.GET.get('query')
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=405)

        # Overenie, či bola query poslaná
        if not user_input:
            return JsonResponse({'error': 'Query parameter is required.'}, status=400)

        # Zavolanie funkcie file_description s user_input
        description = file_description(user_input)

        if not description:
            return JsonResponse({"error": "Failed to generate file description"}, status=500)

        # Skrátenie odpovede na 300 znakov a odstránenie formátovania
        short_description = re.sub(r'\s+', ' ', description.strip())[:300]

        # Vrátenie výstupu z file_description v JSON formáte
        return JsonResponse({"message": short_description})
    except Exception as e:
        # Spracovanie chyby
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)


@csrf_exempt
def get_chart(request):
    """
    Dynamicky generuje JavaScriptový kód na vykreslenie grafu a vracia ho ako čistý kód použiteľný priamo na stránke.
    """
    try:
        if request.method == 'POST':
            # Získanie query z tela POST požiadavky
            data = json.loads(request.body.decode('utf-8'))
            user_input = data.get('query')
        elif request.method == 'GET':
            # Získanie query z GET parametrov
            user_input = request.GET.get('query')
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=405)

        # Overenie, či bola query poslaná
        if not user_input:
            return JsonResponse({'error': 'Query parameter is required.'}, status=400)

        # Zavolanie process_request s user_input
        chart_code = process_request(user_input)

        if not chart_code:
            return JsonResponse({"error": "Failed to generate chart code"}, status=500)

        # Odstránenie prebytočných znakov, ak je to potrebné
        clean_chart_code = chart_code.strip()

        # Vrátenie JavaScriptového kódu v odpovedi
        return HttpResponse(clean_chart_code, content_type="application/javascript")
    except Exception as e:
        # Spracovanie chyby
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)



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

import requests
import os
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def download_file(request):
    print("Downloading file")
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            url = data.get('url')
            if not url:
                return JsonResponse({'error': 'URL is required'}, status=400)

            context = ssl._create_unverified_context()

            url = "https://data.montgomerycountymd.gov/api/views/mmzv-x632/rows.csv?accessType=DOWNLOAD"
            response = urlopen(url, context=context)
            # Get the Content-Disposition header
            content_disposition = response.getheader('Content-Disposition')

            # Extract filename from the Content-Disposition header
            filename = "default.csv"
            if content_disposition:
                # The header will look like 'attachment; filename="Crash_Reporting_-_Drivers_Data.csv"'
                filename = content_disposition.split('filename=')[-1].strip('\"')
            else:
                # Fallback to the URL's basename if no content disposition header exists
                filename = url.split('/')[-1].split('?')[0]

            save_path = os.path.join("../data/Downloads/")
            os.makedirs(save_path, exist_ok=True)
            file_name = os.path.join(save_path, filename)

            # Download the file
            response = requests.get(url)
            if response.status_code == 200:
                with open(file_name, 'wb') as file:
                    file.write(response.content)
                return JsonResponse({'message': f'File downloaded successfully to {file_name}'}, status=200)
            else:
                return JsonResponse({'error': f'Failed to download file. Status code: {response.status_code}'},
                                    status=500)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': f'Failed to download file: {e}'}, status=500)
        except PermissionError as e:
            return JsonResponse({'error': f'Permission denied: {e}'}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def validate_query(request):
    """
    Overí, či query dáva zmysel na základe pevne definovanej stromovej štruktúry a je obsahovo blízko téme.
    """
    try:
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            user_query = data.get('query')
        elif request.method == 'GET':
            user_query = request.GET.get('query')
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=405)

        if not user_query:
            return JsonResponse({'error': 'Query parameter is required.'}, status=400)

        # Pevne definovaná stromová štruktúra
        tree_structure = """
        .
        ├── T-Systems
        │   ├── hardware
        │   │   ├── memory.csv
        │   │   ├── peripherals.csv
        │   │   ├── processors.csv
        │   │   └── storage.csv
        │   ├── hr
        │   │   ├── benefits.csv
        │   │   ├── payroll.csv
        │   │   └── recruitment.csv
        │   ├── management
        │   │   ├── meetings.csv
        │   │   ├── policies.csv
        │   │   └── reports.csv
        │   ├── notebooks
        │   │   ├── dell.csv
        │   │   ├── hp.csv
        │   │   └── lenovo.csv
        │   ├── pcs
        │   │   ├── desktop
        │   │   │   ├── dell.csv
        │   │   │   └── hp.csv
        │   │   └── laptops
        │   │       ├── macbook.csv
        │   │       └── surface.csv
        │   ├── people
        │   │   ├── contractors
        │   │   │   ├── it.csv
        │   │   │   └── marketing.csv
        │   │   └── employees
        │   │       ├── engineering.csv
        │   │       ├── hr.csv
        │   │       └── sales.csv
        │   ├── projects
        │   │   ├── active.csv
        │   │   └── archived.csv
        │   └── software
        │       ├── applications.csv
        │       ├── licenses.csv
        │       └── operating_systems.csv
        ├── abc.txt
        └── people
            └── time_series_covid19_deaths_global.csv
        """

        # Zoznam kľúčových slov, ktoré by mali byť v query
        relevant_keywords = [
            # Všeobecné pojmy
            "T-Systems", "Telekom", "hardware", "hr", "management", "notebooks", "pcs", 
            "people", "projects", "software", "employees", "data", "files", "folders",

            # Hardvér a IT
            "memory", "storage", "peripherals", "processors", "servers", "dell", "hp", 
            "lenovo", "macbook", "laptops", "desktop", "computers", "equipment",

            # Ľudské zdroje
            "payroll", "benefits", "recruitment", "contractors", "employees", "engineering", 
            "sales", "marketing", "team", "people", "departments", "workforce",

            # Projekty a riadenie
            "meetings", "policies", "reports", "tasks", "deadlines", "active", "archived", 
            "documents", "governance", "project management", "timelines",

            # Softvér
            "applications", "licenses", "operating systems", "OS", "tools", "programs", 
            "solutions", "digital transformation",

            # COVID-19 a súvisiace dáta
            "covid", "pandemic", "deaths", "time series", "global", "health", 
            "statistics", "disease",

            # Telekom a firemné témy
            "telecom", "telecommunication", "T-Mobile", "networks", "services", "infrastructure", 
            "enterprise", "customers", "broadband", "connectivity", "solutions", 
            "IT infrastructure",

            # Ďalšie všeobecné témy
            "analytics", "data science", "reports", "charts", "tables", "datasets", 
            "files", "exports", "cloud", "AI", "machine learning"
        ]


        # Kontrola, či query obsahuje kľúčové slovo
        if any(keyword.lower() in user_query.lower() for keyword in relevant_keywords):
            return JsonResponse({"valid": True, "message": "The query is valid."})

        # Generovanie promptu na validáciu pomocou API
        validation_prompt = (
            f"Based on the folder structure below, does this query make sense? "
            f"Focus on whether the query relates to the listed topics or files. "
            f"Respond with 'yes' if it is related, otherwise respond with 'no'. "
            f"Query: {user_query}\n\n"
            f"Folder Structure:\n{tree_structure}"
        )

        # Poslanie na OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a folder structure validation assistant."},
                {"role": "user", "content": validation_prompt},
            ],
        )

        # Spracovanie odpovede
        validation_response = response.choices[0].message.content.strip().lower()
        if "yes" in validation_response:
            return JsonResponse({"valid": True, "message": "The query is valid."})
        else:
            explanation = re.sub(r'\s+', ' ', validation_response)[:300]  # Skrátenie na 300 znakov
            return JsonResponse({"valid": False, "message": explanation})

    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
