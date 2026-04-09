import os
import time

import grpc

import students_pb2
import students_pb2_grpc
from db import init_db, upsert_students


def sync_students() -> None:
    init_db()

    server_target = os.getenv("GRPC_SERVER", "server:50051")
    retries = int(os.getenv("CLIENT_RETRIES", "20"))
    retry_interval = float(os.getenv("CLIENT_RETRY_INTERVAL", "1.5"))

    for attempt in range(1, retries + 1):
        try:
            with grpc.insecure_channel(server_target) as channel:
                stub = students_pb2_grpc.StudentServiceStub(channel)
                response = stub.ListStudents(students_pb2.Empty(), timeout=10)

            total = upsert_students(response.students)
            print(f"Synchronization completed. {total} students stored in client database.")
            return
        except grpc.RpcError as exc:
            print(f"Attempt {attempt}/{retries} failed: {exc}")
            if attempt == retries:
                raise
            time.sleep(retry_interval)


if __name__ == "__main__":
    sync_students()
