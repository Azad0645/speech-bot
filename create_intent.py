from google.cloud import dialogflow_v2 as dialogflow
from dotenv import load_dotenv
import os
import json


def create_intent(project_id, display_name, training_phrases, message_texts):
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)

    training_phrases_objects = []
    for phrase in training_phrases:
        part = dialogflow.Intent.TrainingPhrase.Part(text=phrase)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases_objects.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases_objects,
        messages=[message],
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )
    print(f"Intent created: {response.display_name}")


if __name__ == "__main__":
    load_dotenv()

    PROJECT_ID = os.getenv("DIALOGFLOW_PROJECT_ID")

    with open("questions.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for display_name, block in data.items():
        questions = block.get("questions", [])
        answer = block.get("answer", "")

        create_intent(PROJECT_ID, display_name, questions, [answer])