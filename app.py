from flask import Flask, render_template, request, redirect, url_for, flash, session
import database
import requests # Para a API externa

app = Flask(__name__)
app.secret_key = 'haru09082025' # Mude para uma string aleatória e segura!

# Rotas
@app.route('/')
def index():
    """Redireciona para a página de login."""
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Lida com a exibição do formulário de login e autenticação."""
    if request.method == 'POST':
        username = request.form['login']
        password = request.form['senha']

        conn = database.get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()

        if user:
            session['logged_in'] = True
            session['username'] = user['username']
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard')) # Redireciona para um dashboard após login
        else:
            flash('Login ou senha inválidos!', 'error')
            return render_template('login.html') # Mantém na página de login com erro
    return render_template('login.html') # Exibe o formulário de login (método GET)

@app.route('/dashboard')
def dashboard():
    """Página de dashboard acessível apenas após login."""
    if not session.get('logged_in'):
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return redirect(url_for('login'))

    # Exemplo de uso de uma API externa (API de fatos sobre gatos)
    cat_fact = "Não foi possível obter um fato sobre gatos."
    try:
        response = requests.get('https://catfact.ninja/fact')
        response.raise_for_status() # Lança um erro para status de erro HTTP
        data = response.json()
        cat_fact = data.get('fact', cat_fact)
    except requests.exceptions.RequestException as e:
        print(f"Erro ao consultar API de gatos: {e}")
        flash('Não foi possível carregar o fato sobre gatos no momento.', 'error')

    return render_template('dashboard.html', username=session['username'], cat_fact=cat_fact)

@app.route('/logout')
def logout():
    """Realiza o logout do usuário."""
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Certifique-se de que o banco de dados está inicializado antes de iniciar o app
    database.init_db()
    app.run(debug=True) # debug=True ativa o modo de depuração e recarrega o servidor automaticamente