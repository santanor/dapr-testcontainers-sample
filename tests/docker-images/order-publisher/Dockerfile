# First stage: Build dependencies using Alpine
FROM dapr:integration AS builder

FROM publisher:latest

USER root

RUN adduser --disabled-password --gecos '' nonroot

WORKDIR /app
ENV PYTHONPATH=/app

# Create a .sh file to run the python app. Dapr requires a shell command to run the app.
RUN echo '#!/bin/sh\n \
uvicorn app:app --host 0.0.0.0 --port 8000' > /run.sh
RUN chmod +x /run.sh

# Copy dependencies from the first stage
COPY --from=builder /usr/local/bin/dapr /usr/local/bin/dapr
COPY --from=builder /root/.dapr /home/nonroot/.dapr
COPY --from=builder /opt/dapr /opt/dapr
COPY --from=builder /components /components

USER nonroot


ENTRYPOINT ["dapr"]
CMD ["run", "--app-id", "order-publisher", "--app-port", "8000", "--dapr-http-port", "3500", \
   "--resources-path", "/components", "--dapr-grpc-port", "50001",  \
   "--app-health-probe-interval", "1", "--app-health-probe-timeout", "1000", "--app-health-threshold", "10",\
   "--enable-app-health-check=true", "--placement-host-address", "dapr-placement:50005",\
   "--scheduler-host-address", "dapr-scheduler:50006", "/run.sh" ]