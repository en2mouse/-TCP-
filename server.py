import socket
import os

def receive_file(client_socket, save_path):
    try:
        # 接收文件名和文件大小
        filename, filesize = client_socket.recv(1024).decode().split('\n')
        filesize = int(filesize)
        print(f"接收文件：{filename}，大小：{filesize}字节")

        # 创建保存文件的路径
        save_file_path = os.path.join(save_path, filename)

        # 接收文件数据并保存到本地
        with open(save_file_path, 'wb') as file:
            received_size = 0
            while received_size < filesize:
                data = client_socket.recv(1024)
                file.write(data)
                received_size += len(data)

        print("文件接收完成")

    except Exception as e:
        print(f"文件传输失败：{str(e)}")


def send_file(client_socket, file_path):
    try:
        with open(file_path, 'rb') as file:
            filename = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            client_socket.send(f'{filename}\n{file_size}'.encode())
            while True:
                data = file.read(1024)
                if not data:
                    break
                client_socket.send(data)

        print("文件发送完成")

    except Exception as e:
        print(f"文件发送失败：{str(e)}")


def main():
    # 服务器IP地址和端口号
    server_ip = '127.0.0.1'
    server_port = 12345

    # 接收到的文件保存路径
    save_path = 'server_files'

    # 创建TCP套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.bind((server_ip, server_port))
        server_socket.listen(1)
        print("等待客户端连接...")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"客户端 {client_address} 连接成功")

            # 接收客户端请求
            request = client_socket.recv(1024).decode()
            print(request)
            if request == 'upload':
                # 处理上传文件请求
                receive_file(client_socket, save_path)
            elif request == 'download':
                
                # 处理下载文件请求
                file_path = client_socket.recv(1024).decode()

                print(f"客户端请求下载文件：{file_path}")
                send_file(client_socket, file_path)

            # 关闭客户端连接
            client_socket.close()

    except Exception as e:
        print(f"服务器发生错误：{str(e)}")

    finally:
        # 关闭套接字连接
        server_socket.close()


# 调用主函数
if __name__ == '__main__':
    main()
