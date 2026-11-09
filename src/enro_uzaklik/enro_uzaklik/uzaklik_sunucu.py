import math

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import Float64

from enro_interfaces.srv import UzaklikKontrol


class UzaklikSunucu(Node):

    def __init__(self):
        super().__init__('uzaklik_sunucu')
        # Topic where the distance is published after every successful request
        self.publisher = self.create_publisher(Float64, '/enro/hedef_uzakligi', 10)
        # Service that the client calls; check_distance runs for every request
        self.service = self.create_service(
            UzaklikKontrol, '/enro/uzaklik_kontrol', self.check_distance)
        self.get_logger().info('Service /enro/uzaklik_kontrol is ready')

    def check_distance(self, request, response):
        self.get_logger().info(
            f'Request: robot=({request.robot_x}, {request.robot_y}) '
            f'target=({request.hedef_x}, {request.hedef_y}) '
            f'threshold={request.yakinlik_esigi_m} m')

        # nan and inf are not valid positions or thresholds
        values = [request.robot_x, request.robot_y,
                  request.hedef_x, request.hedef_y, request.yakinlik_esigi_m]
        for value in values:
            if not math.isfinite(value):
                return self.error_response(response, 'all values must be finite numbers')

        if request.yakinlik_esigi_m <= 0:
            return self.error_response(response, 'yakinlik_esigi_m must be greater than 0')

        # Straight-line distance between the robot and the target
        dx = request.hedef_x - request.robot_x
        dy = request.hedef_y - request.robot_y
        distance = math.sqrt(dx * dx + dy * dy)

        # Very large inputs can still overflow to infinity
        if not math.isfinite(distance):
            return self.error_response(response, 'distance is too large to calculate')

        response.basarili = True
        response.uzaklik_m = distance
        response.hedefe_yakin = distance <= request.yakinlik_esigi_m
        if response.hedefe_yakin:
            response.aciklama = (f'Target is within the threshold '
                                 f'({distance:.2f} m <= {request.yakinlik_esigi_m:.2f} m)')
        else:
            response.aciklama = (f'Target is outside the threshold '
                                 f'({distance:.2f} m > {request.yakinlik_esigi_m:.2f} m)')

        # Publish the distance once, only for successful requests
        message = Float64()
        message.data = distance
        self.publisher.publish(message)

        self.get_logger().info(f'Published {distance} m to /enro/hedef_uzakligi')
        return response

    def error_response(self, response, reason):
        # Failed request: fixed values and an explanation, nothing is published
        response.basarili = False
        response.uzaklik_m = 0.0
        response.hedefe_yakin = False
        response.aciklama = 'Error: ' + reason
        self.get_logger().warning(response.aciklama)
        return response


def main(args=None):
    rclpy.init(args=args)
    node = UzaklikSunucu()
    try:
        # Keep the node running so it can answer requests
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
