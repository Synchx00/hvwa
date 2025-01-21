# FIX

### Comparison and Explanation

#### Vulnerable Code:

```python
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
cursor.execute(query)
```

- **Issue**: The query string is constructed by directly embedding user inputs (`username` and `password`). This makes the application vulnerable to SQL injection, where an attacker can manipulate the input to execute arbitrary SQL commands. For example, an attacker could input `admin' OR '1'='1` as the username and any string as the password to bypass authentication.

#### Secure Code:

```python
cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
```

- **Solution**: The use of parameterized queries (also known as prepared statements) ensures that user inputs are treated as data, not as part of the SQL query. This approach prevents SQL injection by separating the SQL code from the user-provided data.