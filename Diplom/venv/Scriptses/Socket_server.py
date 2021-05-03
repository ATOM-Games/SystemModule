import socket, cv2, pickle, struct


#def createSocket(c_ip, c_pt):
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
    #host_ip = c_ip
port = 5001
    #port = c_pt
socket_address = (host_ip, port)
server_socket.bind(socket_address)
server_socket.listen(5)
print("Listen : socket address ", socket_address)
while True:
    client_socket,addr = server_socket.accept()
    print("GOT CONNECTION : ", addr)
    if client_socket:
        vid = cv2.VideoCapture(0)
        while (vid.isOpened()):
            img,frame = vid.read()
            a = pickle.dumps(frame)
            message = struct.pack("Q", len(a)) + a