from socketserver import TCPServer, ThreadingTCPServer
import socket


class HTTPServer(TCPServer):
    allow_reuse_address = 1  # Seems to make sense in testing environment

    def server_bind(self):
        """Override server_bind to store the server name."""
        TCPServer.server_bind(self)
        host, port = self.server_address[:2]
        self.server_name = socket.getfqdn(host)
        self.server_port = port


class ThreadHTTPServer(ThreadingTCPServer):
    allow_reuse_address = 1  # Seems to make sense in testing environment

    def server_bind(self):
        """Override server_bind to store the server name."""
        ThreadingTCPServer.server_bind(self)
        host, port = self.server_address[:2]
        self.server_name = socket.getfqdn(host)
        self.server_port = port

