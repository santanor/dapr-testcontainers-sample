# First stage: Build dependencies using Alpine
FROM dapr:integration AS builder

FROM processor:latest

USER root

RUN adduser --disabled-password --gecos '' nonroot

WORKDIR /app
ENV PYTHONPATH=/app

# Create a .sh file to run the python app. Dapr requires a shell command to run the app.
RUN echo '#!/bin/sh\n \
uvicorn app:app --host 0.0.0.0 --port 8001' > /run.sh

RUN chmod +x /run.sh

# Copy dependencies from the first stage
COPY --from=builder /usr/local/bin/dapr /usr/local/bin/dapr
COPY --from=builder /root/.dapr /home/nonroot/.dapr
COPY --from=builder /opt/dapr /opt/dapr
COPY --from=builder /components /components

USER nonroot

EXPOSE 8001

ENTRYPOINT ["dapr"]
CMD ["run", "--app-id", "order-processor", "--app-port", "8001", "--dapr-http-port", "3501", \
   "--resources-path", "/components", "--dapr-grpc-port", "50002", "--scheduler-host-address", "", "/run.sh" ]