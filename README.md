# oradb
Simple python class to help abstract db operations and improve portablity of code

## Usage example
```python
import oradb

db_conn = oradb.Oradb("/path/to/my/config_file.cfg")

sql_results = db_conn.execute('SELECT * FROM TEST')

for row in sql_results:
  print(row)
```
