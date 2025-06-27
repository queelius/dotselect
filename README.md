# `dotselect`

> "What we observe is not nature itself, but nature exposed to our method of questioning."
>
> — Werner Heisenberg

**Advanced `dot` pathing with wildcards, descendants, and predicates.**

```python
>>> from dotselect import find_all
>>> data = {
...     "id": "proj1",
...     "spec": {
...         "components": [
...             {"id": "comp1", "type": "server", "ports": [80, 443]},
...             {"id": "comp2", "type": "database", "version": "14.2"}
...         ]
...     }
... }
>>> # Find every 'id' key, no matter how deeply it's nested.
>>> find_all(data, "**.id")
['proj1', 'comp1', 'comp2']
```

## Why? A Rich, Pre-built Path Language

The `dot` ecosystem provides a layered approach to finding data. `dotselect` provides a rich, pre-built syntax that combines the most common and powerful addressing patterns into a single tool.

*   **Exact Addressing (`dotget` style):** `spec.components.0`
*   **Pattern Addressing (`dotstar` style):**
    *   `*` (Adjacency Wildcard): Matches direct children. `spec.components.*.id`
    *   `**` (Descendant Wildcard): Matches at any depth. `**.id`
*   **Conditional Addressing:** `spec.components[type=server]`

You can combine them to ask complex questions with maximum expressiveness and minimum syntax.

## The Path Language

### The Descendant Wildcard: `**`

The "deep scan" operator. It matches any key at any level of nesting. Use it when you don't know or care about the exact path to a key.

```python
# Finds the 'version' key whether it's at the root or deeply nested.
find_first(data, "**.version")
# -> "14.2"
```

### The Adjacency Wildcard: `*`

Selects all items in a list or all values in a dictionary at a single level.

```python
# Find all ports for all components
find_all(data, "spec.components.*.ports")
# -> [[80, 443], ["14.2"]]  Wait, we can do better...
```

### The Predicate: `[key=value]`

Selects items from a list of dictionaries based on a condition.

```python
# Find the ports of only the 'server' component
find_first(data, "spec.components[type=server].ports")
# -> [80, 443]
```

## Command-Line Usage

`dotselect` can be used as a command-line tool to query JSON or YAML files.

The output format will match the input format.

```bash
# Find all ids in a JSON file from stdin
cat data.json | dotselect '**.id' > ids.json

# Find the ports of the server component in a YAML file
dotselect 'spec.components[type=server].ports' data.yml > ports.yml
```

## When to use `dotselect`

✅ You need to combine wildcards, deep scans, and conditional filters.
✅ You need to find data without knowing its exact depth or location.
✅ You want the most powerful *pre-built* addressing tool in the `dot` ecosystem.

## When NOT to use `dotselect`

❌ You *only* need a simple wildcard (`*`). Use `dotstar` for clarity and simplicity.
❌ You *only* need an exact path. Use `dotget`.
❌ You need to define a **custom path syntax** (e.g., regex keys, fuzzy matching) or need to build a specialized, high-performance tool. **Use the `dotpath` engine for this.**

## Philosophy

`dotselect` embodies the principle of "the right tool for the job." While `dotget` and `dotstar` provide simple, elegant solutions for common cases, `dotselect` provides a powerful, curated set of features for the vast majority of complex data-finding tasks.

It is the bridge between simplicity and full extensibility. Its purpose is to provide a rich, expressive syntax for asking complex questions about the location of data, without requiring the user to engage with the underlying `dotpath` engine. It gives precise, unambiguous locations to the **Action Layer** tools (`dotpipe`, `dotmod`), enabling them to perform powerful, targeted operations.

## Install

```bash
pip install dotselect
```

## License

MIT

