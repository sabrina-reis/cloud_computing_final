# IP Metadata Database Performance Comparison
Cloud-based performance testing infrastructure comparing MySQL vs MongoDB for IP metadata lookups under varying workloads.

Project Overview
This project implements and benchmarks MySQL and MongoDB for storing and retrieving 50 million IP address geolocation records. The infrastructure uses Google Cloud Platform with auto-scaling, load balancing, and comprehensive monitoring to determine optimal database configurations under various workloads.

# Getting Started
Prerequisites
Google Cloud Platform account with billing enabled
gcloud CLI installed and authenticated: gcloud init
Python 3.8+ for scripts and analysis

# Run setup script
./bootstrap.sh

# Begin testing

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

# Cleanup
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


