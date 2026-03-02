from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Entry
from sqlalchemy import or_


def insert_entry(row: dict):
    db: Session = SessionLocal()

    db_entry = Entry(**row)

    db.add(db_entry)
    db.commit()
    db.close()


def search_entries(query: str, limit: int = 10):
    db: Session = SessionLocal()

    results = (
        db.query(Entry)
        .filter(
            or_(
                Entry.title.ilike(f"%{query}%"),
                Entry.content.ilike(f"%{query}%"),
                Entry.context.ilike(f"%{query}%")
            )
        )
        .order_by(Entry.created_at.desc())
        .limit(limit)
        .all()
    )

    db.close()
    return results


def fetch_candidates(limit: int = 500):
    db: Session = SessionLocal()

    results = (
        db.query(Entry)
        .order_by(Entry.created_at.desc())
        .limit(limit)
        .all()
    )

    db.close()
    return results


def get_entry_by_id(entry_id: str):
    db: Session = SessionLocal()

    entry = db.query(Entry).filter(Entry.entry_id == entry_id).first()

    db.close()
    return entry

def fetch_five_entries_from_db():
    db: Session = SessionLocal()

    results = (
        db.query(Entry)
        .order_by(Entry.created_at.desc())
        .limit(5)
        .all()
    )

    db.close()
    return results