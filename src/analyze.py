import json
import os
import csv
import pandas as pd

from client import Client
from sale import Sale
from client_collection import ClientCollection
from sales_collection import SalesCollection
from functional_utils import (
    top_spender_by_country,
    top_client_in_category,
    high_spending_clients,
    monthly_sales
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_clients(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
        clients = []
        for item in data:
            clients.append(Client(
                item["client_id"],
                item["name"],
                item["country"],
                item.get("signup_date", None)  # ← add this
            ))
    return clients


def load_sales(filepath):
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        sales = []
        for row in reader:
            sales.append(Sale(
                row["sale_id"],
                int(row["client_id"]),
                row["product"],
                row["category"],
                float(row["amount"]),
                row.get("date", None)  # ← add this
            ))
    return sales


def generate_report():
    # Load data internally
    clients = load_clients(os.path.join(BASE_DIR, 'data', 'clients.json'))
    sales   = load_sales(os.path.join(BASE_DIR, 'data', 'sales.csv'))

    client_collection = ClientCollection(clients)
    sales_collection  = SalesCollection(sales)

    filepath = os.path.join(BASE_DIR, 'data', 'report.json')

    summary = {
        "total_clients": len(clients),
        "total_sales":   len(sales),
        "total_revenue": round(sum(sale.amount for sale in sales), 2)
    }

    clients_data = []
    for client in clients:
        clients_data.append({
            "client_id":       client.client_id,
            "name":            client.name,
            "country":         client.country,
            "total_spent":     round(sales_collection.total_amount_by_client(client.client_id), 2),
            "average_sale":    round(sales_collection.average_sale_by_client(client.client_id), 2),
            "number_of_sales": len(sales_collection.sales_by_client(client.client_id))
        })

    country_results = top_spender_by_country(clients, sales_collection)
    top_by_country  = {}
    for country, (client, total) in country_results.items():
        top_by_country[country] = client.name

    categories = set(sale.category for sale in sales)
    sales_by_category = {}
    for category in categories:
        sales_by_category[category] = round(
            sales_collection.total_amount_by_category(category), 2
        )

    high_spenders       = high_spending_clients(clients, sales_collection, threshold=500)
    high_spending_names = [client.name for client in high_spenders]

    monthly = monthly_sales(os.path.join(BASE_DIR, 'data', 'sales.csv'))

    report = {
        "summary":           summary,
        "clients":           clients_data,
        "top_by_country":    top_by_country,
        "sales_by_category": sales_by_category,
        "high_spenders":     high_spending_names,
        "monthly_sales":     monthly
    }

    with open(filepath, "w") as f:
        json.dump(report, f, indent=4)

    print("Report saved to report.json")
    return report


# ============================================================
# MAIN CODE
# ============================================================


clients = load_clients(os.path.join(BASE_DIR, 'data', 'clients.json'))
sales   = load_sales(os.path.join(BASE_DIR, 'data', 'sales.csv'))

client_collection = ClientCollection(clients)
sales_collection  = SalesCollection(sales)

# Calculation 1
total_clients = len(clients)
print(f"Total clients: {total_clients}")

# Calculation 2
total_sales = len(sales)
print(f"Total sales: {total_sales}")

# Calculation 3
for client in clients:
    total = sales_collection.total_amount_by_client(client.client_id)
    print(f"{client.name} total spent: €{round(total, 2)}")

# Calculation 4
for client in clients:
    count = len(sales_collection.sales_by_client(client.client_id))
    print(f"{client.name} number of sales: {count}")

# Calculation 5
for client in clients:
    avg = sales_collection.average_sale_by_client(client.client_id)
    print(f"{client.name} average sale: €{round(avg, 2)}")

# Calculation 6
country_result = top_spender_by_country(clients, sales_collection)
for country, (client, total) in country_result.items():
    print(f"{country}: {client.name} → €{round(total, 2)}")

# Calculation 7
categories = set(sale.category for sale in sales)
for category in categories:
    print(f"{category} total: €{round(sales_collection.total_amount_by_category(category), 2)}")

# Calculation 8
client8, count8 = top_client_in_category(clients, sales_collection, "Electronics")
print(f"Top Electronics client: {client8.name} with {count8} purchases")

# Calculation 9
spending_result = high_spending_clients(clients, sales_collection, threshold=500)
print("High spending clients:")
for client in spending_result:
    total = sales_collection.total_amount_by_client(client.client_id)
    print(f"  {client.name} → €{round(total, 2)}")

# Calculation 10
monthly = monthly_sales(os.path.join(BASE_DIR, 'data', 'sales.csv'))
print(f"Monthly sales: {monthly}")

# Generate final report
generate_report(clients, sales, sales_collection, os.path.join(BASE_DIR, 'data', 'report.json'))