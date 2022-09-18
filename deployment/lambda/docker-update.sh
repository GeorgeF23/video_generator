#!/bin/bash

file="deployment/environment.properties"
if [ -f "$file" ]; then 
	echo "Using environment properties from file: $file"
	while IFS=' = ' read -r key value
	do
		eval ${key}=$(echo $value | tr -d \"  )
	echo "  $key = $value"
	done < "$file"

	aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin 787778819105.dkr.ecr.eu-central-1.amazonaws.com

	docker build . -t $ecr_name -f deployment/lambda/Dockerfile
	docker tag $ecr_name:latest $ecr_url:latest
	docker push $ecr_url:latest
fi