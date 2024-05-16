from flask import Flask, render_template
import csv
import re

app = Flask(__name__)

def load_log():
    with open('data/log.csv', 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        logs = list(reader)
        date = str(logs[0][0])
        converted_date = re.sub(r'\d{4}-(\d{2})-(\d{2}) \d{2}:\d{2}:\d{2}', lambda x: f"{int(x.group(1))}月{int(x.group(2))}日", date)
        return converted_date

@app.route('/')
def index():
    date_log = load_log()
    return render_template('index.html', date=date_log)

if __name__ == '__main__':
    app.run(debug=True)
