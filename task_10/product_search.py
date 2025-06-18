import json
import os
from typing import Any, Dict, List, Optional
import openai
from dotenv import load_dotenv

PRODUCTS_FILE = 'products.json'
ENV_TOKEN = 'TOKEN'
MODEL_NAME = 'gpt-4.1-mini'


def load_products(filepath: str) -> List[Dict[str, Any]]:
    """Load the products dataset from a JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)


def get_openai_client() -> openai.OpenAI:
    """Load API key from environment and return an OpenAI client instance."""
    load_dotenv()
    token = os.getenv(ENV_TOKEN)
    if not token:
        raise EnvironmentError(f"Please set the {ENV_TOKEN} environment variable.")
    return openai.OpenAI(api_key=token)


def get_function_schema() -> List[Dict[str, Any]]:
    """Return the function schema for OpenAI function calling."""
    return [
        {
            "name": "find_products",
            "description": "Filter and sort products based on user preferences.",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {"type": "string", "description": "Product category, e.g. Electronics, Fitness, Kitchen, Books, Clothing."},
                    "max_price": {"type": "number", "description": "Maximum price user is willing to pay."},
                    "min_rating": {"type": "number", "description": "Minimum product rating."},
                    "in_stock": {"type": "boolean", "description": "Whether the product should be in stock."},
                    "keywords": {"type": "string", "description": "Keywords or features user wants (e.g. camera, battery, etc)."},
                    "sort_by": {"type": "string", "description": "Field to sort by, e.g. price, rating."},
                    "sort_order": {"type": "string", "enum": ["asc", "desc"], "description": "Sort order: asc or desc."},
                    "limit": {"type": "integer", "description": "Maximum number of products to return."}
                },
                "required": []
            }
        }
    ]


def prompt_user() -> str:
    """Prompt the user for their product search preferences."""
    print("Welcome to the Product Search Tool!")
    print("Describe what you are looking for (e.g. 'I need a smartphone under $800'):")
    return input("> ")


def extract_preferences(client: openai.OpenAI, user_query: str, products: List[Dict[str, Any]], function_schema: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Use OpenAI function calling to extract user preferences from natural language."""
    system_prompt = (
        "You are a helpful assistant that helps users find products from a dataset based on their preferences. "
        "You can filter, sort, and limit the number of products returned. Use the function call to filter, sort, and limit the products. "
        "If the user asks for the 'cheapest', 'most expensive', or 'highest rated' product, sort accordingly and return only the top result (limit: 1). "
        "Return only the matching products."
    )
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query},
            {"role": "system", "content": f"Here is the product dataset: {json.dumps(products)}"}
        ],
        functions=function_schema,
        function_call={"name": "find_products"}
    )
    args = response.choices[0].message.function_call.arguments
    return json.loads(args)


def get_filtered_products(client: openai.OpenAI, products: List[Dict[str, Any]], preferences: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
    """Use OpenAI to filter, sort, and limit products based on extracted preferences."""
    filter_prompt = (
        "You are a helpful assistant that filters, sorts, and limits products from a dataset based on user preferences. "
        "Return only the matching products as a JSON list."
    )
    filter_response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": filter_prompt},
            {"role": "user", "content": f"Filter these products: {json.dumps(products)} with preferences: {json.dumps(preferences)}"}
        ]
    )
    result = filter_response.choices[0].message.content
    try:
        return json.loads(result)
    except Exception:
        print("Could not parse the response as JSON. Raw response:")
        print(result)
        return None


def print_products(products: Optional[List[Dict[str, Any]]]) -> None:
    """Print the filtered products in a structured format."""
    print("\nFiltered Products:")
    if not products:
        print("No products found matching your preferences.")
        return
    for idx, prod in enumerate(products, 1):
        name = prod.get('name', 'Unknown')
        price = prod.get('price', 'N/A')
        rating = prod.get('rating', 'N/A')
        in_stock = prod.get('in_stock', False)
        stock_str = 'In Stock' if in_stock else 'Out of Stock'
        print(f"{idx}. {name} - ${price}, Rating: {rating}, {stock_str}")


def main():
    """Main entry point for the product search tool."""
    try:
        products = load_products(os.path.join(os.path.dirname(__file__), PRODUCTS_FILE))
        client = get_openai_client()
        function_schema = get_function_schema()
        user_query = prompt_user()
        preferences = extract_preferences(client, user_query, products, function_schema)
        filtered_products = get_filtered_products(client, products, preferences)
        print_products(filtered_products)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
