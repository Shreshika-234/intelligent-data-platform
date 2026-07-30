import sqlite3
import pandas as pd


conn = sqlite3.connect("data/books.db")
cursor = conn.cursor()


# save quaries and output to a data/query_result.txt
def execute_and_save(file, query_name, query):
    cursor.execute(query)
    rows = cursor.fetchall()

    # Print to terminal
    print(f"\n{query_name}")
    print(query.strip())

    for row in rows:
        print(row)

    # Save query and output
    file.write(f"\n{query_name}\n")
    file.write("=" * 60 + "\n")
    file.write(query.strip() + "\n\n")

    for row in rows:
        file.write(str(row) + "\n")


query1 = """Select book_id,title,rating 
from books 
where rating >= 3"""


query2 = """
SELECT book_id, title, price_inr
FROM books
ORDER BY price_inr DESC
LIMIT 10
"""


query3 = """
SELECT DISTINCT rating
FROM books
ORDER BY rating
"""


query4 = """
SELECT title, price_gbp
FROM books
WHERE price_gbp BETWEEN 20 AND 30
ORDER BY price_gbp DESC
"""


query5 = """
SELECT
    b.title,
    b.price_inr,
    b.rating,
    c.category_name
FROM books b
LEFT JOIN categories c
    ON b.category_id = c.category_id
ORDER BY b.rating DESC, b.book_id ASC
LIMIT 10
"""


with open("data/query_results.txt", "w", encoding="utf-8") as file:

    execute_and_save(file, "QUERY 1 - Three to Five star books", query1)
    execute_and_save(file, "QUERY 2 - 10 most expensive books", query2)
    execute_and_save(file, "QUERY 3 - Distinct ratings", query3)
    execute_and_save(
        file,
        "QUERY 4 - Books priced between GBP 20 and GBP 30",
        query4
    )
    execute_and_save(
        file,
        "QUERY 5 - Top-rated books with categories",
        query5
    )

print("\nQueries and outputs saved to data/query_results.txt")


# sql to pandas
print("="*50,"SQL to PANDAS Quaries","="*50)
query1_df = pd.read_sql(query1,conn)
print("\nQuery 1 using pd.read_sql:")
print(query1_df)

query5_df = pd.read_sql(query5,conn)
print("\nQuery 5 using pd.read_sql:")
print(query5_df)

sql_join_df = query5_df.reset_index(drop=True)

# join using pandas

books_df = pd.read_sql("Select * from books",conn)
categories_df = pd.read_sql("Select * from categories",conn)

# join query with pandas merge
merged_df = pd.merge(books_df,categories_df,how="left",on="category_id")

# select the same rows as sql query5 selected
merged_result = (merged_df.sort_values(["rating", "book_id"],ascending=[False, True]).head(10)
    [["title", "price_inr", "rating", "category_name"]].reset_index(drop=True))


# both produces equal output
print("\nResults match:",sql_join_df.equals(merged_result))


with open("data/query_results.txt", "a", encoding="utf-8") as file:
    file.write("\n\nSQL JOIN VS PANDAS MERGE\n")
    file.write("=" * 60 + "\n")

    file.write("\nSQL JOIN result using pd.read_sql():\n")
    file.write(sql_join_df.to_string(index=False))

    file.write("\n\nPandas pd.merge() result:\n")
    file.write(merged_result.to_string(index=False))

    file.write(
        f"\n\nResults match: {sql_join_df.equals(merged_result)}\n"
    )



conn.close()