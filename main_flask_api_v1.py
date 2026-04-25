from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Integer, Column, String
from sqlalchemy.orm import sessionmaker, declarative_base

app = Flask(__name__)

engine = create_engine("sqlite:///./test.db")
sessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True)
  email = Column(String)

Base.metadata.create_all(bind=engine)

@app.route("/", methods=["GET"])
def root():
  return jsonify({"message": "API server is running"})

@app.route("/users", methods=["GET"])
def get_users():
   db=sessionLocal()
   try:
     users = db.query(User).all()
     return jsonify([
        {"id":u.id, "email": u.email} for u in users
     ])

   finally:
      db.close()

@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):
   db =sessionLocal()
   try:
      user = db.query(User).filter(User.id == id).first()
      if not user:
         return jsonify({"message": "user not found"}), 404
      return jsonify({ "id": user.id, "email": user.email})
   finally:
      db.close()

@app.route("/users", methods=["POST"])
def create_user():
   db=sessionLocal()
   try:
      data = request.get_json()
      email = data.get('email')
      user = User(email=email)
      db.add(user)
      db.commit()
      db.refresh(user)
      return jsonify({ "id": user.id, "email": user.email})
   finally:
      db.close()

@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
   db=sessionLocal()
   try:
      user = db.query(User).filter(User.id == id).first()
      if not user:
         return jsonify({"message": "User not found"}),404
      data = request.get_json()
      print(data)
      user.email = data.get('email')
      db.commit()
      db.refresh(user)
      return jsonify({"id": user.id, "email": user.email})
   finally:
      db.close()

@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
   db=sessionLocal()
   try:
      user = db.query(User).filter(User.id == id).first()
      if not user:
         return jsonify({"message": "User not found"}),404
      db.delete(user)
      db.commit()
      return jsonify({"message": "User Deleted"})
   finally:
      db.close()
   
   
if __name__ == "__main__":
    app.run(debug=True)