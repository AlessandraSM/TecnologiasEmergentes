from app import app, db
from models import Categoria  # se os modelos estiverem no arquivo models.py

with app.app_context():
    pratos = Categoria(nome="Pratos")
    bowls = Categoria(nome="Bowls")
    vasos = Categoria(nome="Vasos")
    
    db.session.add_all([pratos, bowls, vasos])
    db.session.commit()
    
    print("Categorias criadas com sucesso!")