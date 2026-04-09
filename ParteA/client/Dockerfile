FROM python:3.12-slim

WORKDIR /app

COPY client/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY client/app.py client/db.py ./
COPY proto /protos

RUN python -m grpc_tools.protoc \
    -I/protos \
    --python_out=/app \
    --grpc_python_out=/app \
    /protos/students.proto

RUN mkdir -p /data

ENV CLIENT_DB_PATH=/data/client.db
ENV GRPC_SERVER=server:50051

CMD ["python", "app.py"]
