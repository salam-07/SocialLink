from flask import Flask

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'

from sociallinkapp import routes