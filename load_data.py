import csv
from datetime import datetime
import os
import sqlite3


def create_tables(cursor):
    create_item_table = """
    CREATE TABLE item (
        name TEXT,
        CONSTRAINT unique_item_name UNIQUE (name)
        )
    """

    create_category_table = """
    CREATE TABLE category (
        name TEXT,
        CONSTRAINT unique_category_name UNIQUE (name)
        )
    """

    create_item_category_table = """
    CREATE TABLE itemcategory (
        item TEXT, 
        category TEXT,
        FOREIGN KEY(item) REFERENCES item(name),
        FOREIGN KEY(category) REFERENCES category(name),
        CONSTRAINT unique_itemcategory UNIQUE (item, category)
        )
    """

    create_entry_table = """
    CREATE TABLE entry (
        item TEXT,
        datetime TEXT, -- "YYYY-MM-DD HH:MM:SS.SSS"
        amount REAL,
        FOREIGN KEY(item) REFERENCES item(name)
        )
    """

    create_table_statements = [
        create_item_table,
        create_category_table,
        create_item_category_table,
        create_entry_table
    ]
    for statement in create_table_statements:
        cursor.execute(statement)


def load_data(cursor):
    file_loc = '/Users/andy/Downloads/spoutdoors.csv'

    all_categories = set()
    items_and_categories = {}
    entries = []

    with open(file_loc, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            entries.append(row)
            categories = [text.strip(' ') for text in row['categories'].split(';') if text]
            all_categories.update(set(categories))
            items_and_categories[row['name']] = categories

    load_items(cursor, items_and_categories.keys())
    load_categories(cursor, all_categories)
    load_itemcategory(cursor, items_and_categories)
    load_entries(cursor, entries)


def load_items(cursor, items):
    insert_item = """INSERT INTO item VALUES (?)"""
    for item in items:
        cursor.execute(insert_item, (item.lower(),))

def load_categories(cursor, categories):
    insert_category = """INSERT INTO category VALUES (?)"""
    for category in categories:
        cursor.execute(insert_category, (category.lower(),))
        
def load_itemcategory(cursor, items_and_categories):
    insert_item_category = """INSERT INTO itemcategory VALUES (?, ?) -- item, category"""
    for item, categories in items_and_categories.items():
        for category in categories:
            cursor.execute(insert_item_category, (item.lower(), category.lower()))
            
def load_entries(cursor, entries):
    insert_entry = """INSERT INTO entry VALUES (?,?,?) -- item, datetime, amount"""
    datetime_format = '%a %b %d %H:%M:%S UTC %Y' # Sat Jul 28 15:59:00 UTC 2018
    for entry in entries:
        timestamp = datetime.strptime(entry['date'], datetime_format)
        cursor.execute(insert_entry, (entry['name'].lower(), timestamp, entry['amount']))


def delete_old_db(db_file):
    os.remove(db_file)


def main():
    db_file = './daytum.db'
    delete_old_db(db_file)
    db = sqlite3.connect(db_file)
    cursor = db.cursor()
    create_tables(cursor)
    load_data(cursor)
    db.commit()


main()
