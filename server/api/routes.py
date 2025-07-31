import base64
import json
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from services.pdf_utils import read_pdf, write_pdf
from services.inference import process_chat
from services.url_utils import extract_urls_from_text, fetch_url_content

import tempfile
import os

router = APIRouter()

@router.post("/enhance-resume/")
async def enhance_resume(
    history: str = Form(...),
    file: UploadFile = File(...)
):
    messages = json.loads(history)

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, "input.pdf")
        output_path = os.path.join(tmpdir, "enhanced_resume.pdf")

        with open(input_path, "wb") as f:
            f.write(await file.read())

        resume_text = read_pdf(input_path)

        chat_str = json.dumps(messages)
        print(chat_str)

        urls = extract_urls_from_text(chat_str + "\n" + resume_text)
        url_text = fetch_url_content(urls) if urls else ""

        print("Running inference...")
        result = process_chat(chat_str, resume_text, url_text)
        print("Inference done.")

        tool_call = result.get("tool_call")
        message = result.get("message")

        if tool_call and tool_call["name"] == "write_pdf":
            pdf_text = tool_call["arguments"]["text"]
            write_pdf(pdf_text, output_path)

            with open(output_path, "rb") as f:
                pdf_b64 = base64.b64encode(f.read()).decode("utf-8")

            return JSONResponse({
                "tool_call": tool_call,
                "message": message,
                "enhanced_resume_pdf_b64": pdf_b64,
                "filename": "enhanced_resume.pdf"
            })

        return JSONResponse({
            "error": "No valid tool call returned."
        }, status_code=400)