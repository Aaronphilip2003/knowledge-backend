from fastapi import FastAPI, Query, HTTPException
from datetime import datetime
from app.models import EntryCreate
from app.db import insert_entry, search_entries, fetch_candidates, get_entry_by_id,fetch_five_entries_from_db
from app.embeddings import generate_embedding
from app.search_utils import cosine_similarity
from app.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware


# Create tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/entries")
def get_entries():
    # Replace this with your database query to fetch entries
    entries = fetch_five_entries_from_db()
    return {"results": entries}

@app.post("/entries")
def create_entry(entry: EntryCreate):

    text_for_embedding = f"{entry.title}\n{entry.context}\n{entry.content}"

    embedding = generate_embedding(text_for_embedding)

    row = {
        "entry_id": entry.id,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "type": entry.type,
        "title": entry.title,
        "language": entry.language,
        "project": entry.project,
        "tags": entry.tags,
        "context": entry.context,
        "content": entry.content,
        "embedding": embedding
    }

    insert_entry(row)

    return {"status": "success"}


@app.get("/search")
def search(q: str = Query(...)):
    results = search_entries(q)

    return {
        "results": [
            {
                "entry_id": r.entry_id,
                "title": r.title,
                "type": r.type,
                "created_at": r.created_at,
            }
            for r in results
        ]
    }


@app.get("/search/hybrid")
def hybrid_search(q: str):

    query_embedding = generate_embedding(q)

    candidates = fetch_candidates(limit=500)

    results = []

    for row in candidates:

        if not row.embedding:
            continue

        semantic_score = cosine_similarity(query_embedding, row.embedding)

        keyword_score = 0
        if q.lower() in (row.title or "").lower():
            keyword_score += 0.3
        if q.lower() in (row.content or "").lower():
            keyword_score += 0.2
        if q.lower() in (row.context or "").lower():
            keyword_score += 0.1

        final_score = 0.8 * semantic_score + 0.2 * keyword_score

        if final_score >= 0.2:  # Minimum score threshold
            results.append({
                "entry_id": row.entry_id,
                "title": row.title,
                "type": row.type,
                "semantic_score": semantic_score,
                "final_score": final_score,
                "context": row.context,
            })

    results.sort(key=lambda x: x["final_score"], reverse=True)

    return {"results": results[:10]}

@app.get("/entry/{entry_id}")
def get_entry(entry_id: str):
    entry = get_entry_by_id(entry_id)  # Fetch the entry from the database using the entry_id
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    
    return {
        "entry_id": entry.entry_id,
        "title": entry.title,
        "type": entry.type,
        "content": entry.content,  # Assuming the entry has a content field
        "created_at": entry.created_at,
        "tags": entry.tags,  # Assuming the entry has tags
    }