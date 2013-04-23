from flask import Flask, jsonify
import requests

app = Flask(__name__)
app.debug = True


@app.route('/', methods=['GET'])
def home():
    data = {
        'name': 'skein',
        'description': 'Untangling the mess that is url shortening',
        'source': 'https://github.com/problematic/skein',
        'usages': {
            '/u/:url': 'returns a JSON object containing the final url and associated metadata',
        },
    }

    return jsonify(data)


@app.route('/u/<path:url>', methods=['GET'])
def untangle(url):
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    try:
        r = requests.head(url, allow_redirects=True)
    except requests.exceptions.ConnectionError:
        return jsonify({}), 503

    data = {
        'url': r.url,
        'status_code': r.status_code,
        'history': [hop.url for hop in r.history],
    }

    return jsonify(data), 404 if r.status_code == 404 else 200


if __name__ == '__main__':
    app.run()
