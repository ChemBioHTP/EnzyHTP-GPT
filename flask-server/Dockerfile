FROM continuumio/anaconda3:main

# Set the Time Zone.
ENV TZ "US/Central"

# Copy the current directory file to the working directory.
RUN mkdir -p /var/www/flask-server && cd /var/www/flask-server
WORKDIR /var/www/flask-server
ADD . /var/www/flask-server

# Set start command
CMD [ "/bin/bash", "start.sh" ]

# Other information
LABEL org.opencontainers.image.authors="Zhong, Yinjie"

# Configure the environment
RUN bash ./docker_env_config.sh
