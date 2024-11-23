from openai import OpenAI
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

client = OpenAI()

def send_to_chatgpt(prompt):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a data analysis assistant and Python code expert."},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content

def generate_graphs(file_path, given_prompt):

    try:
        df = pd.read_csv(file_path)
        print("\nОсь перші 5 рядків набору даних:")
        print(df.head())

        prompt = f"""
        Here is my dataset:\n\n{df.head(10).to_string(index=False)}\n\n
        Using this dataset and this given prompt: {given_prompt}, provide Python code to generate suitable 5 graphs for data scientist salary analysis. And then save them to directory graphs/ as png 
        First **Return ONLY Python code** without any explanation, comments, or extra text. Ensure the code is ready to execute as is.
        We already have data in pandas dataset df you NEED to use df as dataset
        use ONLY matplotlib.pyplot as plt or seaborn as sns
        as code make a description of each graphic like this:
        We made this graph because
        We use this graph because
        , use file name for name of the graphic, sepparate by 2/n and save it in the txt file. 
        """
        print("\nSending to ChatGPT...")
        gpt_response = send_to_chatgpt(prompt)
        gpt_response = gpt_response[9:(len(gpt_response)-4)]
        print("\nРекомендація ChatGPT:")
        print(gpt_response)
        exec(gpt_response)


    except Exception as e:
        print(f"Виникла помилка: {e}")

if __name__ == "__main__":
    file_path = 'salary-dataset.csv'
    given_prompt = 'Salary of data scientists'
    generate_graphs(file_path, given_prompt)
