from llmconnector import connector
from sqlconnector import get_connection
from createresponse import create_response_from_llm
from logger import log_query_result
import re,json
from datetime import datetime


date_time=datetime.now() 

# datetime.today
# current_time = datetime.now().time()  # Gets current time (hours, minutes, seconds)
#print("Current time:", current_time)


def structuredAgent(user_input):

    prompt = f"""
    You are a university chatbot assistant that converts natural language questions into MySQL queries.

    Your job is to:
    - Read the user input.
    - sometimes you may get user input in json format, if so extract the user input from the json.
    - Identify if the question is about timetables, bus schedules, or café menus.
    - Analyze whether it's related to timetables, bus schedules, or café menus.
    - Convert it into a valid MySQL SELECT query.
    - Handle natural language date expressions like "today", "tomorrow", or weekdays.
    - Wrap your SQL output **only** inside <final_answer> tags. Do not add any explanations or comments.
    - user will not put ? at the end of the question. but consider every query as a question. 
    - do not use LIKE keyword in sql statement, Use '=' instead 'Like'

Database tables:

1. `timetables(course_name, lecturer_name, location, start_time, end_time, date, day_of_week)`
2. `bus_schedules(route_name, departure_location, arrival_location, departure_time, arrival_time, date, day_of_week)`
3. `cafe_menus(item_name, item_type, price, date, day_of_week)`

Instructions:
- departure_location is 'University Main Gate' if user says "main gate" or "campus" or even if user didnt mention it.
- departure_location is 'Sports Complex' if user says "campus sport center" or "rec" or "recreational center".
- arrival_locations are (Panadura,Kaduwela,Gampaha,Kadawatha,Moratuwa,Horana,Kaluthara,Athurugiriya,Pettah,Nugegoda) if the location starts with lowercase make it uppercase
- 


Mapping Rules:
- "today" → `CURRENT_DATE()`
- "tomorrow" → `CURRENT_DATE() + INTERVAL 1 DAY`
-  Weekdays like "Monday", "Tuesday" → `day_of_week = 'Monday'` etc.
-  "main gate" → `departure_location = 'University Main Gate'`
-  "campus" → `departure_location = 'University Main Gate'`
- 

Output format:
```<final_answer>[SQL_QUERY]</final_answer>```

Examples:

User: "What’s on the cafe menu today?"  
→ <final_answer>SELECT item_name, item_type, price FROM cafe_menus WHERE date = CURRENT_DATE();</final_answer>



User: "when is the bus to kadawatha arriving at the main gate?"
→ <final_answer>SELECT route_name, departure_time, arrival_time FROM bus_schedules WHERE departure_location ='University Main Gate' AND date = CURRENT_DATE() AND arrival_location='Kadawatha' ;
</final_answer>

User: "What are the bus schedules for today"
→ <final_answer>SELECT route_name, departure_time, arrival_time FROM bus_schedules WHERE departure_location ='University Main Gate' AND date = CURRENT_DATE();</final_answer>

User: "When does the bus leave from campus to Athurugiriya tomorrow?"  
→ <final_answer>SELECT route_name, departure_time, arrival_time FROM bus_schedules WHERE departure_location ='University Main Gate' AND arrival_location='Athurugiriya' AND date = CURRENT_DATE() + INTERVAL 1 DAY;</final_answer>

User: "when is the bus to Maharagama arriving at the main gate in Monday?"  
→ <final_answer>SELECT route_name, departure_time, arrival_time FROM bus_schedules WHERE departure_location ='University Main Gate' AND day_of_week='Monday' AND arrival_location='Maharagama' AND date = CURRENT_DATE() + INTERVAL 1 DAY;</final_answer>

User: "When does the bus to Kadawatha leave from the main gate on Monday?"
→ <final_answer>SELECT route_name, departure_time, arrival_time FROM bus_schedules WHERE departure_location = 'University Main Gate' AND arrival_location = 'Kadawatha' AND day_of_week = 'Monday';</final_answer>

User: "Is there a bus to Colombo Fort today?"
→ <final_answer>SELECT route_name, departure_time, arrival_time FROM bus_schedules WHERE departure_location = 'University Main Gate' AND arrival_location = 'Colombo Fort' AND date = CURRENT_DATE();</final_answer>

User: "What time is the next bus to Nugegoda from the rec?"
→ <final_answer>SELECT route_name, departure_time, arrival_time FROM bus_schedules WHERE departure_location = 'Sports Complex' AND arrival_location = 'Nugegoda' AND date = CURRENT_DATE();</final_answer>

User: "Any buses to Maharagama tomorrow?"
→ <final_answer>SELECT route_name, departure_time, arrival_time FROM bus_schedules WHERE departure_location = 'University Main Gate' AND arrival_location = 'Maharagama' AND date = CURRENT_DATE() + INTERVAL 1 DAY;</final_answer>

User: "When is the bus to Panadura arriving at the main gate on Wednesday?"
→ <final_answer>SELECT route_name, departure_time, arrival_time FROM bus_schedules WHERE departure_location = 'University Main Gate' AND arrival_location = 'Panadura' AND day_of_week = 'Wednesday';</final_answer>

User: "How can I go to Athurugiriya from the recreational center on Thursday?"
→ <final_answer>SELECT route_name, departure_time, arrival_time FROM bus_schedules WHERE departure_location = 'Sports Complex' AND arrival_location = 'Athurugiriya' AND day_of_week = 'Thursday';</final_answer>

User: "Is there a bus to Pettah on Friday from the campus?"
→ <final_answer>SELECT route_name, departure_time, arrival_time FROM bus_schedules WHERE departure_location = 'University Main Gate' AND arrival_location = 'Pettah' AND day_of_week = 'Friday';</final_answer>

User: "When does the bus to Kalutara depart on Saturday?"
→ <final_answer>SELECT route_name, departure_time, arrival_time FROM bus_schedules WHERE departure_location = 'University Main Gate' AND arrival_location = 'Kalutara' AND day_of_week = 'Saturday';</final_answer>

User: "Show me bus schedules to Moratuwa this Sunday."
→ <final_answer>SELECT route_name, departure_time, arrival_time FROM bus_schedules WHERE departure_location = 'University Main Gate' AND arrival_location = 'Moratuwa' AND day_of_week = 'Sunday';</final_answer>

User: "Do we have any buses to Kadawatha on Tuesday?"
→ <final_answer>SELECT route_name, departure_time, arrival_time FROM bus_schedules WHERE departure_location = 'University Main Gate' AND arrival_location = 'Kadawatha' AND day_of_week = 'Tuesday';</final_answer>


User: "What time is the software engineering lecture on Wednesday?"  
→ <final_answer>SELECT course_name, start_time, end_time, location FROM timetables WHERE course_name = 'software engineering' AND day_of_week = 'Wednesday';</final_answer>

Now generate the SQL query for the following user input:

"{user_input}"
    """
    print("agent called for structured question")
    response=connector(prompt)  # Call the connector function with user input
    
