package main;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.SocketException;
import java.net.UnknownHostException;

public class PhoneMockup 
{	
	private DatagramSocket sock;
	private DatagramPacket pack;
	
	public PhoneMockup() throws IOException
	{
		byte[] msg = new byte[20];
		sock = new DatagramSocket(1200);
		pack = new DatagramPacket(msg, 20);
		System.out.println("Waiting for IP");
		sock.receive(pack);
		System.out.println("Pack recieved");
		StringBuilder sb = new StringBuilder();
		for(int i = 0; i < pack.getLength(); i++)
			sb.append((char)pack.getData()[i]);
		String his = sb.toString();
		System.out.println(his);
		
		System.out.println("Sending IP");
		String mine = InetAddress.getLocalHost().getHostAddress().toString() + "\n";
		System.out.println(mine);
		
		System.out.println(mine.getBytes().length);
		for(int i = 0; i < mine.getBytes().length; i++)
			System.out.print("(" + mine.getBytes()[i] + ", " + (char)mine.getBytes()[i] + ") ");
		pack = new DatagramPacket(mine.getBytes(), mine.getBytes().length, InetAddress.getByName(his), 1200);
		sock.send(pack);
		
		sock.close();
		
		ServerSocket ss = new ServerSocket(1200);
		System.out.println("Listening");
		Socket s = ss.accept();
		System.out.println("connection accepted");
		PrintWriter out;
		BufferedReader in;
		out =new PrintWriter(s.getOutputStream(), true);
		in = new BufferedReader(new InputStreamReader(s.getInputStream()));
		while(true)
		{
			String message = in.readLine();
			System.out.println(message);
		}
		
		
	}

	public static void main(String[] args) throws IOException
	{
		new PhoneMockup();
		System.out.println();

	}

}
