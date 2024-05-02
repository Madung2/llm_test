# langserve_ollama


EEVE => 10 빌리언 정도

랭서브와 올라마를 사용해서 리모트러너블을 이용해 실제 서비스에 적용할 수 있는 형태로 만든다.

올라마: 오픈소스 LLM

랭서브: 랭체인 어플리케이션을 restapi로 배포할 수 있도록 도와주는 도구.fastapi와 pydantic을 사용해서 데이터 검증을 제공하고, 서버에 배포된 runnable을 호출할 수 있는 클라이언트도 제공한다.

랭체인: 대형 언어 모델(LLMs)을 활용하는 애플리케이션을 개발하기 위한 프레임워크

리모트러너블: LLM을 호스팅한것?!

EEVE: 야놀자에서 공개한 모델


### 기타
 
* 모델파일 :gguf 파일을 변환해서 올려주는데 사용하는 파일
* 모델파일 템플릿: 질문과 답변하는 템플릿. 올라마 깃헙에서 문법 확인 필
* 챗봇 프롬트 스타일은 chat.py에서 기본 설정 가능

### 방법
1. 올라마를 사용해서 허깅페이스로부터 EEVE를 다운받는다.
올라마를 사용하면 출력도 빠르고 쾌적한 환경에서 테스트 가능

2. 올라마를 랭서브(호스팅)에 얹어서 리모트러너블을 만든다.

3. 프롬프트, 챗봇, 리모트체인(서비스 내제화)


### 리모트 체인
리모트 러너블 체인으로 구성이 되어야 실제 서비스에 내제화 가능하다.

특정 부문에 대해 학습을 시키고 싶을 때 올라마에 해당 문서(혹은 관련된 다른 텍스트 파일등)을 로드해서 학습시킬 수 있다.
이때 문서는 작은 조각들을 나눠서 모델에 넣어야 한다. 이는 임베딩을 생성한 뒤 벡터 데이터베이스에 저장하는 방식으로 수행할 수 있다. (임베딩이란 텍스트와 같은 데이터를 수치적 형태로 변환하는 과정)
체인이란 기존 모델과 추가적으로 학습된 부분을 바느질 하듯이 연결하는것을 말한다. 
따라서 체인을 코드안에 정의 내리는 부분이 필요함.

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA

# 사용하고 싶은 파일을 로드한다.
loader = WebBaseLoader("https://www.gutenberg.org/files/1727/1727-h/1727-h.htm")
data = loader.load()

# 텍스트를 조각화 한다.
text_splitter=RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
all_splits = text_splitter.split_documents(data)

# 텍스트 조각을 벡터스토어에 임베딩 및 정장한다.
oembed = OllamaEmbeddings(base_url="http://localhost:11434", model="nomic-embed-text")
vectorstore = Chroma.from_documents(documents=all_splits, embedding=oembed)

# 체인이 완성된 ollama로 질문을 할 수 있다.
qachain=RetrievalQA.from_chain_type(ollama, retriever=vectorstore.as_retriever())
qachain.invoke({"query": question})
```

**임베딩의 기본 개념**
* 차원 축소: 임베딩은 고차원의 데이터(예: 텍스트)를 저차원의 벡터 공간으로 매핑하는 과정입니다. 이렇게 하면 복잡한 데이터를 간단하게 표현할 수 있고, 계산 효율성을 높일 수 있다.
* 의미적 유사성: 임베딩된 벡터는 비슷한 의미를 가진 단어나 문서가 벡터 공간에서 서로 가까이 위치하도록 만듭니다. 예를 들어, "왕"과 "여왕"은 임베딩 공간에서 서로 가까운 위치에 있을 것.



# 구현


### **올라마 로컬에서 EEVE 실행**

1. 올라마에서 Modelfile 형식으로 EEVE-Korean-10.8B 이미지 생성

```
$ ollama create EEVE-Korean-10.8B -f Modelfile
```

2. 올라마에서 EEVE-Korean-10.8B 이미지 실행
```
$ ollama run EEVE-Korean-10.8B:latest
```

3. 앱에서 실행
```
$ python server.py
```

>> http://127.0.0.1:8000/chat/playground/

4. 컴퓨터 서버 키기
* 내부 ip 확인: ipconfig
* 외부 ip 확인: https://www.whatismyip.com/
* 내부 방화벽 인바운드 규칙 편집
* 내부 ip랑 외부ip 포트 포워딩 : 라이터 관리 페이지 접속 >>Port Forwarding 





