FROM python:3.12-slim

WORKDIR /app

COPY load_test/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY load_test/load_test.py ./
COPY proto /protos

RUN python -m grpc_tools.protoc \
    -I/protos \
    --python_out=/app \
    --grpc_python_out=/app \
    /protos/students.proto

ENV GRPC_SERVER=server:50051
ENV LOAD_USERS=80
ENV LOAD_REQUESTS_PER_USER=150
ENV LOAD_TIMEOUT=5

CMD ["python", "load_test.py"]
