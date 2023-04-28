# Standard library import
import re
import os

# Third-party library import
import requests
import argparse

# LangChain imports
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chat_models import ChatOpenAI

os.environ["OPENAI_API_KEY"] = "This is as far my easter egg skill goes"


def scrape_md_content(url: str) -> str:
    """Fetches and returns the content of a .md file from the given URL."""
    # Check if the URL points to a .md file
    if not url.endswith(".md"):
        raise ValueError("The provided URL does not point to a .md file.")

    # Fetch the content of the .md file using the requests library
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        raise ValueError(
            f"Failed to fetch the .md file. Status code: {response.status_code}"
        )
    # Extract and return the content of the .md file
    return response.text


def process_text_and_generate_docstrings(text, temperature=0.5):
    """Processes the input text, extracts code blocks, generates docstrings, summarizes documentation, and returns the result."""
    llm = OpenAI(temperature=0.5)
    # Define the prompt templates
    code_docstring_template = (
        "Generate a simple docstring for the following code:\n{code}\n"
    )
    summary_template = "Summarize the following documentation:\n{documentation}\n"

    # Use a regular expression to extract code blocks (assuming code blocks are enclosed in triple backticks)
    code_blocks = re.findall(r"```(.*?)```", text, re.DOTALL)

    # Remove code blocks from the original text to isolate the documentation
    documentation = re.sub(r"```(.*?)```", "", text, flags=re.DOTALL).strip()

    # Generate a summary for the documentation
    formatted_summary_prompt = summary_template.format(documentation=documentation)
    summary = llm(formatted_summary_prompt).strip()

    # Generate docstrings for each code block
    docstrings = []
    for code in code_blocks:
        formatted_code_prompt = code_docstring_template.format(code=code)
        docstring = llm(formatted_code_prompt).strip()
        docstrings.append(docstring)

    # Combine summary, code blocks, and docstrings
    result = [summary]
    for code, docstring in zip(code_blocks, docstrings):
        result.append(docstring)
        result.append(code)

    with open("better_documentation.txt", "w") as file:
        file.write("\n".join(result))

    return


def generate_code_from_documentation(documentation: str, user_input: str) -> str:
    """Generates code based on the provided documentation and user input."""
    # Define the chat prompt template
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                "The following is a conversation between a human and an AI. "
                "The AI has access to the following documentation:\n\n{documentation}\n\n"
                "The AI can use this documentation to generate code."
            ),
            HumanMessagePromptTemplate.from_template("{input}"),
        ]
    )

    # Initialize the chat model
    chat_model = ChatOpenAI(temperature=0.7)

    # Format the prompt with the documentation and user input

    # Convert the formatted prompt to messages and pass them to the chat model
    response = chat_model(
        prompt.format_prompt(
            documentation=documentation, input=user_input
        ).to_messages()
    )

    # Return the AI-generated code
    return response.content


def main():
    parser = argparse.ArgumentParser(description="Generate code from documentation.")
    parser.add_argument(
        "url", type=str, help="URL of the documentation (must be a .md file)."
    )
    parser.add_argument("prompt", type=str, help="User prompt for code generation.")
    args = parser.parse_args()

    file_name = "better_documentation.txt"

    # Check if the file exists
    if not os.path.exists(file_name):
        # Scrape the content of the .md file from the URL
        original_documentation = scrape_md_content(args.url)

        # Process the original documentation and generate better documentation
        process_text_and_generate_docstrings(original_documentation)

    try:
        with open("better_documentation.txt", "r") as file:
            # Read the contents of the file
            better_documentation = file.read()
    except FileNotFoundError:
        print(f"Error: better_documentation.md was not found.")

    # Generate code based on the better documentation and user prompt
    code = generate_code_from_documentation(better_documentation, args.prompt)

    # Print the generated code
    print(code)


if __name__ == "__main__":
    main()
