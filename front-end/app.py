from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    with open('/workspace/front-end/index.html', 'r') as file:
        html_content = file.read()
    return render_template_string(html_content)

if __name__ == '__main__':
    app.run(port=5000)

