from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
import os

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(seconds=5),
}

def upload_files_to_minio():
    folder_path = '/opt/airflow/dags/source/'
    bucket_name = 'airflow-bucket'
    s3_hook = S3Hook(aws_conn_id='minio_s3')

    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv') or file_name.endswith('.xlsx'):
            local_file_path = os.path.join(folder_path, file_name)
            key = file_name
            s3_hook.load_file(filename=local_file_path, key=key, bucket_name=bucket_name, replace=True)

with DAG(
    dag_id='copy_csv_to_minio',
    default_args=default_args,
    start_date=datetime(2023, 1, 1),
    catchup=False,
    schedule_interval=None,
) as dag:

    upload_task = PythonOperator(
        task_id='upload_files_to_minio',
        python_callable=upload_files_to_minio,
    )


