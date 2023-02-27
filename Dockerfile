FROM ubuntu:18.04

ARG DEBIAN_FRONTEND=noninteractive
ARG NODE_VERSION="v17.0.1"
ARG SOLANA_CLI_VERSION="stable"
ARG ANCHOR_CLI="latest"
# Set the environment variables
ENV HOME="/root"

# Update the package repository and install essential packages
RUN apt-get update && \
    apt-get install -y curl git libssl-dev libudev-dev pkg-config zlib1g-dev build-essential

# Install Node.js and Yarn using NVM (Node Version Manager) 
# and set the default version to ${NODE_VERSION}
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
ENV NVM_DIR="${HOME}/.nvm"
RUN . $NVM_DIR/nvm.sh && \
    nvm install ${NODE_VERSION} && \
    nvm use ${NODE_VERSION} && \
    nvm alias default node && \
    npm update -g npm && \
    npm install -g yarn
ENV PATH="${HOME}/.nvm/versions/node/${NODE_VERSION}/bin:${PATH}"

# Install Solana
RUN sh -c "$(curl -sSfL https://release.solana.com/$SOLANA_CLI_VERSION/install)"
ENV RUSTUP_HOME="${HOME}/.rustup"
ENV CARGO_HOME="${HOME}/.cargo"
ENV PATH="${HOME}/.local/share/solana/install/active_release/bin:${PATH}"

# Install Rust
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y --profile minimal
ENV PATH="${HOME}/.cargo/bin:${PATH}"

# Install Anchor
RUN cargo install --git https://github.com/project-serum/anchor avm --locked --force

RUN avm install ${ANCHOR_CLI}
RUN avm use ${ANCHOR_CLI}

# Set the working directory to /app
WORKDIR /app

# Start a bash shell in the container
CMD ["/bin/bash", && tail -f /dev/null]
