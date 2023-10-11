#!/bin/zsh
aws lightsail create-container-service-deployment \
    --region us-west-2 \
    --cli-input-json file://local-container.json
