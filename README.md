# Sales Analytics System

## 📌 Problem Statement
You are a data analyst at an e-commerce company. This Python project is built to:

1. Read and clean messy sales transaction files  
2. Fetch real-time product information from an API  
3. Analyze sales patterns and customer behavior  
4. Generate comprehensive reports for business decisions  

---

## 📂 Repository Structure
```
sales-analytics-system/
│── README.md
│── main.py
│── requirements.txt
│
├── utils/
│   ├── file_handler.py
│   ├── data_processor.py
│   ├── api_handler.py
│
├── data/
│   └── sales_data.txt
│
└── output/
```

---

## 📁 Dataset Provided
File: `data/sales_data.txt`

### File Characteristics
- Pipe-delimited format (`|`)
- Non-UTF8 encoding (handled inside the code)
- Data quality issues:
  - Some fields contain commas inside values
  - Some rows may have missing or extra fields
  - Some numeric values contain commas (e.g., `1,500`)
  - Some invalid records exist (e.g., zero quantity, negative price, wrong ID format)

---

## 🧹 Data Cleaning Criteria Implemented

### ❌ REMOVE These Records (Invalid)
- Missing `CustomerID` OR missing `Region`
- `Quantity <= 0`
- `UnitPrice <= 0`
- `TransactionID` not starting with `"T"`
- Rows having missing or extra fields

Expected invalid records: ~10

---

### ✅ CLEAN and KEEP These Records (Valid)
- Remove commas in `ProductName`
  - Example: `Mouse,Wireless` → `MouseWireless`
- Remove commas in numeric fields and convert to int/float
  - Example: `1,916` → `1916`
- Skip empty lines safely

Expected valid records after cleaning: ~70

---

## 📌 Validation Output (Console Output)
The cleaning function prints the following format:

```
Total records parsed: 80
Invalid records removed: 10
Valid records after cleaning: 70
```

---

## 📊 Output Generated
After execution, a cleaned report is generated:

📌 File saved at:
```
output/sales_report.csv
```

This output contains:
- Transaction details
- Cleaned numeric fields
- A calculated `TotalAmount` column (`Quantity * UnitPrice`)

---

## 🌐 API Integration
The project fetches product details using a public API endpoint (DummyJSON):

- `utils/api_handler.py` fetches product information
- Output is printed for a sample ProductID during execution

---

## ⚙️ How to Run the Project

### 1️⃣ Clone the repository
```bash
git clone <your-repo-link>
cd sales-analytics-system
```

### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Run the project
```bash
python main.py
```

---

## 📄 Data Quality Report
A ready data quality report is available in:

```
output/data_quality_report.txt
```

---

## ✅ Deliverables Included
- `main.py` (main execution file)
- `utils/file_handler.py` (handles file reading + encoding)
- `utils/data_processor.py` (cleaning + validation)
- `utils/api_handler.py` (API integration)
- `data/sales_data.txt` (dataset)
- `output/sales_report.csv` (generated output)
- `output/data_quality_report.txt` (final report)
- `README.md` (instructions and documentation)

---

## 🚀 GitHub Push Commands
```bash
git init
git add .
git commit -m "Sales analytics system project"
git branch -M main
git remote add origin https://github.com/<username>/sales-analytics-system.git
git push -u origin main
```

---

## 👨‍💻 Author
Sahil Kashyap
