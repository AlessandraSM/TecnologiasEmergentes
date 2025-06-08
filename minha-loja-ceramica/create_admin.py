from app import app, db
from models import Usuario

with app.app_context():
    db.create_all()
    admin = Usuario(username='admin', is_admin=True)
    admin.set_password('minhasenha')
    db.session.add(admin)
    db.session.commit()
    print("Admin criado com sucesso!")