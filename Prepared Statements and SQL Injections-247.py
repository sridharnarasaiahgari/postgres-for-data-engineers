## 1. Execute Method Placeholders ##

row_values = { 
    'identifier': 1, 
    'mail': 'adam.smith@dataquest.io',
    'name': 'Adam Smith', 
    'address': '42 Fake Street'
}
import psycopg2
conn = psycopg2.connect("dbname = dq user = dq")
cur = conn.cursor()
cur.execute("INSERT INTO users values(%(identifier)s, %(mail)s, %(name)s, %(address)s);",row_values)
conn.commit()
conn.close()


## 2. SQL Injections ##

def get_email(name):
    import psycopg2
    conn = psycopg2.connect("dbname=dq user=dq")
    cur = conn.cursor()
    # create the query string using the format function
    query_string = "SELECT email FROM users WHERE name = '" + name + "';"
    # execute the query
    cur.execute(query_string)
    res = cur.fetchall()
    conn.close()
    return res
# add you code below
all_emails = get_email("Joseph Kirby' OR 1 = 1; --")

## 3. Getting the Address ##

def get_email(name):
    import psycopg2
    conn = psycopg2.connect("dbname=dq user=dq")
    cur = conn.cursor()
    # create the query string using the format function
    query_string = "SELECT email FROM users WHERE name = '" + name + "';"
    # execute the query
    cur.execute(query_string)
    res = cur.fetchall()
    conn.close()
    return res
name = "Larry Cain' UNION SELECT address FROM users WHERE name = 'Larry Cain"
address_and_email = get_email(name)
print(address_and_email)

## 4. Avoiding SQL Injections ##

def get_email_fixed(name):
   import psycopg2
   conn = psycopg2.connect("dbname=dq user=dq")
   cur = conn.cursor()
   # fix the line below
   cur.execute("SELECT email FROM users WHERE name = %s;",(name,))
   res = cur.fetchall()
   conn.close()
   return res

## 5. Prepared Statements ##

import psycopg2
user = (10003, 'alice@dataquest.io', 'Alice', '102, Fake Street')
conn = psycopg2.connect("dbname = dq user = dq")
cur = conn.cursor()
cur.execute("PREPARE insert_user (integer, text, text, text) AS INSERT INTO users VALUES ($1, $2, $3, $4);")
cur.execute("EXECUTE insert_user(%s, %s, %s, %s);",user)


## 6. Prepared Statements Table ##

import psycopg2
conn = psycopg2.connect("dbname=dq user=dq")
cur = conn.cursor()
cur.execute("PREPARE get_email AS SELECT email FROM users WHERE name = $1;")
cur.execute("EXECUTE get_email (%s);", ('Anna Carter', ))
anna_email = cur.fetchone()
cur.execute("""
    SELECT * FROM pg_prepared_statements;
""")
print(cur.fetchall())

## 7. Runtime Gain ##

import timeit
import psycopg2
import csv
# function that inserts all users using a prepared statement
def prepared_insert():
    conn = psycopg2.connect("dbname=dq user=dq")
    cur = conn.cursor()           
    cur.execute("""
        PREPARE insert_user(integer, text, text, text) AS
        INSERT INTO users VALUES ($1, $2, $3, $4)
    """)
    for user in users:
        cur.execute("EXECUTE insert_user(%s, %s, %s, %s)", user)
    conn.close()

# function that insert all users using a new INSERT query for each user
def regular_insert():
    conn = psycopg2.connect("dbname=dq user=dq")
    cur = conn.cursor()           
    for user in users:
        cur.execute("""
            INSERT INTO users VALUES (%s, %s, %s, %s)
        """, user)
    conn.close()

# read the users into a list
users = [ ]
with open('user_accounts.csv', 'r') as file:
    next(file) # skip csv header
    reader = csv.reader(file)
    for row in reader:
        users.append(row)
# write you code here
time_prepared = timeit.timeit(prepared_insert, number = 1)
time_regular = timeit.timeit(regular_insert, number = 1)
print(time_prepared)
print(time_regular)