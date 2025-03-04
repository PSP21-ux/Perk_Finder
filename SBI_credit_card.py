import csv
import requests
from bs4 import BeautifulSoup
import os

# Define CSV file
CSV_FILE = "sbi_credit_cards.csv"

# Function to read existing card names from CSV
def get_existing_card_names(csv_file):
    if not os.path.exists(csv_file):
        return set()  # Return empty set if file doesn't exist

    existing_cards = set()
    with open(csv_file, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip header
        for row in reader:
            if row:  
                existing_cards.add(row[0])  # Card Name is the first column
    return existing_cards

# Function to extract features from the "Learn more" page
def extract_features(learn_more_url):
    response = requests.get(learn_more_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        tab_content_section = soup.find('section', class_='tab-content')
        if tab_content_section:
            tab_content = tab_content_section.find('div', class_='tab-inner-content', id='feature-1-tab')
            if tab_content:
                features = {}
                for feature in tab_content.find_all('li'):
                    heading = feature.find('h3')
                    if heading:
                        feature_name = heading.text.strip()
                        feature_details = [detail.text.strip() for detail in feature.find_all('li')]
                        features[feature_name] = feature_details
                return features
    return None

# Function to extract Fees (Joining Fee, Renewal Fee, Add-on Fee)
def extract_fees(learn_more_url):
    response = requests.get(learn_more_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        fees_section = soup.find('div', class_='tab-inner-content', id='feature-2-tab')
        if fees_section:
            fees = {}
            fees_list = fees_section.find('h3', string="Fees")
            if fees_list:
                fee_items = fees_list.find_next('ul')
                if fee_items:
                    fee_details = [li.get_text(strip=True) for li in fee_items.find_all('li')]
                    fees["Fees"] = fee_details
            return fees
    return None

# Main URL of the credit cards page
main_url = "https://www.sbicard.com/en/personal/credit-cards.page#all-card-tab"

# Send a GET request to the main webpage
response = requests.get(main_url)

# Check if the request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    card_containers = soup.find_all('div', class_='grid col-2')

    # Load existing cards
    existing_cards = get_existing_card_names(CSV_FILE)

    # Open CSV file in append mode
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        # Write header only if file is empty
        if os.stat(CSV_FILE).st_size == 0:
            writer.writerow(["Card Name", "Benefits", "Features", "Fees", "Learn More URL", "Apply Now URL", "Front Image URL", "Back Image URL"])

        # Loop through each card container
        for container in card_containers:
            card_name = container.find_next('h4').text.strip()

            # Skip if already added
            if card_name in existing_cards:
                print(f"⚠️ Skipping {card_name} (Already in CSV)")
                continue

            learn_more_link = container.find_next('a', class_='learn-more-link')['href']
            learn_more_url = f"https://www.sbicard.com{learn_more_link}" if not learn_more_link.startswith('http') else learn_more_link

            # Extract Apply Now URL
            apply_now_tag = container.find('div', class_='item-footer')
            apply_now_url = "N/A"
            if apply_now_tag:
                apply_link = apply_now_tag.find('a', class_='button primary')
                if apply_link and 'href' in apply_link.attrs:
                    apply_now_url = f"https://www.sbicard.com{apply_link['href']}" if not apply_link['href'].startswith('http') else apply_link['href']

            # Extract Card Images
            front_image = container.find('figure', class_='front').find('img')['src']
            back_image = container.find('div', class_='card-features back').find('img')['src']

            # Extract Benefits
            benefits_section = container.find('ul')
            benefits = [li.get_text(strip=True).replace('Rs.', 'Rs. ') for li in benefits_section.find_all('li')] if benefits_section else []

            # Extract Features & Fees from "Learn More" page
            features = extract_features(learn_more_url)
            fees = extract_fees(learn_more_url)

            # Print extracted details for debugging
            print(f"✅ Adding {card_name}")
            print(f"Learn More URL: {learn_more_url}")
            print(f"Apply Now URL: {apply_now_url}")
            print(f"Front Image URL: {front_image}")
            print(f"Back Image URL: {back_image}")

            if benefits:
                print("\n**Benefits**")
                for benefit in benefits:
                    print(f"  - {benefit}")

            if features:
                print("\n**Features**")
                for feature, details in features.items():
                    print(f"{feature}:")
                    for detail in details:
                        print(f"  - {detail}")

            if fees and "Fees" in fees:
                print("\n**Fees**")
                for detail in fees["Fees"]:
                    print(f"  - {detail}")

            print("-" * 50)

            # Write new data to CSV file
            writer.writerow([
                card_name,
                ", ".join(benefits),
                str(features) if features else "N/A",
                str(fees["Fees"]) if fees and "Fees" in fees else "N/A",
                learn_more_url,
                apply_now_url,
                front_image,
                back_image
            ])

    print(f"\n✅ Data successfully saved to {CSV_FILE}")

else:
    print(f"❌ Failed to retrieve the webpage. Status code: {response.status_code}")
