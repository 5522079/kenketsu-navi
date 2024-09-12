from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('top.html')

@app.route('/prefecture/<name>')
def prefecture_page(name):
    # クリックされた都道府県名に基づいて対応するページを表示
    # 例として、都道府県名に対応するページを表示
    return f"ここは{name}のページです"

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/nationwide')
def nationwide():
    return render_template('nationwide.html')

if __name__ == '__main__':
    app.run(debug=True)
