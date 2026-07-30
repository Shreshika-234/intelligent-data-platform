# Module 1 — Data Pipeline

## Overview

This module implements an end-to-end data pipeline using book data from Books to Scrape, a public website designed for web-scraping practice.

The pipeline performs the following steps:

1. Scrapes book data using `requests` and `BeautifulSoup`.
2. Stores the scraped data in `data/raw_books.csv`.
3. Cleans and transforms the data using pandas.
4. Converts book prices from GBP to INR using the project-defined fixed conversion rate of **1 GBP = 105.50 INR**.
5. Stores the cleaned data in `data/clean_books.csv`.
6. Loads the cleaned data into a normalized SQLite database.
7. Executes SQL queries covering the required SQL operations.
8. Reads SQL query results into pandas DataFrames.
9. Reproduces the SQL join using `pd.merge()` and verifies that both approaches produce equivalent results.

The final dataset contains **108 books across 8 categories**.

---

## Project Structure

```text
data_pipeline/
│
├── scraper.py
├── clean.py
├── database.ipynb
├── queries.py
├── requirements.txt
├── README.md
│
└── data/
    ├── raw_books.csv
    ├── clean_books.csv
    ├── books.db
    └── query_results.txt
```

### Files

- `scraper.py` — Scrapes book data from Books to Scrape.
- `clean.py` — Cleans and transforms the scraped data.
- `database.ipynb` — Creates the normalized SQLite database and loads the cleaned data.
- `queries.py` — Executes SQL queries, reads query results into pandas, performs the pandas merge, and compares the SQL and pandas results.
- `requirements.txt` — Contains the Python dependencies required for this module.
- `data/raw_books.csv` — Raw data produced by the scraper.
- `data/clean_books.csv` — Cleaned and transformed dataset.
- `data/books.db` — SQLite database containing the normalized tables.
- `data/query_results.txt` — Saved SQL queries, query outputs, and SQL JOIN vs pandas merge comparison.

---

## Setup

This project uses a **separate `requirements.txt` for each module**.

Navigate to the Data Pipeline module:

```bash
cd data_pipeline
```

Create a virtual environment if required:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

### Dependencies

The Data Pipeline module uses:

```text
requests
beautifulsoup4
pandas==2.3.3
```

`sqlite3` is part of the Python standard library, so no separate SQLite package is required.

---

# Running the Module

Run the pipeline in the following order.

## Step 1 — Scrape the Data

Run:

```bash
python3 scraper.py
```

This scrapes the selected book categories and creates:

```text
data/raw_books.csv
```

## Step 2 — Clean and Transform the Data

Run:

```bash
python3 clean.py
```

This cleans the scraped data, converts the required columns into appropriate types, performs the fixed GBP-to-INR conversion, and creates:

```text
data/clean_books.csv
```

## Step 3 — Create and Populate the SQLite Database

Open:

```text
database.ipynb
```

in Jupyter Notebook, JupyterLab, or VS Code and run all cells from top to bottom.

The notebook creates and populates the normalized SQLite database:

```text
data/books.db
```

with the following tables:

```text
categories
books
```

## Step 4 — Execute SQL Queries and pandas Analysis

Run:

```bash
python3 queries.py
```

This executes the required SQL queries, reads SQL results into pandas, reproduces the SQL join using `pd.merge()`, compares the two approaches, and saves the results to:

```text
data/query_results.txt
```

## Complete Pipeline Flow

```text
Books to Scrape
       |
       v
   scraper.py
       |
       v
raw_books.csv
       |
       v
    clean.py
       |
       v
clean_books.csv
       |
       v
 database.ipynb
       |
       v
    books.db
       |
       v
   queries.py
       |
       v
query_results.txt
```

---

# 1. Web Scraping

## Data Source

The data is collected from Books to Scrape, a public website created for web-scraping practice.

The scraper uses:

- `requests` to retrieve HTML pages.
- `BeautifulSoup` to parse the HTML and extract book information.

