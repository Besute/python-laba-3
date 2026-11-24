# Python Catalog

## Classroom Information

Each classroom is represented by an `Item` object.

The object contains the following fields:

- `id` - unique identifier generated automatically
- `category` - classroom category
- `class_number` - classroom number
- `campus` - building or campus name
- `date` - date associated with the classroom record

The `date` field can be generated automatically if it is not provided.

## Usage

### Installation

This project uses Poetry for dependency management.

Install the dependencies:

```bash
poetry install
```

Activate the virtual environment:

```bash
poetry shell
```

### Creating a classroom

```python
from catalog.library import Item

classroom = Item(
    category="computer_class",
    class_number="137",
    campus="Laboratory Building"
)
```

### Catalog operations

The catalog supports the following operations:

- `add()` - add a classroom
- `get()` - retrieve a classroom by ID
- `remove()` - remove a classroom by ID
- `find_by_category()` - find classrooms by category
- `find_by_name()` - search classrooms by name
- `len()` - get the total number of classrooms
- `iter()` - iterate through catalog items
- `in` - check whether an item exists in the catalog

### Data Storage

Catalog data can be saved to and loaded from JSON files.

The storage functionality is intended to preserve classroom information between program runs.

## Testing

The project uses `pytest` for automated testing.

Run all tests:

```bash
poetry run test
```
