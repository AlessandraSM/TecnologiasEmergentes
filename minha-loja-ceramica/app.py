from flask import Flask, render_template, redirect, request
from models import db, Usuario, Produto, Categoria
from routes.produtos import produtos_bp
from routes.auth import auth_bp
from flask_login import LoginManager


app = Flask(__name__)
app.secret_key = 'uma_chave_secreta_qualquer'

# Configurações do banco
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///produtos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa a extensão SQLAlchemy com a app
db.init_app(app)

# Configura o Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

# Filtro de moeda para templates
def formatar_moeda_br(valor):
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
app.jinja_env.filters['moeda_br'] = formatar_moeda_br

# Carrega usuário para Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Registra os blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(produtos_bp, url_prefix='/produtos')  # Apenas uma vez!

# Rota inicial redirecionando para a home pública
@app.route('/')
def index():
    return redirect('/home')

# Rota pública que mostra os produtos sem exigir login
@app.route('/home')
def home():
    categoria_id = request.args.get('categoria', type=int)
    categorias = Categoria.query.all()

    if categoria_id:
        produtos = Produto.query.filter_by(categoria_id=categoria_id).all()
    else:
        produtos = Produto.query.all()

    return render_template('home.html', produtos=produtos, categorias=categorias, categoria_id=categoria_id)

# Inicia a aplicação
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
