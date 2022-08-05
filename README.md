# Scientific-Display-GUI
The repository contains a front-end interface for displaying sensor data from a Science Module including Ozone,tVOC,CO2,Moisture, Spectrometer Graphs and a Microscope Image

### Running the software : 

Open a new terminal and type the following commands : 

```
source /opt/ros/noetic/setup.bash
roscd catkin_ws
cd src
git clone https://github.com/LavaHawk0123/Scientific-Display-GUI.git
cd ..
catkin_make
```

Now open 2 terminals side-by-side and
in the first run : 

```
roslaunch gui_sm testbench.launch
```

in another terminal run : 

```
cd src/gui_sm/gui/GUI-2022/
python3 Science_gui.py
```
### Working :

https://user-images.githubusercontent.com/75236655/162396059-64950c41-468c-415d-a8a5-de4d43680b52.mp4
