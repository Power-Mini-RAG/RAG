## Apply migrations tool alembic for written by the author of SQLAlchemy. 

```bash 
cd models/db_schemes/minirag

alembic init alembic
```

### Configrations:

```bash
cp alembic.ini.example alempic.ini

```

- Update the `alembic.ini` with your database credentials (`sqlalchemy.url`)

## this connection example :
```bash
postgresql://postgres:your_password@localhost:5432/your_db_name

```

### Apply all schemes for database or create a new migration :

```bash
alembic revision --autogenerate -m "initial commit"
```

### Upgrade the database :
```bash
alembic upgrade head
```