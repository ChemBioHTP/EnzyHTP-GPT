# Use Node 16 alpine as parent image
FROM node:16-alpine

# Set information.
ENV TZ "US/Central"
LABEL org.opencontainers.image.authors="Zhong, Yinjie"

# Change the working directory on the Docker image to /usr/src/app
WORKDIR /usr/src/app

# Copy package.json and package-lock.json to the /usr/src/app directory
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install --production
RUN npm install pm2 -g

# Copy the rest of project files into this image
COPY . .

# Set production environment.
ENV NODE_ENV=production

# Use PM2 to run the application.
CMD ["/bin/bash", "start_node_app.sh"]
