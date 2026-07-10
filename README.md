# US Traffic Accidents ETL Pipeline & Data Modeling

An end-to-end Data Engineering pipeline designed to ingest, clean, and model the **NHTSA CRSS US Traffic Accidents dataset (2016-2020)**. The project transforms highly normalized raw data into an optimized **Star Schema (Fact & Dimension tables)** using **Python (Pandas)** and orchestrates the entire workflow via **Apache Airflow**.

---

## 🚀 Architecture Overview

The pipeline follows the standard **Medallion/Data Warehouse architecture** partitioned into three operational stages:

1. **Extract**: Automatically scans and merges fragmented yearly data across three main domains (`Accidents`, `Vehicles`, and `People`) utilizing safe type-casting and explicit encoding handling (`ISO-8859-1`).
2. **Transform**: Drops duplicates, handles missing records from the pandemic period, constructs dimension tables, and joins them back to create a central Fact Table, resulting in a clean **Star Schema** layout.
3. **Load**: Shipped directly into a local warehouse.

---

## 📂 Project Structure

```text
us-traffic-accidents-pipeline/
│
├── dags/
│   └── us_accidents_dag.py          # Airflow DAG definition & Task Orchestration
│
├── scripts/
│   ├── extract.py                   # Data ingestion and consolidation script
│   ├── transform.py                 # Star schema data modeling & transformation
│   └── load.py                      # Data warehouse staging & database loader
│
├── requirements.txt                 # Project dependencies
└── .gitignore                       # Ensures local large data binaries remain private
```

---

## 📊 Data Model (Star Schema)

The output relational database is designed to eliminate analytical redundancy and boost query performances during visualization:

Fact_Accidents: Stores metrics like total vehicles (VE_TOTAL), pedestrian count (PEDS), and external dimension keys.

Dim_Location: Geographically indexes locations based on PSU and PJ identifiers.

Dim_Date: Time-intelligence companion supporting temporal slicing (YEAR, MONTH, DAY_WEEK).

Dim_Vehicles: Stores specific operational details of involved motor vehicles.

🛠️ Tech Stack & Requirements
Language: Python 3.12+

Orchestration: Apache Airflow

Data Wrangling: Pandas & NumPy

Storage: Local SQLite Data Warehouse

⚡ How to Run Local Testing
Clone this repository:

git clone [https://github.com/AhmedAmmar187/us-traffic-accidents-pipeline.git](https://github.com/AhmedAmmar187/us-traffic-accidents-pipeline.git)
cd us-traffic-accidents-pipeline
Prepare Data: Place the Kaggle source raw CSV files inside the data/raw/ directory.

Install dependencies:

pip install -r requirements.txt
Execution: Run scripts manually or integrate the dags/ folder directly into your local Airflow home directory.
