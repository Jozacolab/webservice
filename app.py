# from flask import Flask, render_template, request, redirect, url_for, flash, session
# import database
# import requests # Para a API externa

# app = Flask(__name__)
# app.secret_key = 'haru09082025' # Mude para uma string aleatória e segura!

# # Rotas
# @app.route('/')
# def index():
#     """Redireciona para a página de login."""
#     return redirect(url_for('login'))

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     """Lida com a exibição do formulário de login e autenticação."""
#     if request.method == 'POST':
#         username = request.form['login']
#         password = request.form['senha']

#         conn = database.get_db_connection()
#         user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
#         conn.close()

#         if user:
#             session['logged_in'] = True
#             session['username'] = user['username']
#             flash('Login realizado com sucesso!', 'success')
#             return redirect(url_for('dashboard')) # Redireciona para um dashboard após login
#         else:
#             flash('Login ou senha inválidos!', 'error')
#             return render_template('login.html') # Mantém na página de login com erro
#     return render_template('login.html') # Exibe o formulário de login (método GET)

# @app.route('/dashboard')
# def dashboard():
#     """Página de dashboard acessível apenas após login."""
#     if not session.get('logged_in'):
#         flash('Você precisa estar logado para acessar esta página.', 'warning')
#         return redirect(url_for('login'))

#     # Exemplo de uso de uma API externa (API de fatos sobre gatos)
#     cat_fact = "Não foi possível obter um fato sobre gatos."
#     try:
#         response = requests.get('https://catfact.ninja/fact')
#         response.raise_for_status() # Lança um erro para status de erro HTTP
#         data = response.json()
#         cat_fact = data.get('fact', cat_fact)
#     except requests.exceptions.RequestException as e:
#         print(f"Erro ao consultar API de gatos: {e}")
#         flash('Não foi possível carregar o fato sobre gatos no momento.', 'error')

#     return render_template('dashboard.html', username=session['username'], cat_fact=cat_fact)

# @app.route('/logout')
# def logout():
#     """Realiza o logout do usuário."""
#     session.pop('logged_in', None)
#     session.pop('username', None)
#     flash('Você foi desconectado.', 'info')
#     return redirect(url_for('login'))

# if __name__ == '__main__':
#     # Certifique-se de que o banco de dados está inicializado antes de iniciar o app
#     database.init_db()
#     app.run(debug=True) # debug=True ativa o modo de depuração e recarrega o servidor automaticamente
from flask import Flask, render_template, request, redirect, url_for, flash, session
import database
import random
from datetime import datetime, timedelta
import json

app = Flask(__name__)
app.secret_key = 'haru09082025'

# Gerar dados fictícios para o dashboard
def generate_fake_data():
    # Dados de vendas mensais
    months = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
              'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    sales_data = [random.randint(80000, 150000) for _ in range(12)]
    
    # Dados de leads por canal
    lead_channels = ['Organic Search', 'Social Media', 'Email', 'Direct', 'Referral']
    lead_data = [random.randint(100, 500) for _ in range(5)]
    
    # Dados de performance de produtos
    products = ['Produto A', 'Produto B', 'Produto C', 'Produto D', 'Produto E']
    product_performance = [random.randint(70, 100) for _ in range(5)]
    
    # Dados de métricas de negócio
    business_metrics = {
        'receita_total': random.randint(500000, 1000000),
        'crescimento_mensal': random.randint(5, 15),
        'novos_clientes': random.randint(100, 500),
        'taxa_conversao': random.randint(15, 30),
        'satisfacao_cliente': random.randint(85, 98)
    }
    
    # Dados de atividades recentes
    activities = []
    for i in range(10):
        activities.append({
            'user': f'Usuário {random.randint(1, 10)}',
            'action': random.choice(['Adicionou novo cliente', 'Atualizou estoque', 'Criou relatório', 'Realizou venda']),
            'time': (datetime.now() - timedelta(minutes=random.randint(1, 120))).strftime('%H:%M')
        })
    
    # Dados de tráfego por região
    regions = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul']
    traffic_data = [random.randint(1000, 5000) for _ in range(5)]
    
    return {
        'months': months,
        'sales_data': sales_data,
        'lead_channels': lead_channels,
        'lead_data': lead_data,
        'products': products,
        'product_performance': product_performance,
        'business_metrics': business_metrics,
        'activities': activities,
        'regions': regions,
        'traffic_data': traffic_data
    }

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
            session['user_id'] = user['id']
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login ou senha inválidos!', 'error')
            return render_template('login.html')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """Dashboard principal com dados fictícios."""
    if not session.get('logged_in'):
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return redirect(url_for('login'))
    
    data = generate_fake_data()
    
    return render_template('dashboard.html', 
                         username=session['username'],
                         data=data)

@app.route('/get_updated_metrics')
def get_updated_metrics():
    """Retorna métricas atualizadas para atualização em tempo real."""
    if not session.get('logged_in'):
        return json.dumps({'success': False, 'message': 'Não autenticado'})
    
    data = generate_fake_data()
    
    return json.dumps({
        'success': True,
        'business_metrics': data['business_metrics'],
        'sales_data': data['sales_data']
    })

@app.route('/logout')
def logout():
    """Realiza o logout do usuário."""
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('user_id', None)
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    database.init_db()
    app.run(debug=True)