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
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'haru09082025'

# Dados do jogo (em memória para este exemplo simples)
games = {}
high_scores = []

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
            return redirect(url_for('snake_game'))
        else:
            flash('Login ou senha inválidos!', 'error')
            return render_template('login.html')
    
    return render_template('login.html')

@app.route('/snake_game')
def snake_game():
    """Página principal do jogo da cobrinha."""
    if not session.get('logged_in'):
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return redirect(url_for('login'))
    
    # Inicializar ou recuperar jogo do usuário
    user_id = session.get('user_id')
    if user_id not in games:
        games[user_id] = {
            'score': 0,
            'level': 1,
            'game_state': 'not_started'
        }
    
    return render_template('snake_game.html', 
                         username=session['username'],
                         high_scores=high_scores[:10])  # Top 10 scores

@app.route('/start_game', methods=['POST'])
def start_game():
    """Inicia um novo jogo."""
    if not session.get('logged_in'):
        return json.dumps({'success': False, 'message': 'Não autenticado'})
    
    user_id = session.get('user_id')
    games[user_id] = {
        'score': 0,
        'level': 1,
        'game_state': 'playing',
        'snake': [[10, 10], [10, 11], [10, 12]],  # Posição inicial da cobra
        'direction': 'up',
        'food': [random.randint(0, 19), random.randint(0, 19)],  # Comida em posição aleatória
        'timestamp': datetime.now().timestamp()
    }
    
    return json.dumps({'success': True, 'game_state': games[user_id]})

@app.route('/move_snake', methods=['POST'])
def move_snake():
    """Processa o movimento da cobra."""
    if not session.get('logged_in'):
        return json.dumps({'success': False, 'message': 'Não autenticado'})
    
    user_id = session.get('user_id')
    if user_id not in games or games[user_id]['game_state'] != 'playing':
        return json.dumps({'success': False, 'message': 'Jogo não iniciado'})
    
    data = request.get_json()
    direction = data.get('direction')
    
    # Validar direção (não pode ser oposta à atual)
    opposite_directions = {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}
    if direction and direction != opposite_directions.get(games[user_id]['direction']):
        games[user_id]['direction'] = direction
    
    # Mover a cobra
    head = games[user_id]['snake'][0].copy()
    
    if games[user_id]['direction'] == 'up':
        head[0] -= 1
    elif games[user_id]['direction'] == 'down':
        head[0] += 1
    elif games[user_id]['direction'] == 'left':
        head[1] -= 1
    elif games[user_id]['direction'] == 'right':
        head[1] += 1
    
    # Verificar colisões com as bordas
    if head[0] < 0 or head[0] >= 20 or head[1] < 0 or head[1] >= 20:
        games[user_id]['game_state'] = 'game_over'
        return json.dumps({
            'success': True, 
            'game_state': games[user_id],
            'game_over': True
        })
    
    # Verificar colisão com o próprio corpo
    if head in games[user_id]['snake']:
        games[user_id]['game_state'] = 'game_over'
        return json.dumps({
            'success': True, 
            'game_state': games[user_id],
            'game_over': True
        })
    
    # Adicionar nova cabeça
    games[user_id]['snake'].insert(0, head)
    
    # Verificar se comeu a comida
    ate_food = False
    if head == games[user_id]['food']:
        games[user_id]['score'] += 10 * games[user_id]['level']
        games[user_id]['food'] = [random.randint(0, 19), random.randint(0, 19)]
        ate_food = True
        
        # Aumentar nível a cada 50 pontos
        if games[user_id]['score'] // 50 + 1 > games[user_id]['level']:
            games[user_id]['level'] = games[user_id]['score'] // 50 + 1
    else:
        # Remover cauda se não comeu
        games[user_id]['snake'].pop()
    
    return json.dumps({
        'success': True, 
        'game_state': games[user_id],
        'ate_food': ate_food,
        'game_over': False
    })

@app.route('/save_score', methods=['POST'])
def save_score():
    """Salva a pontuação do jogador."""
    if not session.get('logged_in'):
        return json.dumps({'success': False, 'message': 'Não autenticado'})
    
    user_id = session.get('user_id')
    if user_id not in games or games[user_id]['game_state'] != 'game_over':
        return json.dumps({'success': False, 'message': 'Jogo não finalizado'})
    
    data = request.get_json()
    score = data.get('score', 0)
    
    # Adicionar à lista de highscores
    high_scores.append({
        'username': session['username'],
        'score': score,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M')
    })
    
    # Ordenar por pontuação (maior primeiro)
    high_scores.sort(key=lambda x: x['score'], reverse=True)
    
    # Manter apenas os 100 melhores scores
    while len(high_scores) > 100:
        high_scores.pop()
    
    return json.dumps({'success': True})

@app.route('/get_highscores')
def get_highscores():
    """Retorna a lista de highscores."""
    return json.dumps(high_scores[:10])

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