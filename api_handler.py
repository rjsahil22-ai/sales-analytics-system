import requests

def fetch_product_info(product_id):
    """
    Fetches product info from DummyJSON API.
    """
    try:
        url = "https://dummyjson.com/products"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        products = data.get("products", [])

        num = int(product_id.replace("P", ""))
        for p in products:
            if p.get("id") == num:
                return {
                    "title": p.get("title"),
                    "category": p.get("category"),
                    "brand": p.get("brand"),
                    "price": p.get("price"),
                    "rating": p.get("rating")
                }

        return {"message": f"No API product found for {product_id}"}

    except Exception as e:
        return {"error": str(e)}
