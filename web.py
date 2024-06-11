<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ROS 2 Web Interface</title>
    <script type="text/javascript" src="http://cdn.robotwebtools.org/EventEmitter2/current/eventemitter2.min.js"></script>
    <script type="text/javascript" src="http://cdn.robotwebtools.org/roslibjs/current/roslib.min.js"></script>
    <script type="text/javascript">
        // Connect to ROS
        var ros = new ROSLIB.Ros({
            url: 'ws://YOUR_ROS2_SERVER_IP:9090' // Replace with your ROS 2 server IP
        });

        ros.on('connection', function () {
            console.log('Connected to ROS 2 server.');
        });

        ros.on('error', function (error) {
            console.log('Error connecting to ROS 2 server:', error);
        });

        ros.on('close', function () {
            console.log('Connection to ROS 2 server closed.');
        });

        // Subscribe to a ROS 2 topic
        var listener = new ROSLIB.Topic({
            ros: ros,
            name: '/your_topic_name',
            messageType: 'your_message_type' // Replace with the message type of your topic
        });

        listener.subscribe(function (message) {
            console.log('Received message:', message);
            // Update your web interface with the received message
        });

        // Publish teleoperation commands
        var cmdVel = new ROSLIB.Topic({
            ros: ros,
            name: '/cmd_vel',
            messageType: 'geometry_msgs/Twist'
        });

        function publishCommand(linearX, angularZ) {
            var twist = new ROSLIB.Message({
                linear: {
                    x: linearX,
                    y: 0.0,
                    z: 0.0
                },
                angular: {
                    x: 0.0,
                    y: 0.0,
                    z: angularZ
                }
            });
            cmdVel.publish(twist);
        }
    </script>
</head>
<body>
    <h1>ROS 2 Web Interface</h1>
    <!-- Your HTML content and controls here -->
    <button onclick="publishCommand(0.5, 0.0)">Forward</button>
    <button onclick="publishCommand(-0.5, 0.0)">Backward</button>
    <button onclick="publishCommand(0.0, 0.5)">Rotate Left</button>
    <button onclick="publishCommand(0.0, -0.5)">Rotate Right</button>
</body>
</html>
