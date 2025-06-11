# 🧠 Polyglot-KO FastAPI 서버

한국어 특화 LLM `heegyu/polyglot-ko-1.3b-chat`을 FastAPI를 통해 REST API 형태로 제공합니다.

---

## 📦 설치 및 실행

### 1. Python 가상환경 생성 (선택)

```bash
python -m venv venv
source venv/bin/activate        # (Linux/macOS)
venv\Scripts\activate           # (Windows)
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. 모델 다운로드 및 캐싱

모델은 다음 Hugging Face 저장소에서 자동으로 다운로드됩니다:

🔗 [heegyu/polyglot-ko-1.3b-chat](https://huggingface.co/heegyu/polyglot-ko-1.3b-chat)

설치된 `transformers`와 `torch` 라이브러리를 통해 모델이 처음 실행 시 캐싱됩니다. 인터넷 연결이 필요합니다.

### 4. 서버 실행

```bash
uvicorn app:app --host 0.0.0.0 --port 8888
```

실행 후, 아래 주소로 API 요청이 가능합니다:

```
http://localhost:8888/generate_response/
```

---

## 🔁 API 사용법

### ▶️ 엔드포인트

```
POST /generate_response/
```

### 📥 요청 예시 (test.json)

```json
{
  "content": "한국에서 가장 높은 산은 어디인가요?"
}
```

### 📤 응답 예시

```json
{
  "response": "한국에서 가장 높은 산은 한라산입니다."
}
```

### 🧪 CURL 예시

```bash
curl -X POST http://localhost:8888/generate_response/ \
  -H "Content-Type: application/json" \
  -d @test.json
```

또는 직접 데이터 입력:

```bash
curl -X POST http://localhost:8888/generate_response/ \
  -H "Content-Type: application/json" \
  -d '{"content": "AI는 어떤 원리로 동작하나요?"}'
```

---

## ⚙️ 프롬프트 구조 및 후처리

### 📌 시스템 메시지

모델에게 다음과 같은 지침을 줍니다:

```
당신은 AI 챗봇입니다. 사용자에게 도움이 되고 유익한 내용을 제공해야합니다. 답변은 짧고 명확하게 답하세요.
```

### ✂️ 출력 후처리

응답에서 "\[AI]" 이후의 텍스트를 추출한 후, 마지막 문장 종결자(`.`, `!`, `?`, `。`, `！`, `？`) 기준으로 문장을 잘라냅니다.

---

## 📁 폴더 구조

```
POLYGLOT-KO/
│
├── app.py               # FastAPI 메인 서버 코드
├── test.json            # 요청 예시 파일
├── requirements.txt     # 패키지 의존성 목록
└── heegyu/              # (모델 관련 커스텀 코드가 있다면)
```

---

## 📋 requirements.txt

```txt
fastapi
uvicorn
transformers
torch
```

※ `torch`는 GPU 사용 시, CUDA 버전에 맞는 별도 설치 권장:

```bash
pip install torch==2.1.2+cu118 -f https://download.pytorch.org/whl/torch_stable.html
```

---

## 🙋‍♂️ 문의

이 프로젝트에 대한 문의는 [github.com/heegyu](https://github.com/heegyu) 또는 직접 사용자의 레포지토리를 참고하세요.
