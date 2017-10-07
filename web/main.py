from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route("/")
def main():
    return render_template('index.html')


@app.route('/results', methods=['POST'])
def results():
    categ = request.form['categ']
    return render_template('left-sidebar.html', cat = categ)

if __name__ == "__main__":
    app.run()
