# Part Numbering Method

It's hard to know how to pre-allocate a naming scheme without knowing how many parts will be in each category.  This is a quick apporach to finding out that sort of info.

Look at the number of parts in a large supplier's database and arrange part numbering so that each "section" has a reasonable number of entries.

## Data source:

JCLPCB database from here:

https://yaqwsx.github.io/jlcparts/

```shell
wget https://yaqwsx.github.io/jlcparts/data/cache.zip \
  https://yaqwsx.github.io/jlcparts/data/cache.z0{1..9} \
  https://yaqwsx.github.io/jlcparts/data/cache.z1{0..9}
7z x cache.zip
```

Once you have the data extracted, you can examine it with a SQLite editor/viewer like SQLite Studio.

Use Python to get the frequency of use of each category.

```python
import pandas as pd
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('cache.sqlite3')

# Load data from 'components' table into a pandas DataFrame
query1 = "SELECT category_id FROM components"
df1 = pd.read_sql_query(query1, conn)

# Load data from 'categories' table into another pandas DataFrame
query2 = """
    SELECT c.id as cat_id, c.category, c.subcategory 
    FROM categories AS c
"""
df2 = pd.read_sql_query(query2, conn)

df2['full_category'] = df2['category'] + " - " + df2['subcategory']

# Merge the two DataFrames on 'cat_id'
merged_df = pd.merge(df1, df2, left_on='category_id', right_on='cat_id')

# Count occurrences of each category and sub-category
count_series = merged_df['full_category'].value_counts()

# Save count_series into a csv file named 'category_counts.csv'
count_series.to_csv('category_counts.csv')
```

Then manually edit and group the results in `category_counts.csv`.

## Categories Defined

After a bit of data wrangling and some manual sorting/arranging, I have come up with:

* TBD

## Adding Data

I want to enter data in CSV format so that it can be tracked in revision control.

Convert the CSVs to sqlite using

```shell
pip install csvs-to-sqlite
csvs-to-sqlite ~/path/to/directory kicad_parts.sqlite3
```
