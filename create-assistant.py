from openai import OpenAI
from dotenv import load_dotenv
import os

JP_PROMPT_TMPL = f"""\
    あなたはアップロードされているPDFから特定の情報を抽出するための専用のアシスタントです。
    PDFの情報を参考にしながらユーザーの質問に回答してください
"""

if __name__ == "__main__":
    load_dotenv()

    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    vector_store = client.beta.vector_stores.create(name="PDF Statements")
    file_paths = ["source/sample.pdf"]
    file_streams = [open(path, "rb") for path in file_paths]
    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id, files=file_streams
    )

    assistant = client.beta.assistants.create(
        model="gpt-3.5-turbo-1106",
        description="PDFアシスタント",
        instructions=JP_PROMPT_TMPL,
        name="PDF Assistant",
        tools=[
            {"type": "code_interpreter"},
            {"type": "file_search"},
        ],
    )
    assistant = client.beta.assistants.update(
        assistant_id=assistant.id,
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
    )
