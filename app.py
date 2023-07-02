import logging
import os

import dbinit
from chat import Chat
from controller import ChatController

# Configure the logging settings
logging.basicConfig(filename='debug.log', filemode='a', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    api_key = os.environ.get('GPT_API_KEY')
    print("Ask any question about Customers, Accounts and Transactions. Enter 'q' to quit. Enter 'r' to reset chat.")
    chat: Chat = Chat(api_key)
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
            print("Invalid input. Please enter a number or 'q' to quit.")


if __name__ == "__main__":
    # dbinit.init()
    main()
