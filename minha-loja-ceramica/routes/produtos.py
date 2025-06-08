from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Produto, Categoria
from flask_login import login_required, current_user
from flask import abort
import os
from werkzeug.utils import secure_filename
from flask import current_app

produtos_bp = Blueprint('produtos', __name__, template_folder='../templates')

def admin_required(f):
    @login_required
    def decorated(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    decorated.__name__ = f.__name__
    return decorated

@produtos_bp.route('/')
def listar():
    categoria_id = request.args.get('categoria', type=int)
    categorias = Categoria.query.all()
    
    if categoria_id:
        produtos = Produto.query.filter_by(categoria_id=categoria_id).all()
    else:
        produtos = Produto.query.all()
        
    return render_template('listar.html', produtos=produtos, categorias=categorias, categoria_id=categoria_id)

@produtos_bp.route('/cadastrar', methods=['GET', 'POST'])
@admin_required
def cadastrar():
    categorias = Categoria.query.all()  # pega todas categorias para mostrar no form
    
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        preco = request.form['preco']
        categoria_id = request.form.get('categoria_id')  # pega a categoria selecionada
        
        arquivo_imagem = request.files.get('imagem')
        if arquivo_imagem and arquivo_imagem.filename != '':
            filename = secure_filename(arquivo_imagem.filename)
            caminho_imagem = os.path.join(current_app.root_path, 'static/uploads', filename)
            arquivo_imagem.save(caminho_imagem)
        else:
            filename = None
        
        novo_produto = Produto(
            nome=nome,
            descricao=descricao,
            preco=float(preco),
            imagem=filename,
            categoria_id=int(categoria_id) if categoria_id else None
        )
        db.session.add(novo_produto)
        db.session.commit()
        flash('Produto cadastrado com sucesso!', 'success')
        return redirect(url_for('produtos.listar'))

    return render_template('cadastrar.html', categorias=categorias)

@produtos_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@admin_required
def editar(id):
    produto = Produto.query.get_or_404(id)
    categorias = Categoria.query.all()  
    
    if request.method == 'POST':
        produto.nome = request.form['nome']
        produto.descricao = request.form['descricao']
        produto.preco = float(request.form['preco'])
        
        # Atualiza a categoria selecionada (vindo do campo 'categoria' do form)
        categoria_id = request.form.get('categoria')
        if categoria_id:
            produto.categoria_id = int(categoria_id)
        
        # Se quiser tratar imagem também (se enviar)
        imagem = request.files.get('imagem')
        if imagem and imagem.filename != '':
            # Lógica para salvar a imagem aqui
            pass
        
        db.session.commit()
        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('produtos.listar'))
    
    return render_template('editar.html', produto=produto, categorias=categorias)


@produtos_bp.route('/excluir/<int:id>', methods=['POST'])
@admin_required
def excluir(id):
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    flash('Produto excluído com sucesso!', 'success')
    return redirect(url_for('produtos.listar'))


