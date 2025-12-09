# IP Metadata Database Performance Comparison
Cloud-based performance testing infrastructure comparing MySQL vs MongoDB for IP metadata lookups under varying workloads.

Project Overview
This project implements and benchmarks MySQL and MongoDB for storing and retrieving 50 million IP address geolocation records. The infrastructure uses Google Cloud Platform with auto-scaling, load balancing, and comprehensive monitoring to determine optimal database configurations under various workloads.

# Getting Started
Prerequisites
Google Cloud Platform account with billing enabled
gcloud CLI installed and authenticated: gcloud init
Python 3.8+ for scripts and analysis

## Clone Repository
bash
git clone https://github.com/sabrina-reis/cloud_computing_final.git
cd ip-database-performance

## Set GCP Project 
bash
export GCP_PROJECT_ID="your-project-id"
export GCP_REGION="us-central1"
export GCP_ZONE="us-central1-a"

gcloud config set project $GCP_PROJECT_ID

## Create K6, Grafana, MongoDB, and MySQL VMs
bash
./scripts/setup/create_vms.sh

## Get MongoDB and MySQL Databases with 50M Records From Cloud Storage
Note that sample data is already included in the k6-tests file.
bash
# Download pre-configured databases from Cloud Storage
bash 
./scripts/data/get_dataset.sh

## Import Data to Databases
bash
./scripts/setup/2_setup_mysql.sh
./scripts/setup/3_setup_mongodb.sh

## Create Load Balancers & Monitoring
bash
./scripts/setup/4_create_load_balancers.sh
./scripts/setup/5_setup_grafana.sh

## Build K6 with Database Extensions

### SSH into K6 VM
bash
gcloud compute ssh k6-testing-vm --zone=$GCP_ZONE

### Install Go
bash
sudo apt-get install -y golang-go

### Build K6 with SQL and MongoDB extensions
bash
go install go.k6.io/xk6/cmd/xk6@latest
xk6 build \
  --with github.com/grafana/xk6-sql@latest \
  --with github.com/grafana/xk6-sql-driver-mysql@latest \
  --with github.com/itsparser/xk6-mongo@latest

### Move to PATH
bash
sudo mv k6 /usr/local/bin/

### Verify That K6 Was Downloaded
k6 version

## Run Performance Tests On k6 VM
bash
cd ~/ip-database-performance
./k6 run k6-tests/mysql_constant.js --out json=results/mysql_constant.json
./k6 run k6-tests/mongodb_constant.js --out json=results/mongodb_constant.json

Public Bucket: gs://ip-database-public-snapshots/

Download Links
MySQL Backup: mysql_records.sql.gz
MongoDB Backup: mongodb_records.tar.gz
Sample IPs: sample_ips.json

Test Scenarios
- Constant load
- Stress test
- Spike test
- Soak test
Workload: YCSB Workload C (100% read operations, random IP lookups)

# Configuration
Auto-scaling Policy
Metric: CPU utilization
Target: 70% CPU
Min instances: 0
Max instances: 8
Cool-down: 60 seconds
VM Specifications
Database instances: e2-small (2 vCPU, 2 GB RAM)
K6 testing: e2-standard-4 (4 vCPU, 8 GB RAM)
Grafana monitoring: e2-micro (2 vCPU, 1 GB RAM)

Cleanup
To avoid ongoing charges, delete all resources:

bash
gcloud compute instances list
gcloud compute instance-groups managed list
gcloud compute forwarding-rules list
Manual cleanup if needed:

gcloud compute instance-groups managed delete mysql-mig --zone=us-central1-a
gcloud compute instance-groups managed delete mongodb-mig --zone=us-central1-a

gcloud compute forwarding-rules delete mysql-lb --region=us-central1
gcloud compute forwarding-rules delete mongodb-lb --region=us-central1

gcloud compute instances delete k6-testing-vm grafana-instance --zone=us-central1-a


