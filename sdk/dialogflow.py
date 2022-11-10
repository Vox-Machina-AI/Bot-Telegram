import os
from google.cloud import dialogflow
from google.protobuf.json_format import MessageToDict
from dotenv import load_dotenv


load_dotenv()
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ""


class Dialogflow:
    def __init__(self):
        self.dialogflow_agent = os.getenv('DIALOGFLOW_AGENT')

    def get_response(self, text):
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(self.dialogflow_agent, "12345678")
        text_input = dialogflow.TextInput(text=text, language_code="en-EN")
        query_input = dialogflow.QueryInput(text=text_input)
        response = session_client.detect_intent(request={"session": session, "query_input": query_input})
        intent = response.query_result.intent.display_name
        text = response.query_result.fulfillment_text
        response_json = MessageToDict(response._pb)
        args = ""
        if "image" in response_json["queryResult"]["parameters"]:
            args = response_json["queryResult"]["parameters"]["image"]
        chips = self.create_chips_menu(response)
        return intent, text, args, chips

    @staticmethod
    def create_chips_menu(response):
        chips = []
        if len(response.query_result.fulfillment_messages) >= 2:
            for i, chip in enumerate(response.query_result.fulfillment_messages[1].suggestions.suggestions):
                chips.append(chip.title)
        return chips
