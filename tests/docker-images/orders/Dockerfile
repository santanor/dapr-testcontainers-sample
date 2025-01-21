# We can reuse the entire image if we just parameterize some of the values
# In more complex scenarios this might not be enough, or maintainable
ARG image

# First stage: Build dependencies using Alpine
FROM dapr:integration AS builder

FROM $image 

USER root

RUN adduser --disabled-password --gecos '' nonroot

WORKDIR /app
ENV PYTHONPATH=/app

# Copy dependencies from the first stage
COPY --from=builder /usr/local/bin/dapr /usr/local/bin/dapr
COPY --from=builder /root/.dapr /home/nonroot/.dapr
COPY --from=builder /opt/dapr /opt/dapr
COPY --from=builder /components /components

COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh

USER nonroot

ENTRYPOINT ["/app/run.sh"]