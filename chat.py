import json
import logging
import openai
from typing import List
from training import get_training_messages


class Chat:

    def __init__(self, api_key: str, model: str):
        openai.api_key = api_key
        self.model: str = model
        self.messages: List[dict] = get_training_messages().copy()

    def message(self, message: str, sender: str) -> str:
        logging.debug(message)
        if sender:
            message: str = json.dumps({'message': message, 'sender': sender})

        self.messages.append({"role": "user", "content": message})

        try:

            completion = openai.ChatCompletion.create(
                model=self.model,
                messages=self.messages
            )

            response: str = completion.choices[0].message.content
            logging.debug(response)
            self.messages.append({"role": "assistant", "content": response})

            return response
        except Exception as e:
            logging.error(e)
            return "Sorry, I don't understand you. Please try again."

    def reset(self):
        self.messages = get_training_messages().copy()
        print('model was reset to initial state')
