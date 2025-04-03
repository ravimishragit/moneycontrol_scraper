# Project: Broker Recommendation Scraper & AWS Automation

## Overview
This project is designed to scrape broker recommendations from MoneyControl, process the data, and deploy an AWS Lambda function behind an API Gateway. The processed data is stored in an S3 bucket, and an AWS Batch job cleans up old data.

---

## **Project Structure**
```
moneycontrol_scraper/
│
├── config/  
│      └── settings.py           # AWS configuration and constants  
│
├── scrapper/  
│      ├── scraper.py            # Mock data generator  
│      ├── ingestor.py           # Ingest mock data  
│
├── processor/  
│      └── data_processor.py     # Data filtering, grouping, and aggregation  
│
├── reports/  
│      └── report_generator.py   # Generates Top 3 brokers/companies report  
│
├── apis/  
│      ├── lambda_handler.py     # AWS Lambda function  
│      └── api_gateway.py        # API Gateway setup  
│
├── aws/  
│      ├── batch_cleanup.py      # AWS Batch job for cleanup  
│      ├── s3_manager.py         # S3 uploader and retriever  
│      └── deploy.sh             # Shell script for deployment  
│
├── utils/  
│      ├── logger.py             # Logger setup  
│      ├── datetime_helper.py    # Date utilities  
│      └── data_validator.py     # Data validation utils  
│
├── mock_data/                   # Mock data folder
│      └── mock_broker_data.csv  # Mock data in CSV format  
│
│
├── tests                   # Unit tests for different modules
│   ├── test_scraper.py
│   ├── test_data_processor.py
│   ├── test_lambda_handler.py
│
│── README.md               # Documentation
```
---

## **Installation & Setup**
### **1. Clone the Repository**
```bash
git clone https://github.com/ravimishragit/moneycontrol_scraper.git
cd broker-recommendation
```

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```

---

## **Execution Steps**
### **1. Run the Scraper Locally**
```bash
python main.py
```

### **2. Deploy Using `deploy.sh`**
Make sure AWS CLI is configured, then run:
```bash
chmod +x deploy.sh
./deploy.sh
```
This script will:
✅ **Package & Deploy AWS Lambda**
✅ **Set up API Gateway Integration**
✅ **Register & Submit AWS Batch Cleanup Job**

### **3. Set Up AWS Batch Job for Cleanup (Manual Alternative)**
1. Create an AWS Batch job definition:
   ```bash
   aws batch register-job-definition --job-definition-name dataCleanup \
       --type container --container-properties "{"image": "python:3.8", "command": ["python", "cleanup.py"]}"
   ```
2. Schedule the job to run daily:
   ```bash
   aws batch submit-job --job-name cleanupJob --job-queue default --job-definition dataCleanup
   ```

---

## **Mock Data Example**
Sample broker recommendation data:
```json
[
    {"broker": "HDFC Securities", "company": "Tata Steel", "recommendation": "Buy", "profit_potential": 12.5, "date": "2024-03-15"},
    {"broker": "ICICI Direct", "company": "Infosys", "recommendation": "Sell", "profit_potential": -5.2, "date": "2024-03-20"}
]
```

---

## **Testing**
Run unit tests:
```bash
pytest tests/
```


## **Contributors**
https://github.com/ravimishragit

---

## **License**
MIT License

