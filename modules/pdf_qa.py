from pypdf import PdfReader
import re


def extract_pdf_text(uploaded_file):
    reader = PdfReader(uploaded_file)

    pages_text = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages_text.append(text)

    return "\n".join(pages_text)


def search_pdf_text(text, question, max_chunks=5):

    if not text.strip():
        return []

    # Normalize text for better Urdu/English searching
    text = re.sub(r"\s+", " ", text).strip()
    question = re.sub(r"\s+", " ", question).strip()

    # Split PDF into smaller chunks
    words = text.split()
    chunks = []

    chunk_size = 180

    for i in range(0, len(words), chunk_size):

        chunk = " ".join(
            words[i:i + chunk_size]
        )

        if chunk:
            chunks.append(chunk)

    # Question keywords
    question_words = set(
        question.lower().split()
    )

    scored_chunks = []

    for chunk in chunks:

        chunk_lower = chunk.lower()

        score = 0

        for word in question_words:

            if len(word) >= 2 and word in chunk_lower:
                score += 1

        if score > 0:
            scored_chunks.append(
                (score, chunk)
            )

    scored_chunks.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return [
        chunk
        for score, chunk in scored_chunks[:max_chunks]
    ]