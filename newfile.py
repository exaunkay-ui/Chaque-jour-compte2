from flask import Flask, render_template_string, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "chaquejourcompte_secret"

# -----------------------------
# Base de données
# -----------------------------

def init_db():
    conn = sqlite3.connect("blog.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            contenu TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# -----------------------------
# Pages HTML
# -----------------------------

home_page = """
<h1>Chaque jour compte</h1>
<p>Motivation • Conseil • Inspiration</p>
<a href='/blog'>Voir le Blog</a><br>
<a href='/admin'>Espace Admin</a>
"""

blog_page = """
<h2>Blog Motivation</h2>
{% for post in posts %}
<h3>{{post[1]}}</h3>
<p>{{post[2]}}</p>
<hr>
{% endfor %}
<a href='/'>Retour</a>
"""

login_page = """
<h2>Connexion Admin</h2>
<form method='POST'>
Mot de passe:<br>
<input type='password' name='password'><br><br>
<button type='submit'>Se connecter</button>
</form>
"""

admin_page = """
<h2>Ajouter une publication</h2>
<form method='POST'>
Titre:<br>
<input type='text' name='titre'><br><br>
Message:<br>
<textarea name='contenu'></textarea><br><br>
<button type='submit'>Publier</button>
</form>
<a href='/logout'>Se déconnecter</a>
"""

# -----------------------------
# Routes
# -----------------------------

@app.route('/')
def home():
    return render_template_string(home_page)

@app.route('/blog')
def blog():
    conn = sqlite3.connect("blog.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts ORDER BY id DESC")
    posts = cursor.fetchall()
    conn.close()
    return render_template_string(blog_page, posts=posts)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'admin' not in session:
        return redirect('/login')

    if request.method == 'POST':
        titre = request.form['titre']
        contenu = request.form['contenu']

        conn = sqlite3.connect("blog.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO posts (titre, contenu) VALUES (?, ?)", (titre, contenu))
        conn.commit()
        conn.close()

        return redirect('/blog')

    return render_template_string(admin_page)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] == "3112":
            session['admin'] = True
            return redirect('/admin')
    return render_template_string(login_page)

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/')


if __name__ == "__main__":
    app.run()