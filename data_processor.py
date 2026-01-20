from datetime import datetime

EXPECTED_HEADERS = [
    "TransactionID", "Date", "ProductID", "ProductName",
    "Quantity", "UnitPrice", "CustomerID", "Region"
]

def _clean_number(value):
    """
    Removes commas from numbers like 1,500 -> 1500
    """
    if value is None:
        return None
    value = str(value).strip()
    value = value.replace(",", "")
    return value

def _clean_product_name(name):
    """
    Removes commas from product name like Mouse,Wireless -> MouseWireless
    """
    if name is None:
        return ""
    return str(name).replace(",", "").strip()

def clean_and_validate_sales(lines):
    """
    Cleans and validates sales records.
    Rules:
    - Remove records if CustomerID missing OR Region missing
    - Remove if Quantity <= 0
    - Remove if UnitPrice <= 0
    - Remove if TransactionID does not start with 'T'
    - Keep valid records after cleaning commas in names/numbers
    """
    total_parsed = 0
    invalid_removed = 0
    valid_records = []

    # remove empty lines
    lines = [ln for ln in lines if ln.strip()]

    # header
    header = lines[0].strip().split("|")
    if header != EXPECTED_HEADERS:
        # still continue but assume correct order
        pass

    for line in lines[1:]:
        total_parsed += 1

        parts = line.split("|")

        # If missing/extra fields -> invalid
        if len(parts) != 8:
            invalid_removed += 1
            continue

        transaction_id, date_str, product_id, product_name, qty, unit_price, customer_id, region = parts

        # Basic cleaning
        transaction_id = transaction_id.strip()
        date_str = date_str.strip()
        product_id = product_id.strip()
        product_name = _clean_product_name(product_name)
        customer_id = customer_id.strip()
        region = region.strip()

        # Remove invalid: missing CustomerID or Region
        if customer_id == "" or region == "":
            invalid_removed += 1
            continue

        # Remove invalid: TransactionID not starting with T
        if not transaction_id.startswith("T"):
            invalid_removed += 1
            continue

        # Validate date format (YYYY-MM-DD)
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            invalid_removed += 1
            continue

        # Clean numbers
        qty_clean = _clean_number(qty)
        price_clean = _clean_number(unit_price)

        try:
            qty_int = int(qty_clean)
            price_float = float(price_clean)
        except ValueError:
            invalid_removed += 1
            continue

        # Remove invalid: Quantity <= 0 or UnitPrice <= 0
        if qty_int <= 0 or price_float <= 0:
            invalid_removed += 1
            continue

        valid_records.append({
            "TransactionID": transaction_id,
            "Date": date_str,
            "ProductID": product_id,
            "ProductName": product_name,
            "Quantity": qty_int,
            "UnitPrice": price_float,
            "CustomerID": customer_id,
            "Region": region
        })

    print(f"Total records parsed: {total_parsed}")
    print(f"Invalid records removed: {invalid_removed}")
    print(f"Valid records after cleaning: {len(valid_records)}")

    return valid_records
