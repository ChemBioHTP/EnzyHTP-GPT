FROM node:slim

# Set information.
ENV TZ "US/Central"
LABEL org.opencontainers.image.authors="Zhong, Yinjie"

# Copy the current directory file to the working directory.
WORKDIR /usr/src/app
COPY . .

# Install the environment.
RUN npm install

# Set start command
CMD ["npm", "start"]
