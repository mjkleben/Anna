
import socket

def client():
  host = "192.168.0.199"  # get local machine name
  port = 8100  # Make sure it's within the > 1024 $$ <65535 range
  
  print(host)
  s = socket.socket()
  s.connect((host, port))
  
  while True:
    s.send(raw_input("ENTER SOMETHING:"))
  s.close()

if __name__ == '__main__':
    client()