import logging
import os

import dbinit
from chat import Chat
from controller import ChatController

# Configure the logging settings
logging.basicConfig(filename='debug.log', filemode='a', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def main():

    api_key = os.environ.get('OPENAI_API_KEY')
    model = os.environ.get('OPEN_AI_MODEL')
    print("Ask any question about Customers, Accounts and Transactions. Enter 'q' to quit. Enter 'r' to reset chat.")
    chat: Chat = Chat(api_key=api_key, model=model)
    controller = ChatController(chat)
    while True:
        user_input = input("Question: ")
        if user_input.lower() == 'q':
            break
        if user_input == "r":
            controller.reset()
            continue
        try:
            result = controller.message(message=user_input, sender="USER")
            print(f"ChatGPT: {result}")
        except ValueError:
            print("Invalid input. Please enter question or 'q' to quit.")


if __name__ == "__main__":
    dbinit.init()
    main()
