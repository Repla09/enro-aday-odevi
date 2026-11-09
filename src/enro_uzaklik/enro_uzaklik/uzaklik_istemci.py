import sys

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from enro_interfaces.srv import UzaklikKontrol

USAGE = ('Usage: ros2 run enro_uzaklik uzaklik_istemci '
         'robot_x robot_y hedef_x hedef_y yakinlik_esigi_m')


class UzaklikIstemci(Node):

    def __init__(self):
        super().__init__('uzaklik_istemci')
        self.client = self.create_client(UzaklikKontrol, '/enro/uzaklik_kontrol')

    def send_request(self, numbers):
        request = UzaklikKontrol.Request()
        request.robot_x = numbers[0]
        request.robot_y = numbers[1]
        request.hedef_x = numbers[2]
        request.hedef_y = numbers[3]
        request.yakinlik_esigi_m = numbers[4]
        # call_async returns a future that gets the response later
        return self.client.call_async(request)


def main(args=None):
    # The five numbers come from the command line
    if len(sys.argv) != 6:
        print(USAGE)
        return
    numbers = []
    try:
        for arg in sys.argv[1:]:
            numbers.append(float(arg))
    except ValueError:
        print('All five values must be numbers.')
        print(USAGE)
        return

    rclpy.init(args=args)
    node = UzaklikIstemci()
    try:
        # Wait until the server node is running
        while not node.client.wait_for_service(timeout_sec=1.0):
            node.get_logger().info('Waiting for /enro/uzaklik_kontrol ...')

        future = node.send_request(numbers)
        # Run the node until the server has answered
        rclpy.spin_until_future_complete(node, future)
        response = future.result()
        node.get_logger().info(
            f'Response: basarili={response.basarili}, '
            f'uzaklik_m={response.uzaklik_m}, '
            f'hedefe_yakin={response.hedefe_yakin}, '
            f'aciklama="{response.aciklama}"')
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
