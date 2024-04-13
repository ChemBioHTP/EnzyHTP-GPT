#!/bin/bash

pm2 start ./src/app.js --name "enzyhtp.web.node"
pm2 save
pm2 startup
