# GUI-Robot-5Dof-on-web
This is an attempt to merge a flask app with robotic kinematics to ensure a better, flexible and portable controls and visualizations

To use it you might need to install flask, socketio, numpy and run it into a Raspberry pi board, also if you dont have one you only need to bypass the module send and will run on any kind of pc that runs python.
The robot used is a 5 Dof one, something like this https://articulo.mercadolibre.com.mx/MLM-1340567984-kit-brazo-robotico-para-arduino-incluye-solo-3-servos-sg90-_JM
The arduino connected to the robot servos change their positions with an array that recive from the Raspberry pi via I2C
i'll add the code for the arduino when i find it sorry, but its usable by now in emulation mode.

as you might notice it could be difficult to ensure accuracy on this kind of robots and relocate its TCP in its Inverse kinematics mode, feel free to comment any issue or coment that you might think it could improve the robot, I'll apreciate it as much.

For the invers kinematics mode i recomend you to relocate it from its home position to the nex one:
X = 9
y = 0
z = 13
A = 0
B = 180
C = 0
from this you can relocate it in x,y plane more freely, there is some bugs that I'll fix whenever find the time jejeje, but feel free to modified it.

Furthermore this is only a version, over the next i'll will add the function to use remote GPIO and command promt to program it like in Rapid language.

Thanks and enjoy it
