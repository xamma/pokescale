FROM python:3.13-slim

RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup --no-create-home appuser

WORKDIR /app

COPY src/requirements-pinned.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY src/main/ /app/

USER appuser

EXPOSE 8000

ENTRYPOINT ["python", "api.py"]