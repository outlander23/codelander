from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

app = FastAPI(title="Codelander Server", description="Lightweight C++ code completion server using outlander23/codelander")

# Load model and tokenizer at startup (cached in memory)
model_name = "outlander23/codelander"
try:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
except Exception as e:
    raise RuntimeError(f"Failed to load model: {str(e)}")

class CompletionRequest(BaseModel):
    code_prefix: str
    max_new_tokens: int = 100

@app.post("/complete")
async def complete_code(request: CompletionRequest):
    if not request.code_prefix:
        raise HTTPException(status_code=400, detail="code_prefix is required")
    
    prompt = f"complete C++ code: {request.code_prefix}"
    inputs = tokenizer(prompt, return_tensors="pt")
    
    try:
        outputs = model.generate(
            inputs.input_ids,
            max_new_tokens=request.max_new_tokens,
            temperature=0.7,
            top_p=0.9,
            do_sample=True
        )
        completion = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return {"completed_code": completion}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8345)