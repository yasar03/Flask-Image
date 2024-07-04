# from flask import Flask, render_template, request, jsonify
# import pandas as pd
# import sqlite3
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)

# DATABASE = 'game_data.db'

# def init_db():
#     conn = sqlite3.connect(DATABASE)
#     c = conn.cursor()
#     c.execute('''
#     CREATE TABLE IF NOT EXISTS games (
#         Unnamed INTEGER,
#         AppID INTEGER PRIMARY KEY,
#         Name TEXT,
#         ReleaseDate TEXT,
#         RequiredAge INTEGER,
#         Price REAL,
#         DLCount INTEGER,
#         AboutGame TEXT,
#         SupportedLanguages TEXT,
#         Windows BOOLEAN,
#         Mac BOOLEAN,
#         Linux BOOLEAN,
#         Positive INTEGER,
#         Negative INTEGER,
#         ScoreRank INTEGER,
#         Developers TEXT,
#         Publishers TEXT,
#         Categories TEXT,
#         Genres TEXT,
#         Tags TEXT
#     )
#     ''')
#     conn.commit()
#     conn.close()

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part in the request'}), 400
#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'error': 'No file selected'}), 400

#     if file:
#         df = pd.read_csv(file)
#         df.columns = [column.replace(' ', '') for column in df.columns] 
#         init_db()
#         conn = sqlite3.connect(DATABASE)
#         df.to_sql('games', conn, if_exists='replace', index=False)
#         conn.close()
#         return jsonify({'message': 'File successfully uploaded'}), 200

# @app.route('/query', methods=['GET'])
# def query_data():
#     filters = request.args.to_dict()
#     query = "SELECT * FROM games WHERE "

#     conditions = []
#     parameters = []
#     for key, value in filters.items():
#         if key in ['RequiredAge', 'Price', 'DLCount', 'Positive', 'Negative', 'ScoreRank']:
#             conditions.append(f"{key} = ?")
#             parameters.append(value)
#         else:
#             conditions.append(f"{key} LIKE ?")
#             parameters.append(f"%{value}%")

#     query += " AND ".join(conditions)
#     conn = sqlite3.connect(DATABASE)
#     df = pd.read_sql_query(query, conn, params=parameters)
#     conn.close()
#     return df.to_json(orient='records')

# if __name__ == '__main__':
#     init_db()
#     app.run(host='0.0.0.0', port=5000, debug=True)


from flask import Flask, render_template, request, jsonify
import pandas as pd
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATABASE = 'game_data.db'
ADMIN_PASSWORD = 'admin123'  # You can change this password as needed

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS games (
        Unnamed INTEGER,
        AppID INTEGER PRIMARY KEY,
        Name TEXT,
        ReleaseDate TEXT,
        RequiredAge INTEGER,
        Price REAL,
        DLCount INTEGER,
        AboutGame TEXT,
        SupportedLanguages TEXT,
        Windows BOOLEAN,
        Mac BOOLEAN,
        Linux BOOLEAN,
        Positive INTEGER,
        Negative INTEGER,
        ScoreRank INTEGER,
        Developers TEXT,
        Publishers TEXT,
        Categories TEXT,
        Genres TEXT,
        Tags TEXT
    )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_type = data.get('user_type')
    password = data.get('password', '')

    if user_type == 'admin' and password != ADMIN_PASSWORD:
        return jsonify({'success': False, 'message': 'Invalid password'}), 401
    return jsonify({'success': True})

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file:
        df = pd.read_csv(file)
        df.columns = [column.replace(' ', '') for column in df.columns]
        init_db()
        conn = sqlite3.connect(DATABASE)
        df.to_sql('games', conn, if_exists='replace', index=False)
        conn.close()
        return jsonify({'message': 'File successfully uploaded'}), 200

@app.route('/query', methods=['GET'])
def query_data():
    filters = request.args.to_dict()
    query = "SELECT * FROM games WHERE "

    conditions = []
    parameters = []
    for key, value in filters.items():
        if key in ['AppID','ReleaseDate', 'RequiredAge', 'Price', 'DLCount', 'Positive', 'Negative', 'ScoreRank']:
            conditions.append(f"{key} = ?")
            parameters.append(value)
        else:
            conditions.append(f"{key} LIKE ?")
            parameters.append(f"%{value}%")

    query += " AND ".join(conditions)
    conn = sqlite3.connect(DATABASE)
    df = pd.read_sql_query(query, conn, params=parameters)
    conn.close()
    return df.to_json(orient='records')

@app.route('/columns', methods=['GET'])
def get_columns():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("PRAGMA table_info(games)")
    columns = [col[1] for col in c.fetchall()]
    conn.close()
    return jsonify(columns)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)

