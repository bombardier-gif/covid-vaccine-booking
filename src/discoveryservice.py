import socket
import time
import re
import otp_info

# import thread module
from _thread import *


OTP_PAT = re.compile(r'\b\d{6}\b')


def bind_udp_socket():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to listen all broadcast packet on the port 10041
    server_address = ('', 10041)
    print('starting udp server on %s port %s' % server_address)
    sock.bind(server_address)

    return sock


def receive_otp_from_mobile(sock, password):
    while True:
        print('\n waiting to receive message from mobile')
        data, address = sock.recvfrom(4096)

        print('\n received %s bytes from %s' % (len(data), address))
        print(data)

        if data:

            passwd_from_phone, otp_msg = data.decode('utf-8').split("::")
            if passwd_from_phone == password:
                print('received otp from mobile successfully : %s' % otp_msg)
                otp_info.last_otp_msg_received = otp_msg
                otp_info.last_otp_received_time = time.time()

                if m := OTP_PAT.search(otp_msg):
                    otp_info.last_otp_received = m.group()
                else:
                    print('Unable to identify otp from sms')
            else:
                print('unknown mobile is trying to connect. Data received : %s, Otp received : %s,  Ignoring this data ...' % (data, otp_msg))


def start_receiving_otp(password):
    otp_info.init()
    sock = bind_udp_socket()
    start_new_thread(receive_otp_from_mobile, (sock, password,))


def get_otp(otp_trigger_time):
    # try to read OTP for atmost 3 minutes after trigger time, because after 3 minute otp will expire
    t_end = otp_trigger_time + 60 * 3
    while time.time() < t_end:
        if otp_info.last_otp_received_time > otp_trigger_time:
            print('Otp found : %s' % otp_info.last_otp_received)
            return otp_info.last_otp_received
        else:
            print('No otp received Yet. Sleeping for 1 seconds before rechecking...')
            time.sleep(1)
    return None


# Testing for receiver
def main():
    start_receiving_otp("1234")
    while True:
        get_otp(time.time())


if __name__ == '__main__':
    main()