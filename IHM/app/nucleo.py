import serial


class Nucleo:
    """Classe qui représente la carte Nucléo qui envoie des données"""

    def __init__(self):
        """ Constructeur de la classe"""
        self._ser = serial.Serial('/dev/ttyACM0', baudrate=115200, bytesize=serial.EIGHTBITS,
                                  parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1)

    def get_value(self):
        self._ser.read()

    def send_value(self, value):
        v = bytes(str(value))
        self._ser.write(v)

    def close(self):
        self._ser.close()
