from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator



default_args = {

    "owner": "admin",
    "depends_on_past" : False,
    "email_on_failure" : False,
    "email_on_retry" : False,

    "retries" : 1,
    "retry_delay" : timedelta(minutes=3)
}


with DAG(
    dag_id = "github_event_ETL_project",
    description= "Automated Pipeline",
    schedule_interval= "0 1 * * *",
    start_date= datetime(2026,8,9),
    catchup= False,
    tags = ["pyspark", "github", "etl"]

) as dag:

    start_task = BashOperator(
        task_id = "start_pipeline",
        bash_command= 'echo "=== Bắt đầu chạy ETL Pipeline ==="'
    )

    run_spark_job = BashOperator(
        task_id = "run_spark_job",
        bash_command= 'PYTHONPATH=/opt/airflow python -m src.spark.spark_transformation'
    )

    end_task = BashOperator(
        task_id='end_pipeline',
        bash_command='echo "=== ETL Pipeline hoàn thành thành công! ==="'
    )


    start_task >> run_spark_job >> end_task