The following 8 categories are scraped:

- Travel
- Music
- Art
- Horror
- History
- Health
- Food and Drink
- Religion

All books listed in the selected categories are collected, including paginated category pages where applicable.

The final scraped dataset contains:

```text
108 books
8 categories
```

This exceeds the requirement of at least 60 books across at least 3 categories.

## Scraped Fields

For each book, the scraper collects:

- `title`
- `price`
- `star_rating`
- `availability`
- `category`

Example raw values:

```text
title        = It's Only the Himalayas
price        = £45.17
star_rating  = Two
availability = In stock
category     = Travel
```

The scraped data is stored in:

```text
data/raw_books.csv
```

Keeping the raw data separately allows the cleaning and database stages to be rerun without requiring another scraping request.

---

# 2. Data Cleaning and Transformation

The raw dataset is loaded into pandas and cleaned in `clean.py`.

## Price Cleaning

The original `price` field contains the GBP currency symbol.

Example:

```text
£45.17
```

The currency symbol is removed and the value is converted into the numeric `price_gbp` column.

```text
£45.17 -> 45.17
```

`price_gbp` is stored as a floating-point value.

---

## Rating Conversion

The scraped star rating is represented as text.

The following mapping is used:

```text
One   -> 1
Two   -> 2
Three -> 3
Four  -> 4
Five  -> 5
```

A new `rating` column is created from `star_rating`.

The resulting `rating` values are integers between 1 and 5.

---

## Availability Conversion

The scraped availability text is converted into a boolean `in_stock` column.

For example:

```text
In stock -> True
```

The cleaned pandas DataFrame therefore stores `in_stock` as a boolean:

```text
True / False
```

When the data is inserted into SQLite, the boolean is represented as an integer:

```text
True  -> 1
False -> 0
```

Therefore:

```text
Scraped value      pandas          SQLite
------------------------------------------------
In stock           True            1
Not in stock       False           0
```

The cleaned pandas data uses boolean values, while the SQLite database uses their integer representation.

---

## Handling Parsing Failures and Missing Values

The cleaning pipeline handles unexpected or invalid values instead of allowing them to crash the pipeline.

For numeric fields, safe numeric conversion is used so values that cannot be parsed become missing values.

Numeric parsing failures in:

- `price_gbp`
- `rating`

are handled using median imputation.

The median is calculated from the successfully parsed values and used to replace invalid or missing numeric values.

Rows missing essential fields such as:

- `title`
- `category`

are dropped because these values identify or classify the book and cannot be reliably reconstructed.

This allows the pipeline to handle malformed data without failing.

---

# 3. GBP to INR Conversion

A new `price_inr` column is calculated from `price_gbp`.

The required project-defined fixed baseline conversion rate is:

**1 GBP = 105.50 INR**

This is an artificial, project-defined constant for the assignment. It is not a live or historical market exchange rate.

No external currency-conversion API is required or used.

The calculation is:

```text
price_inr = price_gbp * 105.50
```

The result is rounded to two decimal places.

Example:

```text
price_gbp = 45.17

price_inr = 45.17 * 105.50
          = 4765.44
```

The cleaned and converted dataset is stored in:

```text
data/clean_books.csv
```

The cleaned dataset contains:

```text
title
price
star_rating
availability
category
price_gbp
rating
in_stock
price_inr
```

The required transformed columns have the following types in pandas:

```text
price_gbp    float
rating       integer
in_stock     boolean
price_inr    float
```

---

# 4. SQLite Database

The cleaned dataset is loaded into SQLite using Python's built-in `sqlite3` module inside `database.ipynb`.

The generated database is:

```text
data/books.db
```

A normalized relational database design with two tables is used:

```text
categories
books
```

---

## Categories Table

The `categories` table stores each category once.

Schema:

```sql
CREATE TABLE categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT UNIQUE NOT NULL
);
```

The eight categories are represented as:

