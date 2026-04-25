from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

app = FastAPI()

engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
sessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
# SessionLocal = sessionmaker(bind=engine)
# Base = declarative_base()

class User(Base):
  __tablename__ = "users"
  id = Column(Integer, primary_key=True)
  email = Column(String)

Base.metadata.create_all(bind=engine)

@app.post("/users")
def post_user(email: str):
  db = sessionLocal()
  user = User(email=email)
  db.add(user)
  db.commit()
  db.refresh(user)
  db.close()
  return user

@app.get("/users")
def get_users():
  db= sessionLocal()
  user = db.query(User).all()
  db.close()
  return user

@app.get("/user/id")
def get_user(id: int):
  db=sessionLocal()
  user = db.query(User).filter(User.id == id).first()
  db.close()
  return user if user else "Not Found"

@app.put("/user/id")
def update_user(id: int, email: str):
  db = sessionLocal()
  user = db.query(User).filter(User.id == id).first()
  user.email = email
  db.commit()
  db.refresh(user)
  db.close()
  return user

@app.delete("/user/id")
def delete_user(id: int):
  db = sessionLocal()
  user = db.query(User).filter(User.id == id).first()
  db.delete(user)
  db.commit()
  db.close()
  return {"message":  f"User {id} deleted"}