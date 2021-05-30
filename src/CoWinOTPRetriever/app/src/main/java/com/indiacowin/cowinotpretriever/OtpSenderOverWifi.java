package com.indiacowin.cowinotpretriever;

import android.util.Log;

import java.io.Closeable;
import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.nio.charset.Charset;

public class OtpSenderOverWifi implements Closeable {
    DatagramSocket server;
    int port;

    public OtpSenderOverWifi(int port) throws SocketException {
        this.port = port;
        server = new DatagramSocket(port);
        server.setSoTimeout(10000);
        server.setBroadcast(true);
    }

    public void sendOtp(String otp, String password) throws IOException {
        try {
            //broadcasting self details
            InetAddress addr = InetAddress.getByName("255.255.255.255");
            byte[] msg = String.format("%s::%s", password, otp).getBytes(Charset.defaultCharset());
            DatagramPacket data = new DatagramPacket(msg, msg.length, addr, port);
            server.send(data);
        } catch (IOException e) {
            Log.e("OtpSenderOverWifi", "Error in sending otp to laptop server", e);
            throw e;
        }
    }

    @Override
    public void close() throws IOException {
        server.close();
    }

    public void sendOtpWithRetry(String password, String otp, int retry) {
        new Thread(() -> {
            int remainingRetry = retry;
            while (remainingRetry > 0 ){
                remainingRetry--;
                try {
                    sendOtp(otp, password);
                    break;
                } catch (IOException e) {
                    // Do nothing
                }
            }
        }).start();
    }

}
