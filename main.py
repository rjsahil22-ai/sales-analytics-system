import os
import pandas as pd

from utils.file_handler import read_sales_file
from utils.data_processor import clean_and_validate_sales
from utils.api_handler import fetch_product_info


def generate_report(records, output_path="output/sales_report.csv"):
    df = pd.DataFrame(records)

    # Add TotalAmount column
    df["TotalAmount"] = df["Quantity"] * df["UnitPrice"]

    # Save cleaned data
    df.to_csv(output_path, index=False)

    # Basic analytics
    summary = {
        "Total Sales": df["TotalAmount"].sum(),
        "Total Transactions": df.shape[0],
        "Top Region": df.groupby("Region")["TotalAmount"].sum().idxmax(),
        "Top Product": df.groupby("ProductName")["TotalAmount"].sum().idxmax(),
    }

    return df, summary


def main():
    file_path = os.path.join("data", "sales_data.txt")

    print("\n--- Reading sales data file ---")
    lines = read_sales_file(file_path)

    print("\n--- Cleaning & validating data ---")
    cleaned_records = clean_and_validate_sales(lines)

    print("\n--- Generating report ---")
    df, summary = generate_report(cleaned_records)

    print("\n--- Summary Report ---")
    for k, v in summary.items():
        print(f"{k}: {v}")

    # Fetch API info for first product (example)
    if len(cleaned_records) > 0:
        sample_product_id = cleaned_records[0]["ProductID"]
        print("\n--- Fetching product info from API ---")
        api_data = fetch_product_info(sample_product_id)
        print(f"API Data for {sample_product_id}: {api_data}")

    print("\n✅ Output saved in: output/sales_report.csv")


if __name__ == "__main__":
    main()
