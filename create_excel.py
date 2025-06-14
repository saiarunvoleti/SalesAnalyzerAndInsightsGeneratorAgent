# # Re-run the code to generate the Excel file with column descriptions
# import pandas as pd
# column_descriptions = {
#     "OrderDate": "Date when the order was placed",
#     "Quarter": "Fiscal quarter in which the order was placed (Q1 to Q4)",
#     "FinancialYear": "Financial year corresponding to the order date (e.g., F24)",
#     "CustomerID": "Unique identifier assigned to each customer",
#     "BusinessUnit": "Business unit handling the transaction (Retail, Enterprise, Online)",
#     "ProductName": "Name of the product sold, including its category",
#     "Category": "General category of the product (e.g., Electronics, Furniture)",
#     "Quantity": "Number of product units sold",
#     "Sales": "Total monetary value of the transaction",
#     "Profit": "Profit earned from the transaction",
#     "Region": "Geographical region where the sale occurred"
# }
#
# # Convert to DataFrame
# description_df = pd.DataFrame(list(column_descriptions.items()), columns=["Column", "Description"])
#
# # Save to Excel
# description_file_path = "/Users/saiarunvoleti/Downloads/sales_dataset_column_descriptions.xlsx"
# description_df.to_excel(description_file_path, index=False)
#
# description_file_path


import requests

url = "https://saiarunvoleti1.pythonanywhere.com/testLLM"
data = "display a bar chart for total sales in each quarter in FY25"

response = requests.post(url, json=data)  # or use data=data for form-encoded

print("Status code:", response.status_code)
# print("Response:", response.json())  # or response.text if not JSON
print("Response2: " , response.text)

import imghdr
from io import BytesIO
import base64
image_data = base64.b64decode(response.text)

# Detect format (returns 'png', 'jpeg', etc.)
image_format = imghdr.what(None, h=image_data)

print("Detected format:", image_format)