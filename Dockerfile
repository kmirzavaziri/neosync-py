FROM golang:1.24.1-bullseye

# Install Python and other tools
RUN apt-get update && apt-get install -y \
    gcc \
    make \
    python3 \
    python3-pip \
    vim \
    && apt-get clean

# Set working directory
WORKDIR /app

# Copy everything from your repo
COPY . .

# Run make commands
RUN make neosync-exporter-build && \
    pip3 install pyyaml mysql-connector-python

CMD ["/bin/bash"]
