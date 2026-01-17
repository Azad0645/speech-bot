import os
import random

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv
from google.cloud import dialogflow_v2 as dialogflow


load_dotenv()

PROJECT_ID = os.getenv("DIALOGFLOW_PROJECT_ID")


def detect_intent_text(session_id: str, text: str, language_code: str = "ru") -> str:
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(PROJECT_ID, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    result = response.query_result
    fulfillment_text = result.fulfillment_text
    is_fallback = result.intent.is_fallback

    return fulfillment_text, is_fallback


def handle_message(event, vk_api):
    user_text = event.text
    session_id = str(event.user_id)

    reply, is_fallback = detect_intent_text(session_id, user_text, language_code="ru")

    if is_fallback or not reply.strip():
        return

    vk_api.messages.send(
        user_id=event.user_id,
        message=reply,
        random_id=random.randint(1, 1_000_000),
    )


if __name__ == "__main__":
    vk_session = vk.VkApi(token=os.getenv('VK_TOKEN'))
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            handle_message(event, vk_api)