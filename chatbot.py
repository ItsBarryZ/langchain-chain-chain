import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# Set up the OpenAI API key
os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"

# Define the chat prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            "You are an AI playing the game of 20 Questions. Try to guess the object the user is thinking of by asking yes/no questions. You have a maximum of 20 questions."
        ),
        MessagesPlaceholder(variable_name="history"),
        HumanMessagePromptTemplate.from_template("{input}"),
    ]
)

# Initialize the chat model
llm = ChatOpenAI(temperature=0.7)

# Set up memory for the conversation
memory = ConversationBufferMemory(return_messages=True)

# Initialize the conversation chain
conversation = ConversationChain(memory=memory, prompt=prompt, llm=llm)

# Start the game
print(
    "Let's play 20 Questions! Think of an object, and I'll try to guess it by asking yes/no questions."
)
print("You can answer with 'yes', 'no', or 'exit' to end the game.")

# Counter for the number of questions asked
question_count = 0

while question_count < 20:
    question_count += 1
    response = conversation.predict(input="What is your question?")
    print(f"AI (Question {question_count}):", response)

    user_input = input("You: ").lower()
    if user_input == "exit":
        break

    response = conversation.predict(input=user_input)
    if "Is it" in response or "Is the object" in response:
        print("AI:", response)
        user_input = input("You: ").lower()
        if user_input == "yes":
            print("AI: Hooray! I guessed it correctly!")
            break
        elif user_input == "exit":
            break

if question_count == 20:
    print("AI: I couldn't guess the object within 20 questions. You win!")
