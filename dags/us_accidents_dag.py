from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator


from scripts.extract import merge_yearly_data
from scripts.transform import run_transformations
from scripts.load import load_data_to_warehouse


default_args = {
    'owner': 'Ahmed',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'us_traffic_accidents_etl',
    default_args=default_args,
    description='Automated ETL pipeline for US Traffic Accidents dataset (Star Schema)',
    schedule_interval='@monthly',
    catchup=False
) as dag:


    extract_task = PythonOperator(
        task_id='extract_and_merge_data',
        python_callable=merge_yearly_data,
    )


    transform_task = PythonOperator(
        task_id='transform_and_model_data',
        python_callable=run_transformations,
    )

    load_task = PythonOperator(
        task_id = 'load_data',
        python_callable = load_data_to_warehouse,
    )

    extract_task >> transform_task >> load_task