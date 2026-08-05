# robotic-desk-organization

## 1. Project Overview

Robotic desk organization is a representative and challenging task for service robots operating in real-world environments. The main difficulties arise from the heterogeneous physical properties of desktop objects (e.g., small items, planar rigid objects, and deformable objects) and the variety of task objectives (e.g., sorting, storing, and stacking).

In this project, we propose a constraint-aware multi-primitive framework for robotic desk organization, which exploits both environmental constraints (e.g., table surfaces and edges) and inter-object constraints (e.g., book edges) to enable robust manipulation of heterogeneous objects.

We organize three primary manipulation primitives into a reusable library:

- **Contact grasping**: suitable for small objects and paper;
- **Push-grasping**: exploits table or book edges to grasp planar rigid objects such as rulers;
- **Pry-grasping**: handles planar deformable objects such as books.

Based on a perception pipeline (YOLO11, SAM2.1, geometric feature extraction, and point-cloud processing), together with the manipulation primitives and auxiliary primitives for placement, reorientation, and separation, we develop a spatial-dependency-aware task planner. The planner coordinates primitive execution according to object properties and support and adjacency relationships. The complete system performs object perception, manipulation, and orderly placement in structured desk-organization scenarios.

The figure below illustrates an example of the initial and goal states of the organization task. For more details, please refer to the paper (link provided at the end).

> ![Fig. 1: Initial and goal states of the desktop organization task](https://github.com/manipulation20/robotic-desk-organization/blob/main/Fig0.jpg)
> *Fig. 1: Initial state (left) and organized state (right) of the desktop organization task.*  
> *(The initial scene includes pens, erasers, lead cases, rulers, set squares, paper, books, etc. After organization, small items and rulers are placed in the pen holder, while paper and books are neatly stacked.)*

---

## 2. Repository Structure

This repository is organized around two ROS workspaces and a dataset release page:

- **`ultralytics_ws/`** contains the perception-related ROS packages, including object detection, segmentation, geometric feature extraction, and scene perception.
- **`ur_ws_organize/`** contains the robot-manipulation-related ROS packages, including robot, gripper, and camera communication, hand--eye calibration, manipulation primitives, and task planning.
- **[Releases](https://github.com/manipulation20/robotic-desk-organization/releases)** provides the desktop-object dataset and its annotations for download.

The following subsections mainly describe the functions of the ROS packages used for perception, robot control, calibration, manipulation, and task planning.

### **UR Robot (UR5e)**

- **Universal_Robots_ROS_Driver**: Meta-package for controlling the UR robot.
- **fmauch_universal_robot**: Meta-package containing the UR robot description.

Tutorial: https://github.com/UniversalRobots/Universal_Robots_ROS_Driver

### **Gripper (Rochu)**

- **serial_msgs**: Communication package for controlling the gripper.

### **Camera (Intel RealSense D415)**

- **realsense-ros**: ROS package for Intel RealSense cameras.
- **ddynamic_reconfigure**: Allows dynamic parameter tuning for camera nodes.

Tutorial: http://neutron.manoonpong.com/perception-vision-realsense-set-up-tutorial/

### **Eye-to-Hand Calibration**

- **easy_handeye**: Automated, hardware-independent hand–eye calibration package.
- **aruco_ros**: ROS wrapper for ArUco marker detection.
- **vision_visp**: Provides visual servoing algorithms as ROS components.

### **Perception**

- **object_keypoint_msgs**: Message definitions for visual information of different object types.
- **ultralytics_ros**: Includes object pose estimation, keypoint detection, and environment constraint perception (e.g., table edges).

### **Task Planning**

- **ur_smach**: A multi-primitive-based task planner for desktop organization.

---

## 3. Usage

This section describes the complete workflow for running the robotic desk-organization system, including perception, task planning, and manipulation execution. The required modules should be launched in the following order.

First, start the camera and run the perception modules:

```bash
$ cd ultralytics_ws/
$ source devel/setup.bash

# Launch the camera
$ roslaunch realsense2_camera rs_camera.launch align_depth:=true enable_pointcloud:=true

# Object pose and keypoint detection
$ rosrun ultralytics_ros yolo_ros_node1.py

# Environment constraint detection (e.g., table edges)
$ export PYTHONPATH="/home/xxx/anaconda3/envs/yolo_ros/lib/python3.8/site-packages:$PYTHONPATH"
$ rosrun ultralytics_ros desktop_detection_node.py

```

Then, start the gripper and robot communication interfaces, publish the hand–eye calibration results, and run the task planner:

```bash
$ cd ur_ws_organize/
$ source devel/setup.bash

# Gripper communication
$ roslaunch serial_msgs gripper_control.launch 

# Robot driver
$ roslaunch ur_robot_driver ur5e_work_all.launch

# Publish hand–eye calibration results
$ roslaunch easy_handeye publish.launch

# Task planner
$ rosrun ur_smach TaskPlanner.py

# Start the task
$ rostopic pub /tidy_task_command std_msgs/String "start"

```

---

## 4. Experimental Scenarios

To systematically evaluate the proposed framework, we designed **36 distinct experimental scenarios** under structured but representative desk-organization settings. These scenarios vary in the number of object categories, object combinations, layouts, and spatial relationships, including support, adjacency, overlap, and occlusion.

### Naming Convention

Each scenario is labeled as **`Cxyz`**, where:

- **`x`** = number of object categories involved (range: 2–5)  
- **`y`** = combination index within that category count  
- **`z`** = layout instance index (1–3)  

**Example:** `C311` denotes the first layout instance of the first combination involving three object categories.

### Object Categories

The following object groups are considered, consistent with Section III of the paper:

| Category | Included Objects |
|----------|------------------|
| Small objects | Pens, erasers, lead cases |
| Planar rigid objects | Straight rulers, 30° triangular rulers, 45° triangular rulers |
| Planar deformable objects | Paper sheets (60–80 GSM), paperback books with relatively flexible covers |

Each scenario contains **2 to 5 object categories** with varied object poses and layouts. The scenes include representative spatial relationships, such as small objects or rulers supported by other objects, adjacent objects that may interfere with manipulation, and partially or severely occluded objects. In particular, `C323` contains a pen partially covered by paper, whereas `C411` contains a ruler severely occluded by paper.

### Full Set of 36 Scenarios

The figure below presents all 36 scenarios used in the **Integrated Framework Evaluation**. Each subfigure shows the initial configuration of one desk-organization task, arranged from `C2xx` to `C5xx` according to the number of object categories. For each scenario, the robot is required to place small objects and rulers into a pen holder and stack paper and books according to the goal-state definition in Fig. 1.

![36 experimental scenarios for desktop organization](https://github.com/manipulation20/robotic-desk-organization/blob/main/Fig1.png)

*Fig. 2: The 36 experimental scenarios used to evaluate the integrated framework. Each scene is labeled as `Cxyz`, where `x` denotes the number of object categories, `y` the object-combination index, and `z` the layout instance. The scenarios include varied object combinations and representative support, adjacency, overlap, and occlusion relationships for evaluating the constraint-aware framework and spatial-dependency-aware task planner.*

---

## 5. Resources

- Video: See the supplementary multimedia material.
- Paper: The URL will be released later.

---

## 6. Contact

If you have any questions about this project, feel free to contact:

📧 xxx (Double-anonymous peer review)
