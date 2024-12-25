import socket
import struct
import pickle
import numpy as np
import random

def generate_matrix(rows, cols):
    """
    Генерує матрицю випадкових чисел.
    """
    return np.random.randint(1, 100, size=(rows, cols))

def main():
    host = '127.0.0.1'  # Локальний сервер
    port = 65432        # Порт сервера

    # Генерація розмірів матриць
    N = random.randint(5, 10)
    M = random.randint(5, 10)
    L = random.randint(5, 10)

    # Генерація матриць
    matrix_a = generate_matrix(N, M)
    matrix_b = generate_matrix(M, L)
    print(f"Згенеровано матриці розмірами {N}x{M} та {M}x{L}")

    # Створення сокета
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        print("Підключено до сервера")

        # Відправка даних: розміри матриць та їх елементи
        data = {
            'matrix_a': matrix_a,
            'matrix_b': matrix_b,
            'shape_a': matrix_a.shape,
            'shape_b': matrix_b.shape
        }
        serialized_data = pickle.dumps(data)
        client_socket.sendall(struct.pack('!I', len(serialized_data)) + serialized_data)
        print("Матриці відправлено серверу")

        # Отримання результату
        header = client_socket.recv(4)
        result_length = struct.unpack('!I', header)[0]
        result_data = client_socket.recv(result_length)
        result_matrix = pickle.loads(result_data)

        print("Отримано результат від сервера:")
        print(result_matrix)

if __name__ == "__main__":
    main()
