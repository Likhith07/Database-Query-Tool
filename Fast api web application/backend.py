
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain import LLMChain, PromptTemplate
from langchain.llms import OpenAI
from langchain_core.output_parsers import StrOutputParser
import mysql.connector

app = FastAPI()

class QueryRequest(BaseModel):
    user_input: str

class QueryResponse(BaseModel):
    user_input: str
    sql_query: str
    result: list
    answer: str

# Setting up the MySQL connection
def connect_to_mysql():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password',
            database='classicmodels'
        )
        return conn
    except mysql.connector.Error as db_err:
        print(f"Error connecting to MySQL: {db_err}")
        return None

# Fetching our database schema
def fetch_database_schema(conn):
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        table_info = {}
        for table in tables:
            table_name = next(iter(table.values()))  # Get the table name
            cursor.execute(f"SHOW COLUMNS FROM {table_name}")
            columns = cursor.fetchall()
            table_info[table_name] = [col['Field'] for col in columns]
        
        return table_info
    except mysql.connector.Error as err:
        print(f"Error in fetching database schema: {err}")
        return None
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()

# Generating the SQL query
def generate_sql_query(user_input, table_info):
    try:
        prompt_template = """You are a helpful assistant that generates SQL queries based on user input.
        User input: {user_input}
        Generate a SQL query with respect to {table_info}:
        """
        
        prompt = PromptTemplate(input_variables=["user_input"], template=prompt_template)
        chain = LLMChain(llm=OpenAI(), prompt=prompt)
        
        sql_query = chain.run(user_input=user_input, table_info=table_info)
        
        return sql_query
    except Exception as e:
        print(f"Error generating SQL query: {e}")
        return None

# Execute SQL query
def execute_query(conn, sql_query):
    try:
        cursor = conn.cursor()
        cursor.execute(sql_query)
        result = cursor.fetchall()
        return result
    except mysql.connector.Error as err:
        print(f"Error executing query: {err}")
        return None
    finally:
        if conn and conn.is_connected():
            conn.close()

# Formating our response
def format_response(user_input, sql_query, result):
    answer_prompt = PromptTemplate.from_template(
        """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

        Question: {user_input}
        SQL Query: {sql_query}
        SQL Result: {result}
        Answer: """
    )
    llm = OpenAI()
    rephrase_answer = answer_prompt | llm | StrOutputParser()
    
    response = rephrase_answer.invoke({"user_input": user_input, "sql_query": sql_query, "result": result})
    return response




@app.post("/query", response_model=QueryResponse)
async def query_database(request: QueryRequest):
    conn = connect_to_mysql()
    if not conn:
        raise HTTPException(status_code=500, detail="Connection to MySQL failed.")
    
    table_info = fetch_database_schema(conn)
    print("table_info",table_info)
    if not table_info:
        raise HTTPException(status_code=500, detail="Failed to fetch database schema.")
    
    sql_query = generate_sql_query(request.user_input, table_info)
    if not sql_query:
        raise HTTPException(status_code=500, detail="Failed to generate SQL query.")
    
    result = execute_query(conn, sql_query)
    if result is None:
        raise HTTPException(status_code=500, detail="Failed to execute SQL query.")
    
    response = format_response(request.user_input, sql_query, result)
    
    return QueryResponse(
        user_input=request.user_input,
        sql_query=sql_query,
        result=result,
        answer=response
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="192.168.140.53", port=6090)
