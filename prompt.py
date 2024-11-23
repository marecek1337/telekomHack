from openai import OpenAI
import openai
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import numpy
client = OpenAI()
def read_csv(file_path):
    """Зчитування CSV-файлу."""
    df = pd.read_csv(file_path)
    return df

def send_to_chatgpt(prompt):
    """Відправка запиту до ChatGPT-4."""
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a data analysis assistant and Python code expert."},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content

def main():
    # Введення шляху до набору даних
    file_path = 'salary-dataset.csv'

    try:
        # Зчитування набору даних
        df = read_csv(file_path)
        print("\nОсь перші 5 рядків набору даних:")
        print(df.head())

        given_prompt = 'Did salaries of data scientists and programmer'

        # Запит до ChatGPT
        prompt = f"""
        Here is my dataset:\n\n{df.head(10).to_string(index=False)}\n\n
        Using this dataset and this given prompt: {given_prompt}, provide Python code to generate suitable 5 graphs for data scientist salary analysis. And then save them as png 
        **Return ONLY Python code** without any explanation, comments, or extra text. Ensure the code is ready to execute as is.
        We already have data in pandas dataset df
        """
        print("\nВідправка запиту до ChatGPT...")
        gpt_response = send_to_chatgpt(prompt)
        gpt_response = gpt_response[9:(len(gpt_response)-4)]
        print("\nРекомендація ChatGPT:")
        print(gpt_response)
        exec(gpt_response)


    except Exception as e:
        print(f"Виникла помилка: {e}")

if __name__ == "__main__":
    main()
