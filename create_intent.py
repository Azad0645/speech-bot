from google.cloud import dialogflow_v2 as dialogflow
from dotenv import load_dotenv
import os
import json
import argparse


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
    return response


def main():
    load_dotenv()

    project_id = os.getenv("DIALOGFLOW_PROJECT_ID")

    parser = argparse.ArgumentParser(
        description="Create Dialogflow intents from questions.json-like file"
    )
    parser.add_argument(
        "--questions-path",
        "-q",
        default="questions.json",
        help="Путь к JSON-файлу с вопросами и ответами (по умолчанию questions.json)",
    )
    args = parser.parse_args()
    questions_path = args.questions_path

    with open(questions_path, "r", encoding="utf-8") as f:
        intents_data = json.load(f)

    for intent_name, intent_config in intents_data.items():
        questions = intent_config.get("questions", [])
        answer = intent_config.get("answer", "")

        response = create_intent(project_id, intent_name, questions, [answer])
        print(f"Intent created: {response.display_name}")


if __name__ == "__main__":
    main()