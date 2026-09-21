import os
import re
import math
from dotenv import load_dotenv

load_dotenv()

DOCUMENT_PATH = "rag/documents/cybersecurity_basics.txt"


def load_knowledge():
    """Load CyberShield cybersecurity knowledge."""

    if not os.path.exists(DOCUMENT_PATH):
        return []

    with open(DOCUMENT_PATH, "r", encoding="utf-8") as file:
        text = file.read()

    # Split knowledge into sections
    sections = re.split(r"\n(?=\d+\.)", text)

    return [section.strip() for section in sections if section.strip()]


def tokenize(text):
    """Convert text into simple searchable words."""

    return set(
        re.findall(r"\b[a-zA-Z0-9-]{3,}\b", text.lower())
    )


def similarity(query, document):
    """Calculate simple keyword similarity."""

    query_words = tokenize(query)
    document_words = tokenize(document)

    if not query_words or not document_words:
        return 0

    common_words = query_words.intersection(document_words)

    return len(common_words) / math.sqrt(
        len(query_words) * len(document_words)
    )


def search_knowledge(query, k=4):
    """
    Search CyberShield knowledge base
    and return the most relevant sections.
    """

    knowledge = load_knowledge()

    scored_results = []

    for section in knowledge:

        score = similarity(query, section)

        scored_results.append(
            (score, section)
        )

    scored_results.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return [
        section
        for score, section in scored_results[:k]
        if score > 0
    ]


def get_context(query, k=4):
    """Return relevant knowledge as one context string."""

    results = search_knowledge(query, k)

    if not results:
        return "No directly relevant information was found in the CyberShield knowledge base."

    return "\n\n---\n\n".join(results)