from fastapi import FastAPI
from datetime import datetime
from app.models import EntryCreate
from app.bq import insert_entry
from fastapi import Query
from app.bq import search_entries
from app.embeddings import generate_embedding
from app.search_utils import cosine_similarity
from app.bq import fetch_candidates

app = FastAPI()

@app.post("/entries")
def create_entry(entry: EntryCreate):

    text_for_embedding = f"""
    Title: {entry.title}
    Context: {entry.context}
    Content: {entry.content}
    """

    embedding = generate_embedding(text_for_embedding)

    row = {
        "entry_id": entry.id,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
        "type": entry.type,
        "title": entry.title,
        "language": entry.language,
        "project": entry.project,
        "tags": entry.tags,
        "context": entry.context,
        "content": entry.content,
        "embedding": embedding
    }

    errors = insert_entry(row)

    if errors:
        return {"status": "error", "details": errors}

    return {"status": "success"}

@app.get("/search")
def search(q: str = Query(...)):
    results = search_entries(q)
    return {"results": results}

@app.get("/search/hybrid")
def hybrid_search(q: str):

    query_embedding = generate_embedding(q)

    candidates = fetch_candidates(limit=500)

    results = []

    for row in candidates:
        if not row.get("embedding"):
            continue

        semantic_score = cosine_similarity(query_embedding, row["embedding"])

        keyword_score = 0
        if q.lower() in (row["title"] or "").lower():
            keyword_score += 0.3
        if q.lower() in (row["content"] or "").lower():
            keyword_score += 0.2
        if q.lower() in (row["context"] or "").lower():
            keyword_score += 0.1

        final_score = 0.7 * semantic_score + keyword_score

        row["semantic_score"] = semantic_score
        row["final_score"] = final_score

        results.append(row)

    results.sort(key=lambda x: x["final_score"], reverse=True)

    return {"results": results[:10]}