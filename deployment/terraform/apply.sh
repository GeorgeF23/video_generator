#!/bin/bash

terraform init
terraform apply -var-file=variables.tfvars