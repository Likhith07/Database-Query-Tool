SQL Query Generator with Natural Language Results

Project Overview
This project demonstrates a Python-based application utilizing the Langchain framework to generate SQL queries from user inputs, execute those queries on a MySQL database, and return the results in natural language. Additionally, the application is wrapped in a FastAPI web service, allowing users to interact with the system via a chat-based interface.

Key Features

Natural Language Input: Users input queries in natural language (e.g., "How many orders were shipped in 2003").

SQL Query Generation: The application processes the input and generates an SQL query using Langchain.

Query Execution: Executes the SQL query on the MySQL database.

Natural Language Response: Returns results in concise natural language (e.g., "There were 108 orders shipped in 2003").

Error Handling: Guides the user if any input errors occur.

FastAPI API: A REST API endpoint for streaming user queries and responses.
Example Interaction

User Input:
How many orders were shipped in 2003?

LLM Response:
There were 108 orders which were shipped in the year 2003.

Technical Stack
Python
Langchain: For natural language processing and query generation.
MySQL: For database operations.
FastAPI: For building the API.
Docker: Optional for containerization.
Deployment: The application is deployed on a cloud server.


Developed an application using Python, Langchain, and OpenAI to automate SQL query generation from user input. 
The system processes input using OpenAI models to generate SQL queries, executes them on a MySQL database, and formats the results in natural language.
It features error handling to prompt users for adjustments as needed.

Test the API:
Use any chat-based interface or cURL to send a POST request to the /query endpoint:
curl -X POST "http://localhost:8000/query" -d '{"query": "How many orders were shipped in 2003"}'

API Endpoint
POST /query
Request:
JSON Body: { "query": "Natural language question here" }

Response:
Streamed output providing the natural language response for the executed SQL query.
Ensure that the MySQL database is hosted and accessible.
