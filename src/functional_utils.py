import pandas as pd
from client import Client
from sale import Sale
from client_collection import ClientCollection
from sales_collection import SalesCollection


def top_spender_by_country(clients, sales_collection):
    result = {}
    for client in clients:
        total_spent = sales_collection.total_amount_by_client(client.client_id)
        if client.country not in result or total_spent > result[client.country][1]:
            result[client.country] = (client, total_spent)
    return result


def top_client_in_category(clients, sales_collection, category):
    top_client = None
    top_count  = 0
    for client in clients:
        client_sales = sales_collection.sales_by_client(client.client_id)
        count = sum(1 for sale in client_sales if sale.category == category)
        if count > top_count:
            top_count  = count
            top_client = client
    return top_client, top_count


def high_spending_clients(clients, sales_collection, threshold=500):
    result = []
    for client in clients:
        total_spent = sales_collection.total_amount_by_client(client.client_id)
        if total_spent > threshold:
            result.append(client)
    return result


def monthly_sales(filepath):
    df = pd.read_csv(filepath)
    df["date"]  = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.to_period("M")
    result      = df.groupby("month")["amount"].sum()
    monthly_dict = {str(k): round(v, 2) for k, v in result.items()}
    return monthly_dict