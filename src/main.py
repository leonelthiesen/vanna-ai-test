from vanna.remote import VannaDefault
from dotenv import load_dotenv
from vanna.flask import VannaFlaskApp
import sys
import logging
import os


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

    load_dotenv()

    vanna_api_key = os.environ['VANNA_API_KEY']

    vanna_model_name = 'sqlite-sales'
    vn = VannaDefault(model=vanna_model_name, api_key=vanna_api_key)

    vn.connect_to_sqlite(os.environ['ABSOLUTE_PATH_TO_SDB'])

    train(vn)

    app = VannaFlaskApp(vn)
    app.run()

    #vn.ask(question="Qual o nome do vendedor que fez mais vendas?")

    pass

def train(vn: VannaDefault):
    df_ddl = vn.run_sql("SELECT type, sql FROM sqlite_master WHERE sql is not null")

    for ddl in df_ddl['sql'].to_list():
        vn.train(ddl=ddl)

    # The following are methods for adding training data. Make sure you modify the examples to match your database.
    # DDL statements are powerful because they specify table names, colume names, types, and potentially relationships
    # vn.train(ddl="""
    #     CREATE TABLE IF NOT EXISTS my-table (
    #         id INT PRIMARY KEY,
    #         name VARCHAR(100),
    #         age INT
    #     )
    # """)

    # Sometimes you may want to add documentation about your business terminology or definitions.
    # vn.train(documentation="Our business defines OTIF score as the percentage of orders that are delivered on time and in full")

    # You can also add SQL queries to your training data. This is useful if you have some queries already laying around. You can just copy and paste those from your editor to begin generating new SQL.
    # vn.train(sql="SELECT * FROM my-table WHERE name = 'John Doe'")

    # At any time you can inspect what training data the package is able to reference
    training_data = vn.get_training_data()
    print(training_data)

    # You can remove training data if there's obsolete/incorrect information.
    # vn.remove_training_data(id='1-ddl')

    pass


if __name__ == "__main__":
    main()