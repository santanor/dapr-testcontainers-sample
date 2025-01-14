# First stage: Build dependencies using Alpine
FROM dapr:integration AS builder

FROM processor:latest

USER root

WORKDIR /app
ENV PYTHONPATH=/app

# Copy dependencies from the first stage
COPY --from=builder /usr/local/bin/dapr /usr/local/bin/dapr
COPY --from=builder /root/.dapr /home/nonroot/.dapr
COPY --from=builder /opt/dapr /opt/dapr
COPY --from=builder /components /components

EXPOSE 8001
EXPOSE 3500

ENTRYPOINT ["dapr"]
CMD ["run", "--app-id", "order-processor", "--app-port", "50051", "--dapr-http-port", "3501", \
   "--resources-path", "/components", "--dapr-grpc-port", "50002", "--app-protocol", "grpc", \
   "--app-health-probe-interval", "1", "--app-health-probe-timeout", "1000", "--app-health-threshold", "10",\
   "--enable-app-health-check=true", "--placement-host-address", "dapr-placement:50005",\
   "--scheduler-host-address", "dapr-scheduler:50006"]