# forgive me for this code. i didn't use jinja for the sake of compact.
from flask import Flask, request, redirect
from lyricsgenius import Genius

token = ""
if token == "":
    print('Enter a token first.')
    exit(1)
app = Flask(__name__)
port = 5000
g = Genius(token)

# genius handler
class genius:
    def all(name):
        url = pja.viewport() + pja.return_home() + pja.hr()
        songs = g.search_songs(name)

        for song in songs['hits']:
            url += pja.a(f'''/song/{song['result']['id']}''', song['result']['full_title']) + pja.br() + pja.br()

        return url

    def lyric(id):
        lyrics = g.lyrics(id)

        return pja.viewport() + pja.return_home() + pja.pre_lyrics(lyrics[lyrics.find('['):])

# poor man's jinja
class pja:
    def a(v=None, a=None):
        if not a:a = v
        return f'''<a href="{v}">{a}</a>'''

    def br():
        return '<br>'

    def hr():
        return '<hr>'

    def viewport():
        return '<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1" />'

    def return_home():
        return '<span style="font-size: 25px;margin-block-end: 0.1em;"><a onclick="history.back()" href="/" style="color:green">← return</a></span>'
    
    def pre_lyrics(v):
        return f'''<pre style='word-wrap: break-word;font-family: arial;'>{v}</pre>'''

# Flask
@app.errorhandler(404)
def page_not_found(e):
    return redirect('/')

@app.route("/song/<id>")
def lyrics(id):
    return genius.lyric(id)

@app.route("/")
def index():
    return '''<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1" /><center><br><br><br><h1><i style="color:green">genius</i> dot com</h1><p>for legacy devices</p><form action="/search"><input type="text" name="q" placeholder="death grips" size="30"><br><br><input type="submit" value="Submit"></form></center>'''

@app.route("/search")
def search_song():
    q = request.args.get('q')
    if q == "":return redirect("/")
    return genius.all(q)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=port)
