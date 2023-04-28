import re
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate


def extract_code_blocks(text):
    # Use a regular expression to extract code blocks (assuming code blocks are enclosed in triple backticks)
    code_blocks = re.findall(r"```(.*?)```", text, re.DOTALL)
    return code_blocks


def generate_docstrings(code_blocks):
    # Initialize the language model
    llm = OpenAI(temperature=0.5)

    # Define the prompt template
    prompt = PromptTemplate(
        input_variables=["code"],
        template="Generate a simple docstring for the following code:\n{code}\n",
    )

    # Generate docstrings for each code block
    docstrings = []
    for code in code_blocks:
        formatted_prompt = prompt.format(code=code)
        docstring = llm(formatted_prompt).strip()
        docstrings.append(docstring)

    return docstrings


def process_text(text):
    # Extract code blocks from the input text
    code_blocks = extract_code_blocks(text)

    # Generate docstrings for each code block
    docstrings = generate_docstrings(code_blocks)

    # Combine code blocks with docstrings
    result = []
    for code, docstring in zip(code_blocks, docstrings):
        result.append(docstring)
        result.append(code)

    return "\n".join(result)
