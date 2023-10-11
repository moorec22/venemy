#!/bin/zsh
aws lightsail push-container-image \
    --region us-west-2 \
    --service-name venemy-server \
    --label latest \
    --image venemy-server
