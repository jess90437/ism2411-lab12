"""
Reflection Answers:
1. You've now completed a full ETL pipeline: read a CSV, transform the data, 
   write a new CSV. How does this compare to doing the same task in Excel? 
   What can Python do that Excel can't do easily, and vice versa?
   - Doing ETL in Python is repeatable and automated via scripts, making it 
     ideal for handling large datasets or recurring workflows without manual 
     clicking. Excel provides an intuitive graphical interface and instant 
     visual feedback, but struggles with massive files or complex, multi-step 
     programmatic transformations that Python handles easily.

2. Exercise 8 showed you append mode. Think of a real business process that 
   would benefit from an append-mode log file — describe it and explain 
   why append mode is the right tool.
   - An e-commerce order processing or system error-tracking log benefits 
     greatly from append mode. Append mode ensures that new log entries are 
     safely added to the bottom of the file without overwriting historical 
     records, creating a permanent audit trail.
"""

import csv
from datetime import datetime
import os

# --- Exercise 1 ---
os.makedirs("data", exist_ok=True)

csv_path = "data/sales.csv"
cleaned_path = "data/cleaned.csv"
log_path = "data/run_log.txt"

# --- Exercise 2 ---
print("--- Exercise 2 ---")
with open(csv_path, mode="r", encoding="utf-8") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)

# --- Exercise 3 ---
print("\n--- Exercise 3 ---")
with open(csv_path, mode="r", encoding="utf-8") as file:
    reader = csv.reader(file)
    header = next(reader)
    print("Header:", header)
    print("First data row starts here:")
    for row in reader:
        print(row)

# --- Exercise 4 ---
print("\n--- Exercise 4 ---")
total_revenue = 0
with open(csv_path, mode="r", encoding="utf-8") as file:
    reader = csv.reader(file)
    header = next(reader)  # skip header
    for row in reader:
        product = row[0]
        price = float(row[1])
        quantity = int(row[2])
        line_total = price * quantity
        total_revenue += line_total
        print(f"{product}: {quantity} units × ${price:.2f} = ${line_total:.2f}")

print(f"Overall Total Revenue: ${total_revenue:.2f}")

# --- Exercise 5 ---
print("\n--- Exercise 5 ---")
original_row_count = 0
written_row_count = 0

with open(csv_path, mode="r", encoding="utf-8") as infile, open(
    cleaned_path, mode="w", newline="", encoding="utf-8"
) as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    header = next(reader)
    writer.writerow(["Product", "Price", "Qty", "Total"])

    for row in reader:
        original_row_count += 1
        product, price_str, qty_str = row[0], row[1], row[2]
        price = float(price_str)
        quantity = int(qty_str)
        line_total = price * quantity

        if line_total > 100:
            writer.writerow([product, price, quantity, line_total])
            written_row_count += 1

print(f"Original rows: {original_row_count}")
print(f"Written rows (> $100): {written_row_count}")

# --- Exercise 6 ---
print("\n--- Exercise 6 ---")
# Approach comparison comment:
# Use csv.reader when working with simple index-based lists or unknown schemas.
# Use csv.DictReader when column names are known, making code much more readable and robust.
dict_total_revenue = 0
with open(csv_path, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        product = row["product"]
        price = float(row["price"])
        quantity = int(row["quantity"])
        dict_total_revenue += price * quantity

print(f"DictReader Total Revenue: ${dict_total_revenue:.2f}")

# --- Exercise 7 ---
print("\n--- Exercise 7 ---")
product_summary = {}
with open(csv_path, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        product = row["product"]
        revenue = float(row["price"]) * int(row["quantity"])
        product_summary[product] = product_summary.get(product, 0) + revenue

print("Product Summary (Sorted):")
for prod in sorted(product_summary.keys()):
    print(f"{prod}: ${product_summary[prod]:.2f}")

# --- Exercise 8 ---
print("\n--- Exercise 8 ---")
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
log_entry = f"Run timestamp: {current_time} | Total Revenue: ${total_revenue:.2f}\n"

with open(log_path, mode="a", encoding="utf-8") as log_file:
    log_file.write(log_entry)

print(f"Appended log entry to {log_path}")