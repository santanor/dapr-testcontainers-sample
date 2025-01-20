# First stage: Build dependencies using Alpine
FROM dapr:integration AS builder

# We can reuse the entire image if we just parameterize some of the values
# In more complex scenarios this might not be enough, or maintainable
ARG image
ARG port
ARG app_id
ARG dapr_http_port
ARG dapr_grpc_port

FROM ${image}

USER root

RUN adduser --disabled-password --gecos '' nonroot

WORKDIR /app
ENV PYTHONPATH=/app

# Create a .sh file to run the python app. Dapr requires a shell command to run the app.
RUN echo '#!/bin/sh\n \
uvicorn app:app --host 0.0.0.0 --port ${port}' > /run.sh

RUN chmod +x /run.sh

# Copy dependencies from the first stage
COPY --from=builder /usr/local/bin/dapr /usr/local/bin/dapr
COPY --from=builder /root/.dapr /home/nonroot/.dapr
COPY --from=builder /opt/dapr /opt/dapr
COPY --from=builder /components /components

USER nonroot
EXPOSE ${port}

ENTRYPOINT ["dapr"]
CMD ["run", "--app-id", "${app_id}", "--app-port", "${port}", "--dapr-http-port", "${dapr_http_port}", \
   "--resources-path", "/components", "--dapr-grpc-port", "${dapr_grpc_port}", "--scheduler-host-address", "", "/run.sh" ]