from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.docker_operator import DockerOperator
import docker.types
from config import environment
from airflow.models import Variable

# City Name Variable
city_name = Variable.get("CITY_NAME")

default_args = {
    "owner": "TZT",
    "description": "Compute Air quality  measurement for a city",
    "depend_on_past": True,
    "start_date": datetime(2024, 4, 23, 9, 0, 0),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}


mount = docker.types.Mount(
    type="tmpfs", source=None, target="/tmp/cache", tmpfs_size="2g", read_only=False
)

if environment["REFRESH_RATE"].isdigit():
    refresh_rate = int(environment["REFRESH_RATE"])
    schedule_interval = timedelta(hours=refresh_rate)
else:
    schedule_interval = environment["REFRESH_RATE"]
    schedule_interval = " ".join(schedule_interval)


dag = DAG(
    dag_id="Compute-measurements-Amsterdam-ETL",
    default_args=default_args,
    schedule_interval=schedule_interval,
)


def handle_timeout(context):
    # Code to handle timeout issue
    print("There is an error in the airflow process")


compute_reference = DockerOperator(
    task_id="compute_measurements",
    image="airflow_ddp",
    container_name=f"{city_name}_compute_measurements",
    api_version="auto",
    environment=environment,
    mounts=[mount],
    auto_remove=True,
    mount_tmp_dir=False,
    command=f"--city_name={city_name}",
    docker_url="TCP://docker-socket-proxy:2375",
    network_mode="demo_datapipeline_airflow_default",
    on_failure_callback=handle_timeout,
    dag=dag,
)

compute_reference
