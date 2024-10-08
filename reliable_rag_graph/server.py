from dotenv import load_dotenv
from os import getenv
from fastapi import FastAPI, UploadFile, File
from typing import Annotated
from langserve import add_routes
from uvicorn import run

from reliable_rag_graph.graph.graph import create_graph
from reliable_rag_graph.graph.logger import get_logger
from reliable_rag_graph.utils.check_file_type import check_file_type
from reliable_rag_graph.utils.upsert_file import upsert_file
from reliable_rag_graph.utils.write_file import write_file

logger = get_logger("server")

load_dotenv()

hostname: str = getenv("SERVER_HOSTNAME", "0.0.0.0")
port: int = int(getenv("SERVER_PORT", "8000"))

app = FastAPI(
    title="Reliable RAG Graph",
    version="0.1.0",
    description="A reliable RAG implementation using langgraph",
)


@app.post("/fileupload/")
async def upload_file(file: Annotated[UploadFile, File()]):
    file_type = check_file_type(file)
    file_path = await write_file(file)
    logger.info("Writing of file succeded!")
    await upsert_file(file_path, file_type, chunk_size=300, chunk_overlap=25)



def start() -> None:
    runnable = create_graph()

    add_routes(
        app,
        runnable
    )

    run(app, host=hostname, port=port)

if __name__ == "__main__":
    start()