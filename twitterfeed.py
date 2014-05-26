from flask import Flask, make_response, render_template

from flask import request, redirect, url_for, abort
import feedmaker

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SECRET_KEY='fddfgl3488s__sdfsdfpp33!'
)



def get_rss(user, link=False):

    if link:
        return feedmaker.get_tweets_with_links(user)
    else:
        return feedmaker.get_tweets(user)


def make_site(username, links=False):

    if username is None:
        return redirect(url_for('index'))

    response = make_response(get_rss(username, links))
    if "404" in response.status:
        abort(404)
    elif "416" in response.status:
        abort(416)
    else:
        print response.status
        response.headers['Content-Type'] = 'application/xml'
        return response


@app.route('/', methods=['GET'])
def index():
    username = request.args.get('user', None)
    if username is None:
        return render_template('index.html')

    if int(request.args.get('link', 0)) == 1:
        return redirect(url_for('getrss_links', username=username))

    return redirect(url_for('getrss', username=username))


@app.route('/<username>/')
def getrss(username):
    return make_site(username)


@app.route('/<username>/links/')
def getrss_links(username):
    return make_site(username, True)

if __name__ == '__main__':
    app.run()
