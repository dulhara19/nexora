# from sqlconnector import get_connection

# conn= get_connection()
# cursor = conn.cursor()  
# cursor.execute("SELECT * FROM bus_schedules")
# all_rows = cursor.fetchall()

# print(all_rows)
from datetime import datetime

current_time = datetime.now().time()  # Gets current time (hours, minutes, seconds)
print("Current time:", current_time)