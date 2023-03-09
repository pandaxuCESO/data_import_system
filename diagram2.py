from diagrams import Cluster, Diagram
from diagrams.gcp.compute import Functions, KubernetesEngine, GCE
from diagrams.gcp.database import SQL
from diagrams.gcp.network import LoadBalancing
from diagrams.gcp.analytics import PubSub
from diagrams.gcp.storage import Storage
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.analytics import Spark
from diagrams.programming.flowchart import Action
from diagrams.onprem.inmemory import Memcached
from diagrams.gcp.operations import Monitoring
from diagrams.gcp.security import KMS
from diagrams.aws.compute import ApplicationAutoScaling
from diagrams.onprem.iac import Terraform
from diagrams.onprem.gitops import ArgoCD


with Diagram("Data Import System Architecture", show=False):
    with Cluster("Angular Client"):
        client = User("Front-end client")

    with Cluster("CSV Files"):
        csv_storage = Storage("CSV Storage")

    with Cluster("Processing Cluster"):
        with Cluster("Kubernetes Cluster"):
            k8s_cluster = KubernetesEngine("Kubernetes Cluster")
            with Cluster("Workers"):
                workers = [
                    Functions("Function 1"),
                    Functions("Function 2"),
                    Functions("Function 3"),
                ]
                autoscaler = ApplicationAutoScaling("Autoscaler")
            with Cluster("Master"):
                spark_master = Spark("Spark Master")
                with Cluster("Spark Workers"):
                    spark_workers = [
                        Spark("Spark Worker 1"),
                        Spark("Spark Worker 2"),
                        Spark("Spark Worker 3"),
                    ]

    with Cluster("Database Cluster"):
        with Cluster("PostgreSQL Instances"):
            postgres_instances = [
                SQL("Instance 1"),
                SQL("Instance 2"),
                SQL("Instance 3"),
            ]
        with Cluster("Load Balancer"):
            load_balancer = LoadBalancing("Load Balancer")

    with Cluster("Caching Cluster"):
        caching_instance = Memcached("Memcached Instance")

    with Cluster("Data Consumer"):
        user = User("Data Consumer")

    with Cluster("Message Queue / PubSub"):
        message_queue = PubSub("Message Queue / PubSub")

    with Cluster("CI/CD"):
        argo = ArgoCD("Argo")

    with Cluster("Data Sharding"):
        data_sharding = Server("Data Sharding")

    with Cluster("Management"):
        monitoring = Monitoring("Monitoring")
        logging = Monitoring("Logging")

    with Cluster("Security"):
        kms = KMS("Key Management Service")

    with Cluster("Infrastructure as Code"):
        terraform = Terraform("Terraform")

    client >> Action("Submit CSV file") >> csv_storage
    csv_storage >> Action("Upload CSV files") >> workers
    workers >> Action("Split CSV into smaller chunks") >> spark_master
    spark_master >> Action("Process data using Spark") >> spark_workers
    spark_workers >> Action("Shard data into multiple streams") >> data_sharding
    data_sharding >> Action("Send sharded data to message queue") >> message_queue
    message_queue >> Action("Send messages to consumers") >> workers
    workers >> Action("Perform database operations") >> postgres_instances
    postgres_instances >> Action("Optimize database indexing") >> load_balancer
    load_balancer >> Action("Load balance database queries") >> postgres_instances
    postgres_instances >> Action("Use bulk insert") >> caching_instance
    caching_instance >> Action("Cache data using Memcached") >> user
    spark_workers >> Action("Monitor Spark cluster using Prometheus") >> monitoring
    postgres_instances >> Action("Log database queries using Stackdriver") >> logging
    caching_instance >> Action("Retrieve cached data from Memcached") >> user
    terraform >> csv_storage
    terraform >> load_balancer
    terraform >> caching_instance
    terraform >> monitoring
    terraform >> logging
    terraform >> message_queue
    terraform >> argo
    argo >> k8s_cluster

