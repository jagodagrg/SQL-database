import sqlite3
from sqlite3 import Error


def execute_sql(conn, sql):
    """ Execute sql
    :param conn: Connection object
    :param sql: a SQL script
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)


def add_dish(conn, dish):
    """
    Create a new dish into the dishes table
    :param conn:
    :param dish:
    :return: dish id
    """
    sql = '''INSERT INTO dishes(name, deadline)
             VALUES(?,?)'''
    cur = conn.cursor()
    cur.execute(sql, dish)
    conn.commit()
    return cur.lastrowid


def add_ingredient(conn, ingredient):
    """
    Create a new ingredient into the ingredients table
    :param conn:
    :param ingredient:
    :return: ingredient id
    """
    sql = '''INSERT INTO ingredients(dish_id, name, where_to_buy, amount, already_bought)
             VALUES(?,?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, ingredient)
    conn.commit()
    return cur.lastrowid


def select_all(conn, table):
    """
    Query all rows in the table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table}")
    rows = cur.fetchall()

    return rows


def select_where(conn, table, **query):
    """
    Query tasks from table with data from **query dict
    :param conn: the Connection object
    :param table: table name
    :param query: dict of attributes and values
    :return:
    """
    cur = conn.cursor()
    qs = []
    values = ()
    for k, v in query.items():
        qs.append(f"{k}=?")
        values += (v, )
    q = " AND ".join(qs)
    cur.execute(f"SELECT * FROM {table} WHERE {q}", values)
    rows = cur.fetchall()
    return rows


def update(conn, table, id, **kwargs):
    """
    update status, begin_date, and end date of a task
    :param conn:
    :param table: table name
    :param id: row id
    :return:
    """
    parameters = [f"{k} = ?" for k in kwargs]
    parameters = ", ".join(parameters)
    values = tuple(v for v in kwargs.values())
    values += (id, )

    sql = f''' UPDATE {table}
             SET {parameters}
             WHERE id = ?'''
    try:
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
        print("Updated!")
    except sqlite3.OperationalError as e:
        print(e)


def delete_all(conn, table):
    """
    Delete all rows from table
    :param conn: Connection to the SQLite database
    :param table: table name
    :return:
    """
    sql = f'DELETE FROM {table}'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    print(f'All deleted from {table}')


def delete_where(conn, table, **kwargs):
    """
    Delete from table where attributes from
    :param conn:  Connection to the SQLite database
    :param table: table name
    :param kwargs: dict of attributes and values
    :return:
    """
    qs = []
    values = tuple()
    for k, v in kwargs.items():
        qs.append(f"{k}=?")
        values += (v,)
    q = " AND ".join(qs)

    sql = f'DELETE FROM {table} WHERE {q}'
    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()
    print('Deleted!')


if __name__ == "__main__":

    create_dishes_sql = """
   -- dishes table
   CREATE TABLE IF NOT EXISTS dishes (
      id integer PRIMARY KEY,
      name text NOT NULL,
      deadline text
   );
   """

    create_ingredients_sql = """
       -- ingredient table
   CREATE TABLE IF NOT EXISTS ingredients (
      id integer PRIMARY KEY,
      dish_id integer NOT NULL,
      name VARCHAR(250) NOT NULL,
      where_to_buy VARCHAR(250) NOT NULL,
      amount VARCHAR(250) NOT NULL,
      already_bought BOOL,
      FOREIGN KEY (dish_id) REFERENCES dishes (id)
   );
   """

    dish1 = ('uszka', '23-12-2022')
    dish2 = ('kompot z suszu', '24-12-2022')

    db_file = "my_christmas_shopping.db"

    with sqlite3.connect(db_file) as conn:
        execute_sql(conn, create_dishes_sql)
        execute_sql(conn, create_ingredients_sql)

        dish1_id = add_dish(conn, dish1)
        dish2_id = add_dish(conn, dish2)

        ingredient1 = (dish1_id, 'pieczarki', 'warzywniak', '0.5 kg', False)
        ingredient1_id = add_ingredient(conn, ingredient1)
        ingredient2 = (dish2_id, 'suszone owoce',
                       'warzywniak', '1 opakowanie', False)
        ingredient2_id = add_ingredient(conn, ingredient2)

        # tests
        #to_be_bought = select_where(conn, 'ingredients', already_bought=False)
        #print(f'Shopping list: {to_be_bought}')
        #now_bought = update(conn, 'ingredients', id=2, already_bought=True)
        #to_be_bought = select_where(conn, 'ingredients', already_bought=False)
        #print(f'Shopping list: {to_be_bought}')
        #delete_all(conn, 'ingredients')
        #delete_where(conn, 'ingredients', already_bought=True)
