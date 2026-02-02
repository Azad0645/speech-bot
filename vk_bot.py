import os
import random

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv
from dialogflow_client import detect_intent


def handle_message(event, vk_api, project_id: str):
    user_text = event.text
    vk_user_id = event.user_id
    session_id = f"vk-{vk_user_id}"

    result = detect_intent(project_id, session_id, user_text, "ru")
    reply = result.fulfillment_text
    is_fallback = result.intent.is_fallback

    if is_fallback or not reply.strip():
        return

    vk_api.messages.send(
        user_id=event.user_id,
        message=reply,
        random_id=random.randint(1, 1_000_000),
    )


def main():
    load_dotenv()

    project_id = os.getenv("DIALOGFLOW_PROJECT_ID")

    vk_session = vk.VkApi(token=os.getenv('VK_TOKEN'))
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            handle_message(event, vk_api, project_id)


if __name__ == "__main__":
    main()