from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///url.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
    db.create_all()

# python Class and Database Model
class ShortUrl(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String())
    short_url = db.Column(db.String(length=3))

    def __init__(self, long_url, short_url):
        self.long_url = long_url
        self.short_url = short_url


class URLShortener:
    id = 1
    Storing_UrlId = {}
    
    def url_shortner(self, longUrl):
        if longUrl in self.Storing_UrlId:
            id = self.Storing_UrlId[longUrl]
            shorten_url = self.convereter_func(id)
        else:
            self.Storing_UrlId[longUrl] = self.id
            shorten_url = self.convereter_func(self.id)
            # Counter increment
            self.id= self.id+ 1
        
        return "www.fedoramoteproject.com/"+shorten_url

    #Converting b10 to b62(Alphanumeric)
    def convereter_func(self, id):
        b62_characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        base_len = len(b62_characters)
        stored_list = []
        while id > 0:
            val= id % base_len
            stored_list.append(b62_characters[val])
            id = id // base_len
        return "".join(stored_list[0::-1])



@app.route('/', methods=['POST', 'GET'])
def queries():
    if request.method == 'GET':
        url_received = request.form["#"]
        found_url = ShortUrl.query.all(long=url_received)
        
    return found_url(URLShortener)
