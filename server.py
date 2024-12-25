import socket
import struct
import pickle
import numpy as np
from concurrent.futures import ThreadPoolExecutor

def multiply_matrices(matrix_a, matrix_b):
    """
    Паралельне множення матриць за допомогою ThreadPoolExecutor.
    """
    def multiply_row(row):
        return np.dot(row, matrix_b)

    with ThreadPoolExecutor() as executor:
        result = list(executor.map(multiply_row, matrix_a))
    return np.array(result)

def handle_client(client_socket):
    """
    Обробляє клієнтський запит.
    """
    try:
        # Отримання довжини даних
        header = client_socket.recv(4)
        data_length = struct.unpack('!I', header)[0]

        # Отримання даних
        data = client_socket.recv(data_length)
        matrices = pickle.loads(data)

        matrix_a = matrices['matrix_a']
        matrix_b = matrices['matrix_b']

        # Перевірка коректності розмірів матриць
        if matrix_a.shape[1] != matrix_b.shape[0]:
            response = "Error: Matrix dimensions do not match for multiplication"
            response_data = pickle.dumps(response)
            client_socket.sendall(struct.pack('!I', len(response_data)) + response_data)
            return

        # Множення матриць
        result = multiply_matrices(matrix_a, matrix_b)

        # Відправка результату назад клієнту
        serialized_result = pickle.dumps(result)
        client_socket.sendall(struct.pack('!I', len(serialized_result)) + serialized_result)

    except Exception as e:
        print(f"Помилка: {e}")
    finally:
        client_socket.close()

def main():
    # Параметри сервера
    host = '0.0.0.0'  # Слухає всі IP
    port = 65432

    # Створення сокета
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Сервер запущено на {host}:{port}")

    while True:
        # Приймаємо з'єднання
        client_socket, client_address = server_socket.accept()
        print(f"З'єднання з {client_address}")

        # Обробка клієнта в окремому потоці
        handle_client(client_socket)

if __name__ == "__main__":
    main()
