import tkinter as tk
from PIL import ImageTk, Image
from tkinter import filedialog
import socket
import os


def send_file(server_ip, server_port, file_path):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((server_ip, server_port))

        client_socket.send(b'upload')

        with open(file_path, 'rb') as file:
            filename = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            client_socket.send(f'{filename}\n{file_size}'.encode())

            while True:
                data = file.read(1024)
                if not data:
                    break
                client_socket.send(data)

        print("文件传输完成")

    except Exception as e:
        print(f"文件传输失败：{str(e)}")

    finally:
        client_socket.close()


def download_file(server_ip, server_port, file_path):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((server_ip, server_port))

        client_socket.send(b'download')

        confirmation = client_socket.recv(1024).decode()
        if confirmation == "download_request_received":
            client_socket.send(file_path.encode())

            filename, filesize = client_socket.recv(1024).decode().split('\n')
            filesize = int(filesize)
            print(f"接收文件：{filename}，大小：{filesize}字节")

            save_file_path = os.path.join("client_files", filename)

            with open(save_file_path, 'wb') as file:
                received_size = 0
                while received_size < filesize:
                    data = client_socket.recv(1024)
                    file.write(data)
                    received_size += len(data)

            print("文件下载完成")

    except Exception as e:
        print(f"文件下载失败：{str(e)}")

    finally:
        client_socket.close()


def open_upload_dialog():
    file_path = filedialog.askopenfilename(title="选择待上传的文件")
    if file_path:
        server_ip = server_ip_entry.get()
        server_port = int(server_port_entry.get())
        upload_entry.delete(0, tk.END)
        upload_entry.insert(tk.END, os.path.basename(file_path))
        send_file(server_ip, server_port, file_path)


def open_download_dialog():
    file_path = filedialog.askopenfilename(title="选择要下载的文件")
    if file_path:
        server_ip = server_ip_entry.get()
        server_port = int(server_port_entry.get())
        download_entry.delete(0, tk.END)
        download_entry.insert(tk.END, os.path.basename(file_path))
        download_file(server_ip, server_port, file_path)


# 创建主窗口
window = tk.Tk()
window.geometry("650x220")
window.title("文件传输程序客户端")

# 加载背景图像
image = Image.open("img.png")  # 替换为你的背景图片路径
bg_image = ImageTk.PhotoImage(image)

# 设置背景图像
background_label = tk.Label(window, image=bg_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# 创建服务器设置部分的控件
server_ip_label = tk.Label(window, text="服务器IP：")
server_ip_label.grid(row=0, column=0, padx=10, pady=5)

server_ip_entry = tk.Entry(window, width=30)
server_ip_entry.grid(row=0, column=1, padx=10, pady=5)

server_port_label = tk.Label(window, text="服务器端口：")
server_port_label.grid(row=0, column=2, padx=10, pady=5)

server_port_entry = tk.Entry(window, width=10)
server_port_entry.grid(row=0, column=3, padx=10, pady=5)

# 创建上传文件部分的控件
upload_button = tk.Button(window, text="选择文件上传", command=open_upload_dialog)
upload_button.grid(row=1, column=0, columnspan=4, padx=10, pady=5)

upload_entry = tk.Entry(window, width=50)
upload_entry.grid(row=2, column=0, columnspan=4, padx=10, pady=5)

# 创建下载文件部分的控件
download_button = tk.Button(window, text="选择文件下载", command=open_download_dialog)
download_button.grid(row=3, column=0, columnspan=4, padx=10, pady=5)

download_entry = tk.Entry(window, width=50)
download_entry.grid(row=4, column=0, columnspan=4, padx=10, pady=5)

window.mainloop()
