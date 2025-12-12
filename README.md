# Project Overview
This project implements and benchmarks MySQL and MongoDB for storing and retrieving 50 million IP address geolocation records. The infrastructure uses Google Cloud Platform with auto-scaling, load balancing, and comprehensive monitoring to assess database performance under various workloads and profile cost-performance tradeoffs in horizontal scaling.

# Getting Started
Prerequisites
- Google Cloud Platform account with billing enabled
- gcloud CLI installed and authenticated: gcloud init
- Python 3.8+ for scripts and analysis

# Setup
- Clone repo
- Navigate to repo directory
- Run setup script
```bash
./bootstrap.sh
```

The bootstrap script performs the following tasks:
- Creates MySQL and MongoDB VM instances
- Creates managed instance groups for MySQL and MongoDB
- Creates VM for k6 testing
- Creates VM for Grafana and sets up Grafana
- Imports  pre-built database snapshots onto MySQL and MongoDB VM instances
- Sets up MySQL and MongoDB on the VM instances
- Makes a template for the MySQL and MongoDB VM instances
- Sets up the load balancers

# Begin testing
Tests Available
- Constant load
- Stress test
- Spike test
- Soak test
Workload: YCSB Workload C (100% read operations, random IP lookups)

To run a test, use the format
```bash
k6 run /path/to/test/file
```

For more information on the tests, see cloud_computing_report.pdf.

# Configuration
Auto-scaling Policy
- Metric: CPU utilization
- Target: 70% CPU
- Min instances: 0
- Max instances: 8
- Cool-down: 60 seconds
  
VM Specifications
- Database instances: e2-small (2 vCPU, 2 GB RAM)
- K6 testing: e2-standard-4 (4 vCPU, 8 GB RAM)
- Grafana monitoring: e2-micro (2 vCPU, 1 GB RAM)

For more information on the architecture, see cloud_computing_report.pdf.

# Cleanup
To avoid ongoing charges, delete all resources:

```bash
gcloud compute instances list
gcloud compute instance-groups managed list
gcloud compute forwarding-rules list
Manual cleanup if needed:

gcloud compute instance-groups managed delete mysql-mig --zone=us-central1-a
gcloud compute instance-groups managed delete mongodb-mig --zone=us-central1-a

gcloud compute forwarding-rules delete mysql-lb --region=us-central1
gcloud compute forwarding-rules delete mongodb-lb --region=us-central1

gcloud compute instances delete k6-testing-vm grafana-instance --zone=us-central1-a










