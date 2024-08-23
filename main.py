import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

DATABASE = 'database.db'

# Conectar a DB
def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

# Criar a tabela de dados, se ainda não existir
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit() 

# Rota raiz para explicar o uso da API
@app.route('/')
def home():
    return """
    <h1>Bem vindo à API FLASK </h1>
    <p>Esta API permite que você execute operações na tabela 'dados'</p>
    <p>Rotas disponíveis</p>
    <ul>
        <li>
            POST /dados - Adiciona um novo dado. Envie um JSON com os campos 'nome' e 'idade'.
        </li>
        <li>
            GET /dados - Retorna todos os dados da tabela.
        </li>
        <li>
            GET /dados/{id} - Retorna um dado em específico.
        </li>
        <li>
            PUT /dados/{id} - Atualiza um dado existente. Envie um JSON com os campos 'nome' e 'idade'.
        </li>
        <li>
            DELETE /dados/{id} - Deleta um dado existente.
        </li>
    </ul>
    """
#region DADOS
# Rota para iniciar a DB
@app.route('/initdb')
def initialize_database():
    init_db()
    return 'Banco de dados inicializado'

# Rota para adicionar um novo dado
@app.route('/dados', methods=['POST'])
def add_dados():
    nome = request.json.get('nome')
    idade = request.json.get('idade')

    if not nome:
        return jsonify({'error': 'Nome é obrigatório'})
    if not idade:
        return jsonify({'error': 'Idade é obrigatória'})
    
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO dados (NOME, IDADE) VALUES (?, ?)', (nome, idade))
        db.commit()
        return jsonify({'message': 'Dados inseridos com sucesso'})
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

# Rota para obter todos os dados
@app.route('/dados', methods=['GET'])
def get_dados():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM dados')
        dados = cursor.fetchall()
        return jsonify([dict(row) for row in dados])
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

# Rota para obter um dado
@app.route('/dados/<int:dado_id>', methods=['GET'])
def get_dado(dado_id):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM dados WHERE id = ?', (dado_id,))
        dado = cursor.fetchone()
        if dado: 
            return jsonify(dict(dado))
        else:
            return jsonify({'error': 'ID não encontrado'})
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

# Rota para deletar um dadoteste
@app.route('/dados/<int:dado_id>', methods=['DELETE'])
def delete_dado(dado_id):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM dados WHERE id = ?', (dado_id,))
        dado = cursor.fetchone()
        if dado: 
            cursor.execute('DELETE FROM dados WHERE id = ?', (dado_id,))
            db.commit()
            return jsonify({'message': 'Dado excluído com sucesso'})
        else:
            return jsonify({'error': 'ID não encontrado'})
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

# Rota para atualizar um dado
@app.route('/dados/<int:dado_id>', methods=['PUT'])
def update_dado(dado_id):
    nome = request.json.get('nome')
    idade = request.json.get('idade')

    if not nome:
        return jsonify({'error': 'Nome é obrigatório'})
    if not idade:
        return jsonify({'error': 'Idade é obrigatória'})
    
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM dados WHERE id = ?', (dado_id,))
        dado = cursor.fetchone()
        if dado: 
            cursor.execute('UPDATE dados set nome = ?, idade = ? WHERE id = ?', (nome, idade, dado_id,))
            db.commit()
            return jsonify({'message': 'Dados alterados com sucesso!'}), 200
        else:
            return jsonify({'error': 'ID não encontrado'})
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

#endregion

@app.route('/cidades', methods=['POST', 'GET'])

def handle__cidades():
    if request.method == 'GET':
        return get_cidades()
    elif request.method == 'POST':
        return add_cidade()


def get_cidades():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM cidades')
        dados = cursor.fetchall()
        return jsonify([dict(row) for row in dados])
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

def add_cidade():
    nome_cidade = request.json.get('nome_cidade')
    uf_cidade = request.json.get('uf_cidade')

    if not nome_cidade:
        return jsonify({'error': 'Nome da cidade é obrigatório'})
    if not uf_cidade:
        return jsonify({'error': 'UF da cidade é obrigatória'})
    
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO cidades (NOME_CIDADE, UF_CIDADE) VALUES (?, ?)', (nome_cidade, uf_cidade))
        db.commit()
        return jsonify({'message': 'Dados inseridos com sucesso'})
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@app.route('/cidade/<int:cidade_id>', methods=['DELETE', 'GET', 'PUT'])

def handle_cidade(cidade_id):
    if request.method == 'GET':
        return get_cidade(cidade_id)
    elif request.method == 'DELETE':
        return delete_cidade(cidade_id)
    elif request.method == 'PUT':
        return update_cidade(cidade_id)

def get_cidade(cidade_id):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM cidades WHERE id_cidade = ?', (cidade_id,))
        id = cursor.fetchone()
        if id: 
            return jsonify(dict(id))
        else:
            return jsonify({'error': 'ID não encontrado'})
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

def delete_cidade(cidade_id):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM cidades WHERE id_cidade = ?', (cidade_id,))
        dado = cursor.fetchone()
        if dado: 
            cursor.execute('DELETE FROM cidades WHERE id_cidade = ?', (cidade_id,))
            db.commit()
            return jsonify({'message': 'Dado excluído com sucesso'})
        else:
            return jsonify({'error': 'ID não encontrado'})
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

def update_cidade(cidade_id):
    nome_cidade = request.json.get('nome_cidade')
    uf_cidade = request.json.get('uf_cidade')

    if not nome_cidade:
        return jsonify({'error': 'nome_cidade é obrigatório'})
    if not uf_cidade:
        return jsonify({'error': 'uf_cidade é obrigatória'})
    
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM cidades WHERE id_cidade = ?', (cidade_id,))
        id = cursor.fetchone()
        if id: 
            cursor.execute('UPDATE cidades set nome_cidade = ?, uf_cidade = ? WHERE id_cidade = ?', (nome_cidade, uf_cidade, cidade_id,))
            db.commit()
            return jsonify({'message': 'Dados alterados com sucesso!'}), 200
        else:
            return jsonify({'error': 'ID não encontrado'})
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

#Inicializar a aplicação FLASK
if __name__ == '__main__':
    app.run(debug=True)
