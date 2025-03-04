import pandas as pd
import re

# Load SBI Credit Card CSV file
df_sbi = pd.read_csv("sbi_credit_cards.csv")
df_sbi.drop_duplicates(inplace=True)

# Function to extract Joining Fee
def extract_joining_fee(fees):  
    if pd.isna(fees):  # Handle NaN values
        return "Not Available"
    fees = str(fees).replace("\xa0", " ").strip()  # Normalize spaces
    match = re.search(r"(?:Joining|Annual) Fee.*?:\s*Rs\.?\s*([\d,]+)", fees, re.IGNORECASE)
    return match.group(1) if match else "Not Available"

# Function to extract Renewal Fee
def extract_renewal_fee(fees):
    if pd.isna(fees):  # Handle NaN values
        return "Not Available"
    fees = str(fees).replace("\xa0", " ").strip()  # Normalize spaces
    match = re.search(r"Renewal Fee.*?:\s*Rs\.?\s*([\d,]+)", fees, re.IGNORECASE)
    return match.group(1) if match else "Not Available"

# Apply extraction functions
df_sbi["Joining_Fee"] = df_sbi["Fees"].apply(extract_joining_fee)
df_sbi["Renewal_Fee"] = df_sbi["Fees"].apply(extract_renewal_fee)

# Remove the "Fees" column
df_sbi.drop(columns=["Fees"], inplace=True)

# Rearrange columns for consistency
df_sbi = df_sbi[["Card Name", "Joining_Fee", "Renewal_Fee", "Benefits", "Features", "Learn More URL", "Apply Now URL"]]

# Load Axis Bank CSV file
df_axis = pd.read_csv("axis_credit_cards.csv")

# Rename columns to match SBI format
df_axis.rename(columns={
    "Features": "Benefits",
    "Rewards": "Features",
    "Annual Fee": "Renewal_Fee"
}, inplace=True)

# Rearrange columns for consistency
df_axis = df_axis[["Card Name", "Joining Fee", "Renewal_Fee", "Benefits", "Features", "Know More Link", "Apply Now Link"]]

# Rename columns to match SBI naming convention
df_axis.rename(columns={
    "Joining Fee": "Joining_Fee",
    "Know More Link": "Learn More URL"
}, inplace=True)

# Combine both dataframes into one
df_combined = pd.concat([df_sbi, df_axis], ignore_index=True)

# Save to CSV
df_combined.to_csv("combined_credit_cards.csv", index=False)

# Display first 5 rows of the combined data
print(df_combined.head())
