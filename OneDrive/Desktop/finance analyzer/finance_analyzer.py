import pandas as pd
import matplotlib.pyplot as plt
import os

# File paths
data_folder = "data"
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

file_path = os.path.join(data_folder, "transactions.csv")

# Load CSV with automatic cleanup
df = pd.read_csv(file_path, skip_blank_lines=True)

# Remove any completely empty rows
df.dropna(how="all", inplace=True)

# Strip spaces from column names
df.columns = df.columns.str.strip()

# Convert 'Date' to datetime safely
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df = df.dropna(subset=['Date'])

# Convert Amount to numeric
df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
df = df.dropna(subset=['Amount'])

# ===== Summary by category =====
category_summary = df.groupby('Category')['Amount'].sum()

# Save summary to CSV
summary_csv_path = os.path.join(output_folder, "category_summary.csv")
category_summary.to_csv(summary_csv_path, header=["Total_Amount"])
print(f"✅ Summary saved to {summary_csv_path}")

# ===== Plot total expenses by category =====
plt.figure(figsize=(8, 5))
category_summary.plot(kind='bar', title="Expenses by Category")
plt.ylabel("Amount Spent ($)")
plt.tight_layout()

# Save Figure 1
fig1_path = os.path.join(output_folder, "category_expenses.png")
plt.savefig(fig1_path)
print(f"✅ Figure 1 saved to {fig1_path}")

plt.show()

# ===== Plot spending over time =====
daily_expense = df.groupby('Date')['Amount'].sum()
plt.figure(figsize=(8, 5))
daily_expense.plot(kind='line', marker='o', title="Daily Spending Trend")
plt.ylabel("Amount Spent ($)")
plt.tight_layout()
plt.show()
