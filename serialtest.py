import time
import serial


def main():
     vserial0 = serial.Serial(port='/dev/tnt0', baudrate=9600, bytesize=8, parity=serial.PARITY_EVEN, stopbits=1)
     vserial1 = serial.Serial(port='/dev/tnt1', baudrate=9600, bytesize=8, parity=serial.PARITY_EVEN, stopbits=1)

     n_bytes = 0 

     while n_bytes == 0:
	  data = raw_input()	
          vserial0.write(data)
          n_bytes = vserial1.inWaiting()
          time.sleep(0.05)

     print vserial1.read(n_bytes)

if __name__ == '__main__':
     main()

