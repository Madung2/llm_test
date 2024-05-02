from fastapi import FastAPI
from fastapi.responses import RedirectResponse,  JSONResponse

from fastapi.middleware.cors import CORSMiddleware
from typing import List, Union
from langserve.pydantic_v1 import BaseModel, Field
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langserve import add_routes
from chain import chain
from chat import chain as chat_chain
from fastapi.responses import StreamingResponse
# below are for the other chains
#from translator import chain as EN_TO_KO_chain
#from llm import llm as model
#from xionic import chain as xionic_chain


app = FastAPI()

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/chat/playground")


add_routes(app, chain, path="/prompt")


class InputChat(BaseModel):
    """Input for the chat endpoint."""

    messages: List[Union[HumanMessage, AIMessage, SystemMessage]] = Field(
        ...,
        description="The chat messages representing the current conversation.",
    )
    if HumanMessage:
        print('HumanMessage: ', HumanMessage)



# @app.post("/chat/stream_log")
# async def chat_endpoint(input_chat: InputChat):
#     async def event_stream():
#         # 메시지 로그
#         for message in input_chat.messages:
#             if isinstance(message, HumanMessage):
#                 data = f"User said: {message.content}\n\n"
#                 print(data)  # 서버 콘솔에도 출력
#                 yield data
#         # chat_chain 을 호출하여 대답을 처리
#         response = await chat_chain(input_chat)
#         yield f"data: {response}\n\n"

#     return StreamingResponse(event_stream(), media_type="text/event-stream")





add_routes(
    app,
    chat_chain.with_types(input_type=InputChat),
    path="/chat",
    enable_feedback_endpoint=True,
    enable_public_trace_link_endpoint=True,
    playground_type="chat",
)

#add_routes(app, EN_TO_KO_chain, path="/translate")

#add_routes(app, model, path="/llm")

#add_routes(
#    app,
#    xionic_chain.with_types(input_type=InputChat),
 #   path="/xionic",
 #   enable_feedback_endpoint=True,
#    enable_public_trace_link_endpoint=True,
#    playground_type="chat",
#)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)