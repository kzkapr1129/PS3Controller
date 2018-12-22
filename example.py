import PS3
import time

cont = PS3.Controller("/dev/input/js0")
cont.start()

try:
	while True:
		print(cont.analogVal)
		print(cont.isDActive)
		if cont.isDActive[cont.DButton.SELECT]:
			break
except KeyboardInterrupt:
	pass

cont.stop()