```text
category_id | category_name
------------|---------------
1           | Travel
2           | Music
3           | Art
4           | Horror
5           | History
6           | Health
7           | Food and Drink
8           | Religion
```

---

## Books Table

The `books` table stores individual book records.

Schema:

```sql
CREATE TABLE books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    price_gbp REAL NOT NULL,
    price_inr REAL NOT NULL,
    rating INTEGER NOT NULL,
    in_stock INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (category_id)
        REFERENCES categories(category_id)
);
```

The `category_id` column is a foreign key referencing:

```text
categories.category_id
```

The relationship is:

```text
categories
---------------------
category_id (PK)
category_name
       |
       | 1 : many
       |
       v
books
---------------------
book_id (PK)
title
price_gbp
price_inr
rating
in_stock
category_id (FK)
```

One category can therefore contain multiple books.

---

## Database Design Decision

Category names are stored separately in the `categories` table instead of repeatedly storing the category text for every book.

Instead of:

```text
Book A -> Travel
Book B -> Travel
Book C -> Travel
```

the category is stored once:

```text
1 -> Travel
```

and books reference that category:

```text
Book A -> category_id 1
Book B -> category_id 1
Book C -> category_id 1
```

This reduces repeated category data and establishes a normalized primary-key/foreign-key relationship.

Foreign-key enforcement is enabled using:

```sql
PRAGMA foreign_keys = ON;
```

---

## Database Recreation

`database.ipynb` rebuilds the database tables from the cleaned dataset.

Before creating the tables, the notebook executes:

```sql
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS categories;
```

The `books` table is dropped first because it contains the foreign key referencing the `categories` table.

The tables are then recreated and populated using the cleaned data.

This ensures that rerunning the notebook creates a fresh database instead of inserting duplicate book records into existing tables.

After loading the data, the database contains:

```text
8 categories
108 books
```

---

# 5. SQL Queries

SQL queries are executed against the SQLite database using `queries.py`.

Five queries demonstrate the required SQL operations.

All query strings and outputs are saved to:

```text
data/query_results.txt
```

---

## Query 1 — Books Rated Three Stars or Higher

This query demonstrates `SELECT` and `WHERE`.

```sql
SELECT book_id, title, rating
FROM books
WHERE rating >= 3;
```

It retrieves books with ratings between 3 and 5.

---

## Query 2 — 10 Most Expensive Books

This query demonstrates `ORDER BY` and `LIMIT`.

```sql
SELECT book_id, title, price_inr
FROM books
ORDER BY price_inr DESC
LIMIT 10;
```

Books are ordered from the highest INR price to the lowest, and only the first 10 records are returned.

---

## Query 3 — Distinct Ratings

This query demonstrates `DISTINCT`.

```sql
SELECT DISTINCT rating
FROM books
ORDER BY rating;
```

The resulting distinct rating values are:

```text
1
2
3
4
5
```

---

## Query 4 — Books Within a GBP Price Range

This query demonstrates `BETWEEN`.

```sql
SELECT title, price_gbp
FROM books
WHERE price_gbp BETWEEN 20 AND 30
ORDER BY price_gbp DESC;
```

It retrieves books with GBP prices between 20 and 30.

---

## Query 5 — Top-Rated Books with Categories

This query demonstrates a join between the normalized `books` and `categories` tables.

```sql
SELECT
    b.title,
    b.price_inr,
    b.rating,
    c.category_name
FROM books b
LEFT JOIN categories c
    ON b.category_id = c.category_id
ORDER BY b.rating DESC, b.book_id ASC
LIMIT 10;
```

The tables are joined using:

```text
books.category_id = categories.category_id
```

The results are ordered by rating in descending order.

`book_id` is used as a secondary ordering field to provide deterministic ordering when multiple books have the same rating.

The first 10 records are returned.

---

# 6. SQL Results with pandas

At least two SQL query results are loaded directly into pandas DataFrames using `pd.read_sql()`.

Query 1 is loaded using:

```python
query1_df = pd.read_sql(query1, conn)
```

