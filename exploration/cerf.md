---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.16.1
  kernelspec:
    display_name: ds-sahel-flashflooding
    language: python
    name: ds-sahel-flashflooding
---

# CERF

```python
%load_ext jupyter_black
%load_ext autoreload
%autoreload 2
```

```python
import matplotlib.pyplot as plt

from src.datasources import cerf
```

```python
df = cerf.load_cerf()
```

```python
df
```

```python
# Define the full range of years
full_years = range(df["effective_year"].min(), df["effective_year"].max() + 1)

# Group the data by 'effective_year' and 'Country' and sum the 'Amount in US$'
grouped = (
    df.groupby(["effective_year", "Country"])["Amount in US$"].sum().unstack()
)

# Reindex to include all years, filling missing values with 0
grouped = grouped.reindex(full_years, fill_value=0)

# Plot
fig, ax = plt.subplots(figsize=(10, 6))
grouped.plot(kind="bar", stacked=False, ax=ax)

# Add labels and title
ax.set_xlabel("Effective Year")
ax.set_ylabel("Total Amount in US$")
ax.set_title("Total Amount by Year and Country")
ax.legend(title="Country")

# Show plot
plt.tight_layout()
plt.show()
```
