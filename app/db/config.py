from sqlalchemy import create_engine

sesssionLocal = create_engine("sqlite:///.\db\test.db")

def get_db():
    db =
    try:
        return db
    finally:
        db.close()