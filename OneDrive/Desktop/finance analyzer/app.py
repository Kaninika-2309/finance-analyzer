import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Finance Analyzer")

uploaded_file = st.file_uploader("Upload Transactions CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # Ensure proper date and amount types
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
    df.dropna(subset=['Date', 'Amount'], inplace=True)

    st.write("Data Preview", df.head())

    monthly_expenses = df.groupby(df['Date'].dt.to_period("M"))['Amount'].sum()

    fig, ax = plt.subplots()
    monthly_expenses.plot(kind="bar", ax=ax)
    ax.set_title("Monthly Expenses")
    ax.set_ylabel("Amount")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Save figure
    fig.savefig("figure1.png")

    # Save processed output
    output_csv = "processed_transactions.csv"
    df.to_csv(output_csv, index=False)

    # Download button
    with open(output_csv, "rb") as f:
        st.download_button("Download Processed CSV", f, "processed_transactions.csv")
