#!/bin/bash

# Build the project if necessary
RUN npm run build

# Use pm2 to run the server.
pm2-runtime start node_server.js --name "enzyhtp.web.node"
