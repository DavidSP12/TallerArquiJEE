FROM python:3.12-slim

WORKDIR /app

COPY server/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY server/app.py server/db.py ./
COPY proto /protos

RUN python -m grpc_tools.protoc \
    -I/protos \
    --python_out=/app \
    --grpc_python_out=/app \
    /protos/students.proto

RUN mkdir -p /data

ENV SERVER_DB_PATH=/data/server.db
ENV GRPC_PORT=50051

EXPOSE 50051

CMD ["python", "app.py"]
