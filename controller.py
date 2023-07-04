import json

from chat import Chat
from colors import RED, RESET, YELLOW, BLUE
from db import Database


class ChatController:
    def __init__(self, chat):
        self.db = Database()
        self.chat = chat

    def message(self, message, sender, counter=0):
        if counter > 4:
            return 'error: too many requests'

        response_string:str = self.chat.message(message, sender)

        try:
            response_string = response_string.replace('\n', ' ')
            response_string = response_string.replace('\r', ' ')
            response = json.loads(response_string[:-1] if response_string.endswith('.') else response_string)
        except Exception as e:
            print(f"{RED}error: {e}{RESET}")
            print(f"{RED}value error : {response_string}{RESET}")
            return self.message("Please repeat that answer but use valid JSON only.", "user", counter + 1)

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
                    case _:
                        print('error invalid action')
                        print(response)
            case _:
                print('error, invalid recipient')
                print(response)

    def reset(self):
        self.chat.reset()
        print('chat and db were reset to initial state')
