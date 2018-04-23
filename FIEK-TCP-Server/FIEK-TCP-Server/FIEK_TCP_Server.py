import socket
import sys
from _thread import *
from datetime import datetime
import random


host = ''
serverPort = 11000;
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
try:
    serverSocket.bind((host, serverPort));
except socket.error as e:
    print(str(e));

print('Serveri u startua ne localhost:'+str(serverPort));
serverSocket.listen(10);
print('Serveri eshte i gatshem te pranoj kerkesa');

#funksioni per llogaritjen e fibonnacit
def fibonnaci(n):  
   if n <= 1:
       return n;
   else:
       return(fibonnaci(n-1) + fibonnaci(n-2));

def konvertimi(s,n): #s - cka ne cka do te konvertohet , n- vlera qe do te konvertohet!
    if(s=="CelsiusToKelvin"):
        return n+273.15;
    elif(s=="CelsiusToFahrenheit"):
        #(°C × 9/5) + 32 = °F
        return (n*9/5 + 32);
    elif(s=="KelvinToFahrenheit"):
        #° F = 9/5 x (K - 273.15) + 32
        return (9/5 *(n-273.15) +32);
    elif(s=="KelvinToCelsius"):
        return n-273.15;
    elif(s=="FahrenheitToCelsius"):
        #(°F - 32) x 5/9 = °C 
        return ((n-32)*9/5);
    elif(s=="FahrenheitToKelvin"):
        #K = 5/9 x (° F - 32) + 273
        return (5/9 * (n-32) +273.15);
    elif(s=="PoundToKilogram"):
        #1kg=2.2pound
        return n/2.2;
    elif(s=="KilogramToPound"):
        #1kg=2.2pound
        return n*2.2;

def is_prime(n):
    x=True;
    for x in range(2,n):
        if n%x ==0:
            x=False;
            return x;
    return x;
        


#funksioni per perpunimin e kerkeses qe dergohet nga klienti.
def perpunimi_kerkeses(kerkesaVarg,conn,addr):
    if(kerkesaVarg[0]=='IPADDR'):
        conn.send(str.encode(" IP Adresa e klientit është:"+addr[0]));

    elif(kerkesaVarg[0]=='PORTNR'):
       conn.send(str.encode("Klienti është duke përdorur portin "+str(addr[1])));

    elif(kerkesaVarg[0]=='ZANORE'):
        try:
            s="";
            s=s.join(kerkesaVarg[1:]);          #ruajme fjaline ne nje string s
            count = 0;
            zanoret = set("aeiouy\u00EB");
            for letter in s:             #iterojme neper cdo shkronje te stringut
                if letter in zanoret:    #nese shkronja ne iterim gjindet tek zanoret rritet count
                    count += 1;
            conn.send(str.encode("Teksti i pranuar përmban "+ str(count) +" zanore"));
        except IndexError:
            conn.send(str.encode("Shenoni nje fjali pas kerkeses ZANORE!"));

    elif(kerkesaVarg[0]=='PRINTO'):
        try:
            s="";
            s=str.join(" " , kerkesaVarg[1:]);
            conn.send(str.encode("Fjalia e dhene per printim "+s));
        except IndexError:
            conn.send(str.encode("Ju lutem shenoni nje fjali pas kerkeses PRINTO"));
            
    elif(kerkesaVarg[0]=='HOST'):
        try:
            hostname=socket.gethostname();
            conn.send( str.encode("Emri i hostit është "+hostname));
        except error:
            conn.send(str.encode("Emri i hostit nuk dihet."))

    elif(kerkesaVarg[0]=='TIME'):
        time=datetime.now().strftime('%Y-%m-%d %H:%M:%S');
        conn.send(str.encode(time));
    elif(kerkesaVarg[0]=='LOJA'):
        srand= '';
        for x in range(20):
            rand= random.randint(1,100); #random number
            randString = str(rand) + " "; #converted to strig
            srand += randString;           #all random numbers in one string
        conn.send(str.encode(srand));
    elif(kerkesaVarg[0]=='FIBONACCI'):
        try:
            n=fibonnaci(int(kerkesaVarg[1]));
            conn.send(str.encode(str(n)));
        except IndexError:
            conn.send(str.encode("Ju lutem shenoni nje shifer pas kerkeses FIBONACCI")); 
        except ValueError:
            conn.send(str.encode("Ju lutem shenoni nje shifer pas kerkeses FIBONACCI"));
    elif(kerkesaVarg[0]=='KONVERTO'):
        helpString1="Mundesite per konvertime:\nCelsiusToKelvin  \nCelsiusToFahrenheit  \nKelvinToFahrenheit \nKelvinToCelsius";
        helpString2="\nFahrenheitToCelsius \nFahrenheitToKelvin  \nPoundToKilogram  \nKilogramToPound";
        try:
            s=kerkesaVarg[1];
            n=float(kerkesaVarg[2]);
            conn.send(str.encode(str(konvertimi(s,n))));
        except IndexError:
            conn.send(str.encode("Ju lutem shenoni cka deshironi te konvertoni pastaj shifren! \n"+helpString1+helpString2));
        except ValueError:
            conn.send(str.encode("Ju lutem shenoni cka deshironi te konvertoni pastaj shifren! \n" +helpString1+helpString2));

    elif(kerkesaVarg[0]=='FUQIA'):
        try:
            baza= int(kerkesaVarg[1]);
            eksponenti = int(kerkesaVarg[2]);
            rezultati = pow(baza,eksponenti);
            conn.send(str.encode(str(rezultati)));
        except IndexError:
            conn.send(str.encode("Shenoni bazen pastaj eksponentin pas kerkeses FUQIA"));

    elif(kerkesaVarg[0]=='PRIME'):
        try:
            n = int(kerkesaVarg[1]);
            if is_prime(n):
                conn.send(str.encode("Numri " + str(n) + " eshte numer i thjeshte!"));
            else:
                conn.send(str.encode("Numri " + str(n) + " nuk eshte numer i thjeshte!"));
        except IndexError:
            conn.send(str.encode("Shenoni nje numer pas kerkeses PRIME!"));
        except ValueError:
            conn.send(str.encode("Shenoni nje numer te plote pas kerkeses PRIME!"));

    else:
        conn.send(str.encode("Ju lutem shenoni njerat nga kerkesat!"));
    
def klient_thread(conn,addr):
    while True:
        try:
            data=conn.recv(1024);
            kerkesa = data.decode('utf-8');
            kerkesaVarg = kerkesa.split();
            try:
                perpunimi_kerkeses(kerkesaVarg,conn,addr);
            except IndexError:
                conn.send(str.encode("Kerkesa nuk eshte valide!"))
        except OSError:
            conn.close();
    conn.close();


while True: 
    connectionSocket, addr = serverSocket.accept();
    print('Klienti u lidh ne serverin %s me port %s' % addr);
    start_new_thread(klient_thread,(connectionSocket,addr,));





