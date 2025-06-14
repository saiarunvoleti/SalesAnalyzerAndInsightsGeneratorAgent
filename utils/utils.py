from langchain.llms import Cohere
from langchain import PromptTemplate
from langchain_community.llms import HuggingFacePipeline
# from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import pandas as pd
import os
from langchain.llms import OpenAI

#public variable
COHERE_PRIVATE_KEY = "85HrfBjxabTqWkHa4ROm8y8xorxZ1rnuA3P56iBc"
MODEL_NAME = "command-r"
TEMPERATURE = 0.2

def getCohereLLM():
    # return Cohere(
    #     temperature=TEMPERATURE,
    #     cohere_api_key=COHERE_PRIVATE_KEY,
    # )
    return OpenAI(
        model="gpt-4o-mini",
        temperature=0.1 , # Adjust as needed
        openai_api_key = "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"
    )


# def getLlamaLLM():
#     # model_id = "meta-llama/Llama-2-7b-chat-hf"
#     # tokenizer = AutoTokenizer.from_pretrained(model_id)
#     # model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto")
#     # pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)
#     # llm = HuggingFacePipeline(pipeline=pipe)
#     # return llm
#     return
#
# def getSalesforceLLM():
#     model_id = "Salesforce/codegen-350M-mono"
#     tokenizer = AutoTokenizer.from_pretrained(model_id)
#     model = AutoModelForCausalLM.from_pretrained(model_id)
#     pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)
#     llm = HuggingFacePipeline(pipeline=pipe)
#     return llm

def getDataFrameObject():
    file_name = "final_corporate_sales_dataset.xlsx"
    script_dir = os.path.dirname(os.path.abspath(__file__))  # folder where script is
    file_path = os.path.join(script_dir, file_name)
    df = pd.read_excel(file_path,sheet_name='Sheet1')
    # df = pd.DataFrame()
    return df

def promptCreationForDataFrame():
    df = getDataFrameObject()
    file_name = "sales_dataset_column_descriptions.xlsx"
    script_dir = os.path.dirname(os.path.abspath(__file__))  # folder where script is
    file_path = os.path.join(script_dir, file_name)
    df_description = pd.read_excel(file_path,sheet_name='Sheet1')

    # 1. DataFrame schema: column names and dtypes
    schema_lines = [f"{col}: {dtype}" for col, dtype in df.dtypes.items()]
    schema_str = "\n".join(schema_lines)

    columns_description2 = dict(zip(df_description.iloc[:, 0], df_description.iloc[:, 1]))
    columns_description = [f"{col} : {description}" for col,description in columns_description2.items()]
    columns_description = "\n".join(columns_description)

    # 2. Top 5 rows as a markdown-style table (string)
    top5_str = df.head(2).to_markdown(index=False)

    # 3. Unique values in categorical columns
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    unique_values = {}
    for col in categorical_cols:
        unique_values[col] = df[col].dropna().unique().tolist()

    unique_str_lines = []
    for col, values in unique_values.items():
        unique_str_lines.append(f"{col}: {values}")
    unique_str = "\n".join(unique_str_lines) if unique_str_lines else "No categorical columns."

    # 4. Compose full prompt template
    prompt_template = f"""
    You are provided with a pandas DataFrame. Below are its details:

    Schema:
    {schema_str}
    
    Columns Description:
    {columns_description}

    Top 5 rows:
    {top5_str}

    
    The above lines consist of entire dataframe schema , top 5 rows , and possible values in categorical columns
    """
    return prompt_template