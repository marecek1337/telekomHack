from openai import OpenAI
client = OpenAI()

# def get_key():
#     try:
#         with open("config.json", 'r') as file:
#             config_data = json.load(file)
#             return config_data.get("key")
#     except:
#         print("openai.py -> get_key: error opening/reading the file")


def ask(str):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": str}
        ]
    )
    print(completion.choices[0].message)


ask(input("Ask smth: "))