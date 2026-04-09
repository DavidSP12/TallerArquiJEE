import math
import os
import statistics
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import grpc

import students_pb2
import students_pb2_grpc


def worker(target: str, requests_count: int, timeout: float):
    latencies_ms = []
    ok = 0
    failed = 0

    # Cada worker usa un canal propio y manda sus requests de forma secuencial.
    # El paralelismo total lo da el ThreadPoolExecutor con varios workers a la vez.
    with grpc.insecure_channel(target) as channel:
        stub = students_pb2_grpc.StudentServiceStub(channel)

        for _ in range(requests_count):
            start = time.perf_counter()
            try:
                response = stub.ListStudents(students_pb2.Empty(), timeout=timeout)
                _ = len(response.students)
                ok += 1
            except grpc.RpcError:
                failed += 1
            finally:
                elapsed = (time.perf_counter() - start) * 1000
                latencies_ms.append(elapsed)

    return latencies_ms, ok, failed


def percentile(values, p: float) -> float:
    if not values:
        return 0.0
    if len(values) == 1:
        return values[0]

    sorted_vals = sorted(values)
    index = (len(sorted_vals) - 1) * p
    low = math.floor(index)
    high = math.ceil(index)

    if low == high:
        return sorted_vals[low]

    weight = index - low
    return sorted_vals[low] * (1 - weight) + sorted_vals[high] * weight


def main() -> None:
    target = os.getenv("GRPC_SERVER", "server:50051")
    users = int(os.getenv("LOAD_USERS", "50"))
    requests_per_user = int(os.getenv("LOAD_REQUESTS_PER_USER", "100"))
    timeout = float(os.getenv("LOAD_TIMEOUT", "5"))

    print(f"Iniciando la prueba de carga contra {target}")
    print(f"Usuarios: {users} | Solicitudes por usuario: {requests_per_user}")

    started = time.perf_counter()
    all_latencies = []
    ok_total = 0
    failed_total = 0

    with ThreadPoolExecutor(max_workers=users) as executor:
        futures = [
            executor.submit(worker, target, requests_per_user, timeout)
            for _ in range(users)
        ]

        for future in as_completed(futures):
            latencies, ok, failed = future.result()
            all_latencies.extend(latencies)
            ok_total += ok
            failed_total += failed

    duration = time.perf_counter() - started
    total_requests = ok_total + failed_total

    print("=== Resultado de la prueba de carga ===")
    print(f"Duración (s): {duration:.3f}")
    print(f"Total de solicitudes: {total_requests}")
    print(f"Exitosas: {ok_total}")
    print(f"Fallidas: {failed_total}")
    print(f"Tasa de éxito (%): {(ok_total / total_requests * 100) if total_requests else 0:.2f}")
    print(f"RPS: {(total_requests / duration) if duration else 0:.2f}")

    if all_latencies:
        print(f"Latencia mínima (ms): {min(all_latencies):.2f}")
        print(f"Latencia promedio (ms): {statistics.mean(all_latencies):.2f}")
        print(f"Latencia p50 (ms): {percentile(all_latencies, 0.50):.2f}")
        print(f"Latencia p95 (ms): {percentile(all_latencies, 0.95):.2f}")
        print(f"Latencia p99 (ms): {percentile(all_latencies, 0.99):.2f}")
        print(f"Latencia máxima (ms): {max(all_latencies):.2f}")


if __name__ == "__main__":
    main()
