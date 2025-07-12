from sqlconnector import get_connection
from llmconnector import connector

def bus_schedule_uploader(qery, ):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute(qery)
    all_rows = cursor.fetchall()