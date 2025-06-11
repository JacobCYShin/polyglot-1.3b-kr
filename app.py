from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

import re

def cut_at_sentence_end(text: str):
    # 문장 끝에 해당하는 종결 문자(온점, 느낌표, 물음표 포함)
    matches = list(re.finditer(r'[.!?。？！]', text))
    if matches:
        last_end = matches[-1].end()  # 마지막 종결 기호 위치
        return text[:last_end].strip()
    else:
        return text.strip()


app = FastAPI()

model_id = "heegyu/polyglot-ko-1.3b-chat"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.float16,
    device_map="auto"
)

SYSTEM_MESSAGE = "당신은 AI 챗봇입니다. 사용자에게 도움이 되고 유익한 내용을 제공해야합니다. 답변은 짧고 명확하게 답하세요."

class UserMessage(BaseModel):
    content: str

@app.post("/generate_response/")
async def generate_response(user_message: UserMessage):
    prompt = f"""[시스템 메시지] {SYSTEM_MESSAGE}

[사용자] {user_message.content}
[AI]"""

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    input_ids = inputs["input_ids"]

    outputs = model.generate(
        input_ids=input_ids,
        max_new_tokens=512,
        do_sample=True,
        top_p=0.9,
        temperature=0.8,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.eos_token_id
    )

    output_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # "[AI]" 이후 추출
    if "[AI]" in output_text:
        raw_response = output_text.split("[AI]")[-1].strip()
    else:
        raw_response = output_text.strip()

    # ✂️ 문장 종결자 기준으로 잘라내기
    final_response = cut_at_sentence_end(raw_response)

    return {"response": final_response}
