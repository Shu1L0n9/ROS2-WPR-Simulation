# WPR 系列机器人 ROS2 仿真实验

## 系统版本

- ROS2 Humble (Ubuntu 22.04)

## 实验说明
### 1. 海龟 8 字实验

```
ros2 run turtlesim turtlesim_node
python ros_2_exp_1.py
```

### 2. WPR 机器人实验
1. 获取源码:
```
cd ~/ros2_ws/src/
git clone https://github.com/6-robot/wpr_simulation2.git
```
2. 安装依赖项:  
ROS2 Humble (Ubuntu 22.04)
```
cd ~/ros2_ws/src/wpr_simulation2/scripts
./install_for_humble.sh
```
3. 编译
```
cd ~/ros2_ws
colcon build --symlink-install
```

简单场景:
```
ros2 launch wpr_simulation2 wpb_simple.launch.py 
```
![wpb_simple pic](./media/wpb_simple.png)

SLAM环境地图创建:
```
ros2 launch wpr_simulation2 slam.launch.py 
ros2 run rqt_robot_steering rqt_robot_steering 
```
![wpb_gmapping pic](./media/wpb_gmapping.png)

Navigation导航:
```
ros2 launch wpr_simulation2 navigation.launch.py 
```
![wpb_navigation pic](./media/wpb_navigation.png)
