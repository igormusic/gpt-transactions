import json
import logging
import openai

from training import get_training_messages


def load_string_from_file(file_path):
    with open(file_path, 'r') as file:
        string_data = file.read()
    return string_data


class Chat:

    def __init__(self, api_key, model):
        openai.api_key = api_key
        self.model = model
        if model[:2] == "ft":
            # pre-trained model
            self.messages = []
        else:
            # start every completion with training set + messages captured in the session
            self.messages = get_training_messages().copy()

    def message(self, message, sender):
        logging.debug(message)
        if sender:
            message = json.dumps({'message': message, 'sender': sender})

        self.messages.append({"role": "user", "content": message})

        try:

            completion = openai.ChatCompletion.create(
                model=self.model,
                messages=self.messages
            )

            response = completion.choices[0].message.content
            logging.debug(response)
            self.messages.append({"role": "assistant", "content": response})

            return response
        except Exception as e:
            logging.error(e)
            return "Sorry, I don't understand you. Please try again."

    def reset(self):
        self.messages = get_training_messages().copy()
        print('model was reset to initial state')
