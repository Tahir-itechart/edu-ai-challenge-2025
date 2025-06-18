# Product Search Tool

This is a console-based product search tool that uses OpenAI function calling to extract user preferences from natural language and filter products from the provided dataset (`products.json`).


## Setup

1. **Create and activate the virtual environment:**

```bash
python3 -m venv env
source env/bin/activate
```

Or, if the environment is already created in `task_10/env`:

```bash
source env/bin/activate
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Set your OpenAI API key in a `.env` file:**

Create a file named `.env` in the `task_10` directory with the following content:

```
TOKEN=your_openai_api_key_here
```

## Usage

Run the product search tool:

```bash
python product_search.py
```

Describe your product preferences in natural language. Example queries:
- `I'm looking for the cheapest men's clothing that is in stock`
- `Show me 2 books with the highest rating`
- `I need a kitchen appliance under $100`

The tool will return a structured list of matching products, e.g.:

```
Filtered Products:
1. Men's Socks - $9.99, Rating: 4.1, In Stock
2. Men's T-Shirt - $14.99, Rating: 4.2, In Stock
```

## Notes
- If no products match, the tool will inform you.
- If the OpenAI response cannot be parsed, the raw response will be shown for debugging.
- The code is modular and easy to extend for new features or product attributes.

## Sample Outputs
See `sample_outputs.md` for example queries and responses. 