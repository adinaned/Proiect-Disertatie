from sqlalchemy.exc import OperationalError
from sqlalchemy import text
import os

from models import db
from routes.app_routes import create_app

app = create_app()
dump_files = ["organizations_dump.sql", "roles_dump.sql", "world_countries_dump.sql", "voting_sessions_dump.sql",
              "options_dump.sql", "users_dump.sql", "emails_dump.sql", "passwords_dump.sql",
              "profile_statuses_dump.sql"]


def execute_sql_file(filename):
    with open(filename, 'r') as f:
        sql = f.read()
        statements = sql.strip().split(';')
        for statement in statements:
            if statement.strip():
                db.session.execute(text(statement))
        db.session.commit()


def execute_all_sql_dump_files(files: list):
    dumps_dir = os.path.join(os.path.dirname(__file__), 'dumps')
    for filename in files:
        if filename.endswith('.sql'):
            filepath = os.path.join(dumps_dir, filename)
            print(f"Executing {filename}...")
            execute_sql_file(filepath)


with app.app_context():
    try:
        db.session.execute(text('SELECT 1'))
        print("DB connection was successful")
    except OperationalError as e:
        print(f"DB connection error: {str(e)}")
        exit(1)

with app.app_context():
    try:
        # db.drop_all()
        # print("DB tables dropped successfully")
        db.create_all()
        print("Tables created successfully (if they didn't exist)\n")
        try:
            execute_all_sql_dump_files(dump_files)
            print("\nSQL dump files executed successfully")
        except Exception as e:
            print(f"Error creating tables or executing SQL file: {str(e)}")
    except Exception as e:
        print(f"Error creating tables: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
