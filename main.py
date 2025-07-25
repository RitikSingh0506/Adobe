import os
import json
import datetime
from pdf_utils import extract_sections
from ranker import rank_sections
from analyzer import analyze_subsections

INPUT_DIR = 'input'
OUTPUT_DIR = 'output'

def main():
    # Get persona and job from user (in any language; will be translated to English)
    role = input("Enter the persona role (e.g., PhD Researcher in Computational Biology): ").strip()
    job = input("Enter the job to be done (e.g., Prepare a literature review): ").strip()

    persona = {"role": role, "job": job}

    # Get PDFs from input folder
    documents = [f for f in os.listdir(INPUT_DIR) if f.endswith('.pdf')]
    metadata = {
        "input_documents": documents,
        "persona": persona["role"],
        "job_to_be_done": persona["job"],
        "timestamp": str(datetime.datetime.now(datetime.UTC))
    }

    extracted_sections = []
    refined_subsections = []

    for doc in documents:
        doc_path = os.path.join(INPUT_DIR, doc)
        result = extract_sections(doc_path, translate_always=True)
        sections = result["sections"]
        print(f"Processing '{doc}' in {result['language']}; sections: {len(sections)}")

        ranked = rank_sections(sections, persona)

        for idx, sec in enumerate(ranked):
            extracted_sections.append({
                "document": doc,
                "page_number": sec["page"],
                "section_title": sec["title"],
                "importance_rank": idx + 1
            })

            refined = analyze_subsections(doc_path, sec)
            refined_subsections.append({
                "document": doc,
                "page_number": sec["page"],
                "refined_text": refined
            })

    output = {
        "metadata": metadata,
        "extracted_sections": extracted_sections,
        "subsection_analysis": refined_subsections
    }

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    with open(os.path.join(OUTPUT_DIR, "output.json"), 'w') as f:
        json.dump(output, f, indent=2)

if __name__ == "__main__":
    main()
