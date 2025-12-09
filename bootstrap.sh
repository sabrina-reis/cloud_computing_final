#!/bin/bash
# bootstrap.sh
# Sets up VMs, databases, load balancers, Grafana, and builds k6 for reproducible tests

set -e  # exit on error

# 1. Set environment variables
export GCP_PROJECT_ID="your-project-id"
export GCP_REGION="us-central1"
export GCP_ZONE="us-central1-a"

gcloud config set project $GCP_PROJECT_ID

# 2. Create VMs
echo "Creating VMs..."

# MySQL and MongoDB instances (auto-scaling MIGs)
gcloud compute instance-templates create mysql-template \
    --machine-type=e2-small \
    --image-family=debian-11 \
    --image-project=debian-cloud \
    --metadata=startup-script='#! /bin/bash
      sudo apt-get update && sudo apt-get install -y mysql-server'

gcloud compute instance-templates create mongodb-template \
    --machine-type=e2-small \
    --image-family=debian-11 \
    --image-project=debian-cloud \
    --metadata=startup-script='#! /bin/bash
      sudo apt-get update && sudo apt-get install -y mongodb'

# Managed instance groups
gcloud compute instance-groups managed create mysql-mig \
    --template=mysql-template --size=1 --zone=$GCP_ZONE

gcloud compute instance-groups managed create mongodb-mig \
    --template=mongodb-template --size=1 --zone=$GCP_ZONE

# k6 VM
gcloud compute instances create k6-testing-vm \
    --zone=$GCP_ZONE \
    --machine-type=e2-standard-4 \
    --image-family=debian-11 \
    --image-project=debian-cloud

# Grafana VM
gcloud compute instances create grafana-instance \
    --zone=$GCP_ZONE \
    --machine-type=e2-micro \
    --image-family=debian-11 \
    --image-project=debian-cloud

# 3. Import pre-built database snapshots
echo "Downloading database snapshots..."
mkdir -p ~/ip-database-performance/data
gsutil cp gs://ip-database-public-snapshots/mysql_records.sql.gz ~/ip-database-performance/data/
gsutil cp gs://ip-database-public-snapshots/mongodb_records.tar.gz ~/ip-database-performance/data/

# 4. Set Up MySQL
echo "Setting up MySQL..."
gcloud compute ssh mysql-instance-1 --zone=$GCP_ZONE --command="
  gunzip -c ~/ip-database-performance/data/mysql_records.sql.gz | sudo mysql
"

# 5. Set Up MongoDB
echo "Setting up MongoDB..."
gcloud compute ssh mongodb-instance-1 --zone=$GCP_ZONE --command="
  mkdir -p ~/mongodb_data &&
  tar -xvf ~/ip-database-performance/data/mongodb_records.tar.gz -C ~/mongodb_data &&
  mongorestore ~/mongodb_data
"

# 6. Build k6 with Extensions
echo "Building k6 with SQL and Mongo extensions..."
gcloud compute ssh k6-testing-vm --zone=$GCP_ZONE --command="
  sudo apt-get update && sudo apt-get install -y golang-go git
  go install go.k6.io/xk6/cmd/xk6@latest
  xk6 build \
    --with github.com/grafana/xk6-sql@latest \
    --with github.com/grafana/xk6-sql-driver-mysql@latest \
    --with github.com/itsparser/xk6-mongo@latest
  sudo mv k6 /usr/local/bin/
"

# 7. Set Up Grafana
echo "Setting up Grafana..."
gcloud compute ssh grafana-instance --zone=$GCP_ZONE --command="
  sudo apt-get update &&
  sudo apt-get install -y grafana &&
  sudo systemctl enable grafana-server &&
  sudo systemctl start grafana-server
"

# 8. Set Up Load Balancers
echo "Creating Load Balancers..."
# Example for MySQL
gcloud compute forwarding-rules create mysql-lb \
    --region=$GCP_REGION \
    --ports=3306 \
    --target-pool=mysql-pool || echo "Target pool must be pre-created"

# 9. Instructions for running k6 tests
echo "Bootstrap complete! Run your tests on the k6 VM:"
echo "ssh into k6-testing-vm and run:"
echo "cd ~/ip-database-performance"
echo "./k6 run k6-tests/mysql_constant.js --out json=results/mysql_constant.json"
echo "./k6 run k6-tests/mongodb_constant.js --out json=results/mongodb_constant.json"
