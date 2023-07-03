import json

from chat import Chat
from db import Database

RESET = "\033[0m"

# Text colors
BLACK = "\033[0;30m"
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
BLUE = "\033[0;34m"
MAGENTA = "\033[0;35m"
CYAN = "\033[0;36m"
WHITE = "\033[0;37m"

class ChatController:
    def __init__(self, chat):
        self.db = Database()
        self.chat = chat

    def message(self, message, sender, counter=0):
        if counter > 4:
            return 'error: too many requests'
        response_string = self.chat.message(message, sender)
        try:
            response = json.loads(response_string[:-1] if response_string.endswith('.') else response_string)
        except ValueError:
            print(f"value error : {response_string}")
            return self.message("Please repeat that answer but use valid JSON only.", "SYSTEM", counter + 1)
        match response["recipient"]:
            case "USER":
                return response["message"]
            case "SERVER":
                match response["action"]:
                    case "QUERY":
                        query = response["message"]
                        print(f"{YELLOW}{query}{RESET}")
                        result = self.db.query(query)
                        print(f"{BLUE}{result}{RESET}")
                        return self.message(result, None, counter + 1)
                    case "SCHEMA":
                        result = self.db.query_schema(response["message"])
                        return self.message(result, None, counter + 1)
                    case _:
                        print('error invalid action')
                        print(response)
            case _:
                print('error, invalid recipient')
                print(response)

    def reset(self):
        self.chat.reset()
        print('chat and db were reset to initial state')