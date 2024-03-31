import http.server
import http.client
import socketserver

PORT = 8502
DEST_PORT = 8501
DEST_HOST = 'localhost'  # 修改为 Streamlit 服务的主机地址，如果在不同的服务器上则为其 IP 地址

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # 创建到 Streamlit 服务的连接
        conn = http.client.HTTPConnection(DEST_HOST, DEST_PORT)
        # 转发 GET 请求
        conn.request("GET", self.path)
        # 获取响应
        response = conn.getresponse()
        # 发送响应状态
        self.send_response(response.status)
        # 发送响应头部
        for header in response.getheaders():
            self.send_header(*header)
        self.end_headers()
        # 发送响应内容
        self.wfile.write(response.read())

# 设置服务器地址和端口
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Forwarding requests from port {PORT} to port {DEST_PORT}...")
    # 启动服务
    httpd.serve_forever()
