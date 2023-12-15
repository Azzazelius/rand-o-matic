from flask import Flask, render_template, redirect, url_for, session
from flask_socketio import SocketIO
from flask_dance.contrib.github import make_github_blueprint, github
from flask_caching import Cache
import random
import time
import os

cache = Cache()
app = Flask(__name__)
app.config['CACHE_TYPE'] = 'simple'  # включение кэша
cache.init_app(app)  # Инициилизация кэша в экземпляре Flask. Важно, строка должна идти после включения  Кэша
socketio = SocketIO(app)  # Библиотеку двустороннего обмена данных инициилизируется для экземпляра Flask


print("=============== start the project =======================")

"""
 Не сработавший код OAuth для сервера Amvera. На локальном работал.

# app.secret_key = 'Random_name_4_secret_key'
# github_blueprint = make_github_blueprint(client_id="тут мог бы быть секретный ключ",
#                                          client_secret="а тут клиентский секрет  ")
# app.register_blueprint(github_blueprint, url_prefix="/login") 

# рендер главной страницы и запрос авторизации

@app.route('/', methods=['GET'])
def main():

    try:
        if not github.authorized:
            print("Authorization required")
            return redirect(url_for("github.login"))
        else:
            account_info = github.get("/user")
            if account_info.ok:
                try:
                    print('+++++++++++++ Сохраняем сессию +++++++++++++++++')
                    session["username"] = account_info.json()
                    # print(session["username"])
                except Exception as e:
                    print('============== error: ==================', e)
                number = cache.get("number")
                print('==============', account_info, " Access granted ==============")
                return render_template('main.html', number=number)
    except Exception as e:
        return print(f"An error occurred: ", e)
"""


@app.route('/', methods=['GET'])
def main():
    try:
        number = cache.get("number")
        return render_template('main.html', number=number)
    except Exception as e:
        print('============== error: ==================\n', e)


def set_number():
    while True:
        number = random.randint(1, 20)
        cache.set('number', number)
        socketio.emit('new_number', {'number': number})
        time.sleep(5)


@socketio.on('connect')
def on_connect():
    print('Client connected')


@socketio.on('disconnect')
def on_disconnect():
    print('Client disconnected')


socketio.start_background_task(set_number)
# os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # only for local testing OAuth !!! Разрешает общение HTTP с HTTPS


if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=8080)
    except Exception as e:
        print(f"Failed to start Flask app: {str(e)}")
