import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR PASSWORD HERE",
        database="pandeyji_eatery"
    )

def get_menu_items():
    cnx = get_connection()
    cursor = cnx.cursor()
    query = "SELECT name, price FROM food_items ORDER BY name"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    cnx.close()
    return result

def insert_order_item(food_item, quantity, order_id):
    try:
        cnx = get_connection()
        cursor = cnx.cursor()
        cursor.callproc('insert_order_item', (food_item, quantity, order_id))
        cnx.commit()
        cursor.close()
        cnx.close()
        print("Order item inserted successfully!")
        return 1
    except mysql.connector.Error as err:
        print(f"Error inserting order item: {err}")
        return -1
    except Exception as e:
        print(f"An error occurred: {e}")
        return -1


def get_total_order_price(order_id):
    cnx = get_connection()
    cursor = cnx.cursor()
    query = f"SELECT get_total_order_price({order_id})"
    cursor.execute(query)
    result = cursor.fetchone()[0]
    cursor.close()
    cnx.close()
    return result


def get_next_order_id():
    cnx = get_connection()
    cursor = cnx.cursor()
    query = "SELECT MAX(order_id) FROM orders"
    cursor.execute(query)
    result = cursor.fetchone()[0]
    cursor.close()
    cnx.close()
    if result is None:
        return 1
    else:
        return result + 1


def insert_order_tracking(order_id, status):
    cnx = get_connection()
    cursor = cnx.cursor()
    insert_query = "INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
    cursor.execute(insert_query, (order_id, status))
    cnx.commit()
    cursor.close()
    cnx.close()


def get_order_status(order_id: int):
    cnx = get_connection()
    cursor = cnx.cursor()
    query = "SELECT status FROM order_tracking WHERE order_id = %s"
    cursor.execute(query, (order_id,))
    result = cursor.fetchone()
    cursor.close()
    cnx.close()
    if result is not None:
        return result[0]
    else:
        return None
