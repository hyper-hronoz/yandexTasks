import sys
from math import cos, pi, sin
from controller.MainViewController import MainController


if __name__ == '__main__':
    controller = MainController()
    sys.exit(controller.run())
    