# Use an official hashicorp/packer base image
FROM hashicorp/packer:latest

# Optionally, you can install additional tools or dependencies if needed
# For example, installing jq for JSON parsing
RUN apk add --no-cache jq

# Set the working directory
WORKDIR /app

# Copy Packer configuration files into the container
COPY . /app

# Define the entrypoint to Packer
ENTRYPOINT ["packer"]

# Default command to run when no command is specified
CMD ["--version"]
