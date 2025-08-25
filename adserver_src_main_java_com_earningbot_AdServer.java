package com.earningbot;

import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;

import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;

public class AdServer {
    public static void main(String[] args) throws IOException {
        HttpServer server = HttpServer.create(new InetSocketAddress(8080), 0);
        server.createContext("/ad", new AdHandler());
        server.setExecutor(null);
        server.start();
        System.out.println("Ad server running on port 8080...");
    }

    static class AdHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            String query = exchange.getRequestURI().getQuery();
            String token = null;
            String userId = null;

            if (query != null) {
                for (String param : query.split("&")) {
                    String[] pair = param.split("=");
                    if (pair[0].equals("token")) {
                        token = pair[1];
                    } else if (pair[0].equals("user_id")) {
                        userId = pair[1];
                    }
                }
            }

            String response;
            if (token != null && token.equals("0bc23fcccc35acd927d3e508222416b9")) {
                response = "{\"status\": \"success\", \"ad_url\": \"https://adsterra.com/popunder?user_id=" + userId + "\"}";
            } else {
                response = "{\"status\": \"error\", \"message\": \"Invalid token\"}";
            }

            exchange.getResponseHeaders().set("Content-Type", "application/json");
            exchange.sendResponseHeaders(200, response.length());
            OutputStream os = exchange.getResponseBody();
            os.write(response.getBytes());
            os.close();
        }
    }
}