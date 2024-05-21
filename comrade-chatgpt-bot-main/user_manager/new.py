@app.route('/add_balance', methods=['POST'])
def add_balance():
    """
    Adds balance to a user's account.
    """
    user_id = request.form.get('user_id')
    balance_to_add = Decimal(request.form.get('balance', type=float))
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT balance FROM user_balances WHERE user_id = %s", (user_id,))
        user_balance = cur.fetchone()
        if user_balance:
            new_balance = user_balance[0] + balance_to_add
            cur.execute("UPDATE user_balances SET balance = %s WHERE user_id = %s",
                        (new_balance, user_id))
        else:
            cur.execute("INSERT INTO user_balances "
                        "(user_id, balanceimages_generated) VALUES (%s, %s, 0)",
                        (user_id, balance_to_add)), 
        conn.commit()
        flash(f"Balance updated for user {user_id}.", 'success')
    except psycopg2.Error as e:
        conn.rollback()
        flash(f"Failed to update balance for user {user_id}: {str(e)}", 'danger')
    finally:
        cur.close()
        conn.close()
    return redirect(url_for('index'))