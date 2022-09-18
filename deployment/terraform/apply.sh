#!/bin/bash

cd deployment/terraform
terraform init
terraform apply -var-file=variables.tfvars
terraform output > ../environment.properties
cd ..