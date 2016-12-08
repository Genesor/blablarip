# Rip O Matic
An application written in Python powered by Flask, SQLite and BambooHR.

## Usage

Modify the `src/config.ini` file


```
[main]
db_path: FULL_PATH_TO_ripomatic.db
bamboo_api: API_KEY
```

Then run the `wsgi.py` file:

```
$ py wsgi.py
```

[http://localhost:5000](http://localhost:5000)
