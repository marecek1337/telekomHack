from openai import OpenAI
client = OpenAI()

# def get_key():
#     try:
#         with open("config.json", 'r') as file:
#             config_data = json.load(file)
#             return config_data.get("key")
#     except:
#         print("openai.py -> get_key: error opening/reading the file")


def ask(str, file_path=None):
    '''
    ask gpt a question
    specify the file so gpt will craft a code to plot a graph using python
    '''
    if file_path:
        try:
            with open(file_path, "r") as file:
                file_content = file.read()
                # Append file content
                str += f"\n\nHere is the content of the file:\n{file_content}"
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




# ask(input("Ask smth: "))