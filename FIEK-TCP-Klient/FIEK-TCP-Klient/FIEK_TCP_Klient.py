import socket
import sys 
import select

#serverName = 'localhost';
serverName = input("Shenoni emrin e serverit:");
#serverPort = 11000;
Port = input("Shenoni portin:");
serverPort = int(Port);



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
s.connect((serverName,serverPort));
while True:
    print("-----------------------------------------------------------------------------------------------------")
    var=input("Zgjedhni njeren nga kerkesat: \n IPADDR\n PORTNR\n ZANORE\n PRINTO\n HOST\n TIME\n LOJA\n FIBONACCI\n"+
              " KONVERTO\n FUQIA\n PRIME\n" +
              " Ose shenoni 0 per ta mbyllyr programin\n ");
    var=var.strip(); 
    if len(var) > 128:
        print("Kerkesa nuk mund te jete me e gjate se 128 karaktere!");
        continue;
    if not var:
        print("Ju lutem shenoni nje kerkese!");
        continue;
    if var == "0":
        s.close();
        break;
    s.sendall(str.encode(var));
    data = s.recv(1024);
    data = data.decode('utf-8');
    print(data);
