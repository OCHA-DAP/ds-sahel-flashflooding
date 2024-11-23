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

# CODAB

```python
%load_ext jupyter_black
%load_ext autoreload
%autoreload 2
```

```python
from src.datasources import codab
from src.constants import *
```

```python
for iso3 in ISO3S:
    print(iso3)
    codab.download_codab_to_blob(iso3)
```

```python
test = codab.load_all_codabs(admin_level=0, aoi_only=True)
```

```python
test.plot()
```

```python
test
```

```python

```
