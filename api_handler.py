import requests


def fetch_all_products():
    """
    Fetches all products from DummyJSON API

    Returns: list of product dictionaries

    Requirements:
    - Fetch all available products (use limit=100)
    - Handle connection errors with try-except
    - Return empty list if API fails
    - Print status message (success/failure)
    """
    try:
        url = "https://dummyjson.com/products?limit=100"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        products = data.get("products", [])

        print(f"✅ API Success: Fetched {len(products)} products")
        return products

    except Exception as e:
        print(f"❌ API Failed: {e}")
        return []


def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info

    Parameters: api_products from fetch_all_products()

    Returns: dictionary mapping product IDs to info

    Expected Output Format:
    {
      1: {'title': 'iPhone 9', 'category': 'smartphones', 'brand': 'Apple', 'rating': 4.69},
      2: {'title': 'iPhone X', 'category': 'smartphones', 'brand': 'Apple', 'rating': 4.44},
      ...
    }
    """
    mapping = {}

    for p in api_products:
        pid = p.get("id")
        if pid is None:
            continue

        mapping[pid] = {
            "title": p.get("title"),
            "category": p.get("category"),
            "brand": p.get("brand"),
            "rating": p.get("rating"),
        }

    return mapping


def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information

    Parameters:
    - transactions: list of transaction dictionaries
    - product_mapping: dictionary from create_product_mapping()

    Returns: list of enriched transaction dictionaries

    Enrichment Logic:
    - Extract numeric ID from ProductID (P101 -> 101, P5 -> 5)
    - If ID exists in product_mapping, add API fields
    - If ID doesn't exist, set API_Match = False and other fields to None
    - Handle all errors gracefully

    File Output:
    - Save enriched data to 'data/enriched_sales_data.txt'
    - Use same pipe-delimited format
    - Include new columns in header
    """
    enriched = []

    for t in transactions:
        enriched_txn = dict(t)  # copy original

        try:
            product_id_str = str(t.get("ProductID", "")).strip()

            # Extract numeric part: P101 -> 101
            numeric_id = int(product_id_str.replace("P", ""))

            if numeric_id in product_mapping:
                api_info = product_mapping[numeric_id]
                enriched_txn["API_Category"] = api_info.get("category")
                enriched_txn["API_Brand"] = api_info.get("brand")
                enriched_txn["API_Rating"] = api_info.get("rating")
                enriched_txn["API_Match"] = True
            else:
                enriched_txn["API_Category"] = None
                enriched_txn["API_Brand"] = None
                enriched_txn["API_Rating"] = None
                enriched_txn["API_Match"] = False

        except Exception:
            enriched_txn["API_Category"] = None
            enriched_txn["API_Brand"] = None
            enriched_txn["API_Rating"] = None
            enriched_txn["API_Match"] = False

        enriched.append(enriched_txn)

    return enriched


def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):
    """
    Saves enriched transactions back to file

    Expected File Format:
    TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match

    Requirements:
    - Create output file with all original + new fields
    - Use pipe delimiter
    - Handle None values appropriately
    """
    header = [
        "TransactionID", "Date", "ProductID", "ProductName",
        "Quantity", "UnitPrice", "CustomerID", "Region",
        "API_Category", "API_Brand", "API_Rating", "API_Match"
    ]

    with open(filename, "w", encoding="utf-8") as f:
        f.write("|".join(header) + "\n")

        for t in enriched_transactions:
            row = [
                str(t.get("TransactionID", "")),
                str(t.get("Date", "")),
                str(t.get("ProductID", "")),
                str(t.get("ProductName", "")),
                str(t.get("Quantity", "")),
                str(t.get("UnitPrice", "")),
                str(t.get("CustomerID", "")),
                str(t.get("Region", "")),
                str(t.get("API_Category", "") if t.get("API_Category") is not None else ""),
                str(t.get("API_Brand", "") if t.get("API_Brand") is not None else ""),
                str(t.get("API_Rating", "") if t.get("API_Rating") is not None else ""),
                str(t.get("API_Match", "")),
            ]
            f.write("|".join(row) + "\n")

    print(f"✅ Enriched data saved to: {filename}")
