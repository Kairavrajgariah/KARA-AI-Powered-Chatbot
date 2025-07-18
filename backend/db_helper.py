import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

cnx = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME')
)

def insert_order_item(food_item, quantity, order_id):
    try:
        cursor = cnx.cursor()
        cursor.callproc('insert_order_item', (food_item, quantity, order_id))
        cnx.commit()
        cursor.close()
        print("Order Item inserted successfully")
        return 1
    except mysql.connector.Error as err:
        print(f"Error inserting order item: {err}")
        cnx.rollback()
        return -1
    except Exception as e:
        print(f"An error occurred: {e}")
        cnx.rollback()
        return -1

def get_total_order_price(order_id):
    try:
        cursor = cnx.cursor()
        query = "SELECT get_total_order_price(%s)"
        cursor.execute(query, (order_id,))
        result = cursor.fetchone()[0]
        cursor.close()
        return result
    except Exception as e:
        print(f"Error getting total price: {e}")
        return 0

def get_next_order_id():
    try:
        cursor = cnx.cursor()
        query = 'SELECT MAX(order_id) FROM orders'
        cursor.execute(query)
        result = cursor.fetchone()[0]
        cursor.close()
        return 1 if result is None else result + 1
    except Exception as e:
        print(f"Error fetching next order ID: {e}")
        return -1

def insert_order_tracking(order_id, status):
    try:
        cursor = cnx.cursor()
        insert_query = "INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
        cursor.execute(insert_query, (order_id, status))
        cnx.commit()
        cursor.close()
    except Exception as e:
        print(f"Error inserting tracking: {e}")
        cnx.rollback()

def get_order_status(order_id: int):
    try:
        cursor = cnx.cursor()
        query = "SELECT status FROM order_tracking WHERE order_id = %s"
        cursor.execute(query, (order_id,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            return result[0]
        else:
            return None
    except Exception as e:
        print(f"Error getting order status: {e}")
        return None
