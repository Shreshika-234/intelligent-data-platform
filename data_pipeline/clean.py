import pandas as pd

df = pd.read_csv("data/raw_books.csv")

print(df.head())
print(df.dtypes)
print(df.isnull().sum())

# cleaning the columns
df['price_gbp'] = pd.to_numeric(df['price'].str.replace('£','',regex=False),errors='coerce')
df['rating'] = df['star_rating'].map({'One':1,'Two':2,'Three':3,'Four':4,'Five':5})
df['in_stock'] = df['availability'].str.contains('In stock',case=False)

# impute numeric columns
df['price_gbp'] = df['price_gbp'].fillna(df['price_gbp'].median())
df['rating'] = df['rating'].fillna(df['rating'].median())
df['rating'] = df['rating'].astype(int)

# drop categorical values
df.dropna(subset=["title", "category", "in_stock"],inplace=True)

# convert price
df['price_inr'] = (df['price_gbp']*105.50).round(2)

clean_df = df[
    [
        "title",
        "price_gbp",
        "price_inr",
        "rating",
        "in_stock",
        "category"
    ]
].copy()

clean_df.to_csv("data/clean_books.csv", index=False)

print(clean_df.head())
clean_df.info()
