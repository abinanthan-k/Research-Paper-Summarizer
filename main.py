from fastapi import FastAPI, UploadFile, File, Form
import time
from services.parser import extract_text_from_pdf, split_into_chunks
from services.chain import split_summaries, prepare_final_summary
from services.closest import return_closest_indices
from services.translator import translate_text
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "Good"}

@app.post("/summarize")
async def summarize(file: UploadFile = File(...), language: str = Form(...)):
    start_time = time.time()

    # Step 1: Extract text from file
    contents = await extract_text_from_pdf(file)
    print("1. Content extracted")

    # Step 2: Split into chunks
    chunks = split_into_chunks(contents)
    print("2. Split into chunks")

    # Step 3: Select closest indices
    selected_indices = return_closest_indices(chunks)
    print("3. Selected indices")

    # Step 4: Split summaries
    summaries = split_summaries(selected_indices, chunks)
    print("4. Summaries split")

    # Step 5: Final summary preparation
    result = prepare_final_summary(summaries)
    print("5. Final summary prepared")

    result_text = translate_text(result["output_text"], language)
    print(f"6. Translated text to: {language}")

    time_taken = time.time() - start_time
    print(f"Done in {time_taken} seconds")

    return {
        "Summary": str(result_text),
        "Done in (seconds)": time_taken
    }