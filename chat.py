import time
import os

from openai import OpenAI
from dotenv import load_dotenv

JP_PROMPT_TMPL = f"""\
    あなたはアップロードされているPDFから特定の情報を抽出するための専用のアシスタントです。
    PDFの情報を参考にしながらユーザーの質問に回答してください
"""

ASSISTANT_ID = "asst_W9cokd07M1Q5VD76ziyLY8mk"


def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run


def get_answer(assistant, thread, question: str):
    newMessage = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=question,
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )
    run = wait_on_run(run, thread)
    response = client.beta.threads.messages.list(
        thread_id=thread.id, order="asc", after=newMessage.id
    )

    if response.data and response.data[0].content and len(response.data[0].content) > 0:
        return response.data[0].content[0].text.value
    else:
        raise RuntimeError("Unexpected data structure or empty response")


if __name__ == "__main__":
    load_dotenv()

    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    assistant = client.beta.assistants.retrieve(assistant_id=ASSISTANT_ID)
    thread = client.beta.threads.create()

    print("REPL mode: Type your query below. Type 'exit' to quit.")
    while True:
        query = input("Query: ")
        if query.lower() in {"exit", "quit"}:
            print("Exiting REPL. Goodbye!")
            break

        print("Completing...")
        response = get_answer(assistant, thread, query)
        print(f"Result: {response}")