# Parse and extract classification
    result = response.json()
    raw_output = result.get("response", "")

# Print raw output for debugging
    # print("\n Raw LLM Output:\n", raw_output)

# Step 5: Extract <final_answer>
    match = re.search(r"<final_answer>\s*(.*?)\s*</final_answer>", raw_output, re.DOTALL | re.IGNORECASE)

    if match:
       query = match.group(1).strip()
       if not query.endswith(";"):
          query += ";" 
       print("\n✅ qery generated:✅Sending to database..")
       print(query)
       conn=get_connection()
       cursor=conn.cursor()
       cursor.execute(query)
       all_rows = cursor.fetchall()
       result_string = str(all_rows)
       
        
       if not all_rows:
        print("❌ Data NOT found in the database.")
        fallback_message = "No data found in the database."
        response = create_response_from_llm(fallback_message, user_input, query, date_time)
       else:
        print("\n✅Query Results generated from MYsqlDB:")
        response=create_response_from_llm(all_rows, user_input,query,date_time)
       

       # Step 4: Parse and extract classification
       result = response.json()
       raw_output = result.get("response", "")

      # Print raw output for debugging
      # print("\n📦Raw LLM Output:\n", raw_output)

      # Step 5: Extract <final_answer>
       match = re.search(r"<final_answer>\s*(.*?)\s*</final_answer>", raw_output, re.DOTALL | re.IGNORECASE)
       if match:
          final_answer = match.group(1).strip()
          print("\n✅Final Answer Extracted from Unstructured Agent..")
        # print(final_answer)
    else:
       print("🔴No <final_answer> tag found in the response.")
       final_answer = "Sorry, I couldn't generate a valid SQL query for your question."    
    
    expected_keywords = ["placeholder"] 
    


    log_query_result(
       user_input,
       "StructuredAgent",
       "MySQL",
       final_answer,
       result_string,
       expected_keywords,
       used_fallback=not bool(all_rows),
       success=bool(all_rows)
)

    
    return final_answer         



# Assume these values come from your processing pipeline


# structuredAgent("When is the bus to kadawatha arriving at the main gate?")