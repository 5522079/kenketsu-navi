from flask import Flask, render_template
import csv
import re

app = Flask(__name__)

def load_log():
    with open('data/log.csv', 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        logs = list(reader)
        date = str(logs[0][0])
        update_date = re.sub(r'\d{4}-(\d{2})-(\d{2}) \d{2}:\d{2}:\d{2}', lambda x: f"{int(x.group(1))}月{int(x.group(2))}日", date)
        return update_date

def load_comment():
    with open('data/comment.txt', 'r', encoding='utf-8') as txtfile:
        comment = txtfile.read()
        return comment

@app.route('/')
def index():
    update_date = load_log()
    comment = load_comment()
    return render_template('index.html', date=update_date, content=comment)

@app.route('/aboutsite')
def aboutsite():
    return render_template('aboutsite.html')

if __name__ == '__main__':
    app.run(debug=True)
