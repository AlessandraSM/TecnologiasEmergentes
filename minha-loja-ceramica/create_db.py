from app import app, db
import os

print("Banco será criado em:", os.path.abspath("produtos.db"))

with app.app_context():
    db.create_all()
    print("Banco de dados criado (ou atualizado) com sucesso!")