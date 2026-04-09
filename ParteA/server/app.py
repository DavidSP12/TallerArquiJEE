from concurrent import futures
import os

import grpc

import students_pb2
import students_pb2_grpc
from db import init_db, fetch_students


class StudentService(students_pb2_grpc.StudentServiceServicer):
    def ListStudents(self, request, context):
        students = fetch_students()
        response = students_pb2.StudentList()

        for student in students:
            response.students.add(
                id=student["id"],
                first_name=student["first_name"],
                last_name=student["last_name"],
                email=student["email"],
                major=student["major"],
            )

        return response


def serve() -> None:
    init_db()

    port = os.getenv("GRPC_PORT", "50051")
    max_workers = int(os.getenv("GRPC_MAX_WORKERS", "10"))

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    students_pb2_grpc.add_StudentServiceServicer_to_server(StudentService(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()

    print(f"gRPC server listening on port {port}")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
