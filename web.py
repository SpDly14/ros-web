import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import json
import asyncio
import websockets
from http.server import SimpleHTTPRequestHandler, HTTPServer
import threading

class Nav2WebSocketServer(Node):
    def __init__(self):
        super().__init__('nav2_websocket_server')
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.create_websocket_server()

    async def create_websocket_server(self, websocket, path):
        print("WebSocket connection established")
        try:
            async for message in websocket:
                try:
                    command = json.loads(message)
                    # Assuming 'command' is a JSON object containing navigation commands
                    # Process the command and control Nav2 accordingly
                    # Example:
                    linear_x = command.get('linear_x', 0.0)
                    angular_z = command.get('angular_z', 0.0)
                    twist_msg = Twist()
                    twist_msg.linear.x = linear_x
                    twist_msg.angular.z = angular_z
                    self.publisher.publish(twist_msg)
                except Exception as e:
                    print("Error processing command:", e)
        except websockets.exceptions.ConnectionClosedOK:
            print("WebSocket connection closed")

def serve_http():
    # Serve the HTML content
    Handler = SimpleHTTPRequestHandler
    with HTTPServer(('0.0.0.0', 8000), Handler) as httpd:
        print("HTTP server started on port 8000")
        httpd.serve_forever()

def main(args=None):
    rclpy.init(args=args)
    nav2_websocket_server = Nav2WebSocketServer()
    
    # Start the HTTP server in a separate thread
    http_thread = threading.Thread(target=serve_http)
    http_thread.start()

    try:
        start_server = websockets.serve(nav2_websocket_server.create_websocket_server, '0.0.0.0', 9090)
        asyncio.get_event_loop().run_until_complete(start_server)
        print("WebSocket server listening on port 9090")
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        pass
    nav2_websocket_server.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
