"""
This application contains a Telegram bot that uses OpenAI's GPT model to generate responses and images.
"""
import os
import logging
from decimal import Decimal
from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
from logfmter import Logfmter

app = Flask(__name__, template_folder="templates")
app.secret_key = os.getenv("FLASK_SECRET_KEY")

log_to_file = os.getenv('LOG_TO_FILE', 'False') == 'True'

formatter = Logfmter(
    keys=["timestamp", "logger", "at", "process", "msq"],
    mapping={
        "timestamp": "asctime",
        "logger": "name",
        "at": "levelname",
        "process": "processName",
        "msg": "message",
    },
    datefmt="%Y-%m-%dT%H:%M:%S",
)




handler_stdout = logging.StreamHandler()
handler_stdout.setFormatter(formatter)


enabled_handlers = [handler_stdout]

if log_to_file:
    handler_file = logging.FileHandler("./logs/logfmter_user_management.log")
    handler_file.setFormatter(formatter)
    enabled_handlers.append(handler_file)


logging.basicConfig(handlers=enabled_handlers, level=logging.INFO)


logger = logging.getLogger(__name__)


def get_db_connection():
    """
    Connects to the database using the credentials from environment variables.
    Returns the connection object.
    """
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )
    return conn


@app.route("/")  # опряделяем маршрут для фунцкции def index
def index():
    """
    Renders the index page with allowed users and their balances.
    """
    conn = get_db_connection()
    cur = conn.cursor()  # сusrsor позволяет выполнять код python ,в postgres в сенсе бд
    cur.execute("SELECT user_id FROM allowed_users ORDER BY user_id")
    allowed_users = cur.fetchall()  # импортируем строки из запрос sql
    cur.execute("SELECT user_id, balance FROM user_balances")
    users_balance = cur.fetchall()  # импортируем строки из запрос sql
    cur.close()  # закрываем курсор
    conn.close()  # закрываем соединение
    return render_template(
        "index.html", allowed_users=allowed_users, users_balance=users_balance
    )  # список пользователей будем динамическими данными


@app.route("/allow", methods=["POST"])
def allow_user():
    """
    Allows a user to access the system.
    """
    user_id = request.form.get("user_id")
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT user_id FROM allowed_users WHERE user_id = %s", (user_id,))
        existing_user = cur.fetchone()
        if existing_user:
            flash(f"User {user_id} is already allowed.", "info")
        else:
            cur.execute("INSERT INTO allowed_users (user_id) VALUES (%s)", (user_id,))
            conn.commit()
            flash(f"User {user_id} has been allowed.", "success")
    finally:
        cur.close()
        conn.close()
    return redirect(url_for("index"))


@app.route("/disable", methods=["POST"])
def disable_user():
    """
    Revokes a user's access to the system.
    """
    user_id = request.form.get("user_id")
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT user_id FROM allowed_users WHERE user_id = %s", (user_id,))
        existing_user = cur.fetchone()
        if not existing_user:
            flash(f"User {user_id} is not currently allowed.", "info")
        else:
            cur.execute("DELETE FROM allowed_users WHERE user_id = %s", (user_id,))
            conn.commit()
            flash(f"User {user_id} access revoked.", "warning")
    finally:
        cur.close()
        conn.close()
    return redirect(url_for("index"))


@app.route("/add_balance", methods=["POST"])
def add_users_balance():
    """
    Adds balance to a user's account.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    user_id = request.form.get("user_id")
    balance_to_add = Decimal(request.form.get("balance_to_add", type=float))
    cur.execute("SELECT  balance  FROM user_balances where user_id = %s", (user_id,))
    current_balance = cur.fetchone()
    new_balance = current_balance[0] + balance_to_add
    cur.execute(
        "UPDATE user_balances SET balance = %s WHERE user_id = %s",
        (new_balance, user_id),
    )
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