Query 5 is loaded using:

```python
query5_df = pd.read_sql(query5, conn)
```

This demonstrates retrieving SQLite query results directly into pandas for further analysis.

---

# 7. SQL JOIN vs pandas Merge

The SQL join from Query 5 is separately reproduced using pandas without performing the join in SQL.

First, the individual database tables are loaded into DataFrames:

```python
books_df = pd.read_sql("SELECT * FROM books", conn)
categories_df = pd.read_sql("SELECT * FROM categories", conn)
```

The DataFrames are then joined using:

```python
merged_df = pd.merge(
    books_df,
    categories_df,
    how="left",
    on="category_id"
)
```

This corresponds to:

```sql
LEFT JOIN categories c
ON b.category_id = c.category_id
```

The pandas result is then sorted using:

```text
rating DESC
book_id ASC
```

The first 10 records are selected to reproduce the SQL `LIMIT 10`.

The final pandas result contains the same columns as Query 5:

```text
title
price_inr
rating
category_name
```

The SQL result and pandas result are compared using:

```python
sql_join_df.equals(merged_result)
```

The comparison produces:

```text
Results match: True
```

This confirms that the SQL `LEFT JOIN` and pandas `pd.merge()` approaches produce equivalent output.

The SQL and pandas comparison is also saved in:

```text
data/query_results.txt
```

---

# Design Decisions

## Separate Pipeline Stages

The pipeline is divided into four components:

```text
scraper.py
clean.py
database.ipynb
queries.py
```

Each component has a specific responsibility:

```text
scraper.py       -> data collection
clean.py         -> cleaning and transformation
database.ipynb   -> relational database creation and loading
queries.py       -> SQL querying and pandas comparison
```

This separation makes each stage easier to understand, execute, test, and modify independently.

---

## Preserve Raw Data

The raw scraped dataset is stored in:

```text
data/raw_books.csv
```

This allows the cleaning and database stages to be rerun without scraping the website again.

---

## Preserve Cleaned Data

The transformed dataset is stored separately in:

```text
data/clean_books.csv
```

This maintains a clear distinction between raw source data and processed data.

---

## Missing and Invalid Values

Numeric parsing failures are handled using median imputation rather than allowing unexpected values to crash the pipeline.

Rows missing essential identifying or categorical fields such as `title` or `category` are dropped because these values cannot be reliably inferred.

---

## Fixed Currency Conversion

The required fixed project baseline:

**1 GBP = 105.50 INR**

is applied directly during data transformation.

No external currency API is required, keeping the required conversion deterministic and independent of network availability.

---

## Database Normalization

Categories and books are stored in separate tables and connected using `category_id`.

This avoids repeating category names in every book record and demonstrates a normalized relational database structure using primary and foreign keys.

---

## Reproducible Database Creation

`database.ipynb` rebuilds the database tables from the cleaned dataset.

Existing tables are removed before new tables are created and populated.

This ensures that rerunning the notebook produces a clean database with the expected 108 books rather than accumulating duplicate rows.

---

## Query Output Persistence

The five SQL query strings and their outputs are stored in:

```text
data/query_results.txt
```

The SQL JOIN and pandas merge outputs, along with the comparison result, are also stored in this file.

This allows the query results to be assessed from the repository without relying only on terminal output.

---

# Output Summary

After completing all pipeline stages, the generated artifacts are:

```text
data/raw_books.csv
data/clean_books.csv
data/books.db
data/query_results.txt
```

The pipeline:

- Scrapes **108 books across 8 categories**.
- Cleans and converts the required fields.
- Uses the fixed conversion rate **1 GBP = 105.50 INR**.
- Stores data in a normalized SQLite database using two related tables.
- Executes five SQL queries covering the required SQL operations.
- Loads SQL results into pandas using `pd.read_sql()`.
- Reproduces the SQL join using `pd.merge()`.
- Confirms that both join approaches produce equivalent results with `Results match: True`.