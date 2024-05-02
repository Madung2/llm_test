from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# LangChain이 지원하는 다른 채팅 모델을 사용합니다. 여기서는 Ollama를 사용합니다.
llm = ChatOllama(model="EEVE-Korean-10.8B:latest")

# Prompt 설정
prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful AI Assistant. Your name is '타샤'. You must answer in Korean unless the question is in English. You have a lovely personality.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)



# LangChain 표현식 언어 체인 구문을 사용합니다.
chain = prompt_template | llm | StrOutputParser()
