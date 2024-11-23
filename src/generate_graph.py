# from openai import OpenAI
# import pandas as pd

# client = OpenAI()


# def send_to_chatgpt(prompt):
#     completion = client.chat.completions.create(
#         model="gpt-4o",
#         messages=[
#             {"role": "system", "content": "You are a data analysis assistant and Python code expert."},
#             {"role": "user", "content": prompt}
#         ]
#     )
#     return completion.choices[0].message.content


# # generate graphs and save it to directory graph/ as .png
# #
# def generate_graphs(file_path, given_prompt):
#     try:
#         df = pd.read_csv(file_path)
#         print("\nFirst 5 rows of data:")
#         print(df.head())

#         prompt = f"""
#         Here is my dataset:\n\n{df.head(10).to_string(index=False)}\n\n
#         Using this dataset and this given prompt: {given_prompt}, provide Python code to generate suitable 5 graphs for data scientist salary analysis. And then save them to directory graphs/ as html
#         First **Return ONLY Python code** without any explanation, comments, or extra text. Ensure the code is ready to execute as is.
#         We already have data in pandas dataset df you NEED to use df as dataset
#         also before generating graphs, check if they need normilisation and if they do, normilize
#         use ONLY plotly
#         as code make a description of each graphic like this:


#         graphs:

#         FILENAMEOFTHEGRAPH.png: This graph represents


#         write it to the file description/descriptions_graphs.txt
#         also make a comprehensive description like data scientist and write it to the description/description.txt
#         """
#         print("\nSending to ChatGPT...")
#         gpt_response = send_to_chatgpt(prompt)
#         gpt_response = gpt_response[9:(len(gpt_response) - 4)]
#         print("\nAnswer of ChatGPT:")
#         print(gpt_response)
#         from plot import _install_dependencies
#         _install_dependencies(gpt_response)
#         exec(gpt_response)



#     except Exception as e:
#         print(f"Error: {e}")


# if __name__ == "__main__":
#     file_path = 'salary-dataset.csv'
#     given_prompt = 'Salary of data scientists'
#     generate_graphs(file_path, given_prompt)