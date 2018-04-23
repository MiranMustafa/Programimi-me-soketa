import random
import socket
from datetime import datetime
import random

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
server_socket.bind(('', 11000));

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
        server_socket.sendto(str.encode("IP adresa e klientit eshte: " + addr[0]), addr);

    elif(kerkesaVarg[0]=='PORTNR'):
       server_socket.sendto(str.encode("Klienti është duke përdorur portin " + str(addr[1])), addr);

    elif(kerkesaVarg[0]=='ZANORE'):
        try:
            s=kerkesaVarg[1];           #ruajme fjaline ne nje string s
            count = 0;
            zanoret = set("aeiyou\u00EB");
            for letter in s:             #iterojme neper cdo shkronje te stringut
                if letter in zanoret:    #nese shkronja ne iterim gjindet tek zanoret rritet count
                    count += 1;
            server_socket.sendto(str.encode("Numri i zanoreve ne tekst eshte:" + str(count)), addr);
        except IndexError:
            server_socket.sendto(str.encode("Shenoni nje fjali pas kerkeses ZANORE!"), addr);

    elif(kerkesaVarg[0]=='PRINTO'):
        try:
            kerkesaVarg[1] = kerkesaVarg[1].strip();
            server_socket.sendto(str.encode("Fjalia e dhene per printim "+kerkesaVarg[1]), addr);
        except IndexError:
            server_socket.sendto(str.encode("Ju lutem shenoni nje fjali pas kerkeses PRINTO!"), addr);
            
    elif(kerkesaVarg[0]=='HOST'):
        try:
            hostname=socket.gethostname();
            server_socket.sendto(str.encode("Emri i hostit është "+hostname), addr);

        except error:
            server_socket.sendto(str.encode("Emri i hostit nuk dihet"), addr);

    elif(kerkesaVarg[0]=='TIME'):
        time=datetime.now().strftime('%Y-%m-%d %H:%M:%S');
        server_socket.sendto(str.encode(time), addr);
    elif(kerkesaVarg[0]=='LOJA'):
        srand= '';
        for x in range(20):
            rand= random.randint(1,100); #random number
            randString = str(rand) + " "; #converted to strig
            srand += randString;           #all random numbers in one string
        server_socket.sendto(str.encode(srand), addr);
    elif(kerkesaVarg[0]=='FIBONACCI'):
        try:
            print(int(kerkesaVarg[1]));
            n=fibonnaci(int(kerkesaVarg[1]));
            server_socket.sendto(str.encode(str(n)), addr);
        except IndexError:
            server_socket.sendto(str.encode("Shenoni nje numer pas kerkeses FIBONACCI"), addr);
        except ValueError:
            server_socket.sendto(str.encode("Shenoni nje numer pas kerkeses FIBONACCI"), addr);
    elif(kerkesaVarg[0]=='KONVERTO'):
        helpString1="Mundesite per konvertime:\nCelsiusToKelvin  \nCelsiusToFahrenheit  \nKelvinToFahrenheit \nKelvinToCelsius";
        helpString2="\nFahrenheitToCelsius \nFahrenheitToKelvin  \nPoundToKilogram  \nKilogramToPound";
        try:
            s=kerkesaVarg[1];
            n=float(kerkesaVarg[2]);
            server_socket.sendto(str.encode(str(konvertimi(s,n))), addr);
        except IndexError:        
            server_socket.sendto(str.encode("Ju lutem shenoni cka deshironi te konvertoni pastaj shifren! \n" +helpString1  + helpString2), addr);
        except ValueError:
            server_socket.sendto(str.encode("Ju lutem shenoni cka deshironi te konvertoni pastaj shifren!\n "+helpString1  + helpString2), addr);
    elif(kerkesaVarg[0]=='FUQIA'):
        try:
            baza= int(kerkesaVarg[1]);
            eksponenti = int(kerkesaVarg[2]);
            rezultati = pow(baza,eksponenti);
            server_socket.sendto(str.encode(str(rezultati)), addr);
        except IndexError:
            server_socket.sendto(str.encode("Shenoni bazen pastaj eksponentin pas kerkeses FUQIA"), addr);


    elif(kerkesaVarg[0]=='PRIME'):
        try:
            n = int(kerkesaVarg[1]);
            if is_prime(n):
                server_socket.sendto(str.encode("Numri " + str(n) + " eshte numer i thjeshte!"), addr);   
            else:
                server_socket.sendto(str.encode("Numri " + str(n) + " nuk eshte numer i thjeshte!"),addr);
        except IndexError:
            server_socket.sendto(str.encode("Shenoni nje numer pas kerkeses PRIME!"),addr);
        except ValueError:
            server_socket.sendto(str.encode("Shenoni nje numer te plote pas kerkeses PRIME!"),addr)
    else:
        server_socket.sendto(str.encode("Shenoni njeren nga kerkesat!"), addr);

while True:
    kerkesa, addr = server_socket.recvfrom(1024);
    kerkesa = kerkesa.decode('utf-8');
    kerkesaVarg= kerkesa.split();
    perpunimi_kerkeses(kerkesaVarg,server_socket,addr);
    