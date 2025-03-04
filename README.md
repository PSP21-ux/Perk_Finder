# PERK_FINDER - Credit Card Recommendation System using LLM + RAG

## 📌 Project Overview
This project is designed to scrape credit card details from **SBI** and **Axis Bank**, preprocess the data, and use **LLM + RAG (Retrieval-Augmented Generation)** to recommend the best credit cards based on user queries. The system utilizes **FAISS** for similarity search and **Mistral-7B** for generating AI-powered responses.

---
## 📂 Project Structure

```
├── axis_scraper.py        # Web scraper for Axis Bank credit cards
├── sbi_scraper.py         # Web scraper for SBI credit cards
├── data_preprocessing.py  # Merges & cleans CSV files
├── Ai.py                  # LLM + RAG for querying credit card data
├── sbi_credit_cards.csv   # Scraped data from SBI
├── axis_credit_cards.csv  # Scraped data from Axis
├── combined_data.csv      # Merged and cleaned dataset
├── requirements.txt       # Dependencies
└── README.md              # Project documentation
```

---
## 🛠️ Setup Instructions

### 1️⃣ Install Dependencies
Run the following command to install all required libraries:
```bash
pip install -r requirements.txt
```

### 2️⃣ Run Web Scrapers
Scrape the data from SBI and Axis Bank websites by running:
```bash
python sbi_scraper.py
python axis_scraper.py
```
This will generate `sbi_credit_cards.csv` and `axis_credit_cards.csv`.

### 3️⃣ Preprocess Data
Merge and clean the scraped CSV files:
```bash
python data_preprocessing.py
```
This will generate `combined_data.csv`.

### 4️⃣ Run AI Query System
Start the LLM + RAG-based credit card recommendation system:
```bash
python Ai.py
```
You can now enter a query like:
```
Which Axis Bank credit card is best for shopping?
```

---
## 🔹 How It Works

1. **Web Scraping**: Extracts credit card details from SBI and Axis Bank.
2. **Data Preprocessing**: Cleans and merges scraped data into a structured format.
3. **FAISS Vector Search**: Converts text into embeddings and performs similarity search.
4. **LLM (Mistral-7B) + RAG**: Generates responses based on retrieved documents.

---
## 📌 Example Query

**Input:**
```
Which Axis Bank credit card is best for shopping?
```

**AI Response:**
```
Based on the available data, the best Axis Bank credit cards for shopping are:
1. Axis Bank Flipkart Credit Card - 5% cashback on Flipkart
2. Axis Bank ACE Credit Card - 2% cashback on all online shopping
3. Axis Bank MY ZONE Credit Card - Exclusive offers on fashion & dining
```

---
## 🔗 Future Improvements
- Add more banks and credit cards to expand recommendations.
- Improve query understanding using advanced LLM techniques.
- Deploy as an API or chatbot for real-time queries.

---
## 📜 License
This project is open-source. Feel free to contribute!

---
### 🚀 Happy Coding! 🎯

