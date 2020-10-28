# Filtering data in a Pandas DataFrame

> This recipe shows how to filter data in a `pandas` `DataFrame` using conditional statements. 

Libraries required:
- `pandas`

In the code chunk below, we'll import `pandas`, create some mock data about programming languages, and create a `DataFrame`.

```python
import pandas as pd

data = {
    "language": ["Python", "Python", "R", "Julia", "R"],
    "feature": ["dynamic", "object-oriented", "functional", "multiple dispatch", "dynamic"],
    "importance": [3, 2, 4, 5, 2]
}

df = pd.DataFrame(data)
```

In the chunk below, we'll create new `DataFrames` that satisfy different conditions. 

```python 
# Create a DataFrame with all rows that have importance greater than 3. 
df_important = df[df["importance"] > 3]

# Create a DataFrame with all rows that have Python as the language
df_python = df[df.language == "Python]
```

Conditions can be combined with Python's logical operators, such as `&` (and) and `|` (or).

```python 
# Create a DataFrame with all rows that have the "dynamic" feature, and importance greater than or equal to 2.
df_dynamic2 = df[df.feature == "dynamic" & df.importance >= 2]
```


