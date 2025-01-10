FROM alpine:edge

# Install dapr CLI
RUN apk add --no-cache bash
ADD https://raw.githubusercontent.com/dapr/cli/master/install/install.sh /tmp/install.sh
RUN /bin/bash /tmp/install.sh

# Install daprd
ARG DAPR_BUILD_DIR
COPY $DAPR_BUILD_DIR /opt/dapr
ENV PATH="/opt/dapr/:${PATH}"
RUN dapr init --slim

# Install your app
WORKDIR /components
COPY redis-testcontainer-pubsub.yaml .

EXPOSE 3500
