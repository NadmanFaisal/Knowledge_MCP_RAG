import os
import asyncio
import glob
from data_cleaning.data_extractor import *
from database.database import *

PDF_DIR = 'datasets'

async def run_ingestion_pipeline():
    """
    1. Finds all PDFs in the datasets folder.
    2. Extracts text from each, cleans it, and saves it to a separate .txt file.
    3. Loads all saved text files into the vector database.
    """
    
    pdf_files = glob.glob(os.path.join(PDF_DIR, '*.pdf'))
    
    if not pdf_files:
        print(f"No PDF files found in the '{PDF_DIR}' directory.")
        return

    print(f"--- Starting Ingestion of {len(pdf_files)} PDF(s) ---")
    
    for pdf_path in pdf_files:
        base_name = os.path.basename(pdf_path)
        text_destination = os.path.join(PDF_DIR, base_name.replace('.pdf', '.txt'))
   
        raw_text = extract_text(pdf_path)
        if raw_text:
            with open(text_destination, 'w', encoding='utf-8') as outfile:
                outfile.write(raw_text)
            print(f"   -> Raw text saved to {text_destination}")
            await save_to_db(text_destination)
        
    print("\n--- Ingestion Pipeline Complete. Ready to Query. ---")

async def run_query_loop():
    # await client.delete_collection(name="my_collection")
    # await save_to_db(FILE_PATH)
    query = input("What can I help you with?\n")
    documents = await get_documents(query)
    print(documents)

async def main():
    # client = await chromadb.AsyncHttpClient(host='192.168.68.104', port=8000)
    # await client.delete_collection(name="my_collection")
    await run_ingestion_pipeline()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting RAG system.")
