# 서비스
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'aws homepage'

if __name__=='__main__':
    app.run( debug=True )
    