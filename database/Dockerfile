# Use the official MySQL image as the base image
from mysql:5.7

# Create a directory for our MySQL scripts
RUN mkdir /docker-entrypoint-initdb.d

# Copy the schema, users, images SQL files into the container
COPY schema.sql /docker-entrypoint-initdb.d
COPY users.sql /docker-entrypoint-initdb.d
COPY images.sql /docker-entrypoint-initdb.d


# Set the working directory to /docker-entrypoint-initdb.d
WORKDIR /docker-entrypoint-initdb.d
