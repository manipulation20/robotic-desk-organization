#!/usr/bin/python

# import numpy
import rospy, sys
# import smach
# import smach_ros
# from smach import CBState, State
# from smach import State

# from turtlesim.msg import Pose
# from geometry_msgs import Pose
from geometry_msgs.msg import Pose, Point
from std_msgs.msg import String
import moveit_commander
from moveit_commander import MoveGroupCommander

from moveit_msgs.msg import RobotTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint

from copy import deepcopy
import tf
import tf2_ros
import tf2_geometry_msgs  # **Do not use geometry_msgs. Use this instead for PoseStamped
# sys.path.append('/usr/lib/python3/dist-packages') # pykdl

import math
from math import cos, sin
from tf.transformations import quaternion_from_euler

from threading import Thread

import cv2
import numpy as np
from scipy.spatial import ConvexHull
from matplotlib.path import Path

# RulerPrimitive ###############################################################################################################
# obtain ruler min rectangle, the angle is revified

def calculate_min_area_rect(corners): # 3D corners !!!
    """
    根据给定的角点计算最小外接矩形
    
    参数:
        corners: 包含3D点的列表，每个点具有x, y, z属性 !!!
        
    返回:
        center: 矩形中心点 (x, y, z) 的元组
        width: 矩形宽度 (单位: 米)
        height: 矩形高度 (单位: 米)
        angle: 旋转角度 (单位: 度)
    """
    if len(corners) < 3: #4
        raise ValueError("需要至少4个角点来计算最小外接矩形") # for ruler, if it is triangle, what will happen
    
    # 将3D点转换为2D坐标 (忽略Z轴)
    points_2d = np.array([(pt.x, pt.y) for pt in corners], dtype=np.float32)
    
    # 计算最小外接矩形
    rect = cv2.minAreaRect(points_2d)
    (center_x, center_y), (width, height), angle = rect
    
    # 计算Z坐标的平均值
    z_avg = sum(pt.z for pt in corners) / len(corners)
    
    # 调整OpenCV的角度表示 (OpenCV4返回 [-90, 0] 范围的角度, OpenCV3[0, 90))
    # if width > height:
    #     # width, height = height, width
    #     angle += 90
    
    # 确保角度在 [0, 180) 范围内
    # angle = angle % 180
    
    return (center_x, center_y, z_avg), width, height, angle

#*********************************************************************************
def is_ruler_on_book(book_corners, ruler_position):
    """
    判断尺子是否在书本上
    
    参数:如下
        book_corners: 书本角点列表，每个点是包含x,y,z属性的对象
        ruler_position: 尺子中心点，包含x,y,z属性的对象
        
    返回: 
        True(在书上) 或 False(不在书上)
    """
    if not book_corners or len(book_corners) < 3 or not ruler_position:
        print("书本或尺子信息缺失，无法判断位置关系")
        return False
    
    # 输出书本角点信息
    print("\n书本角点信息:")
    for i, corner in enumerate(book_corners):
        print(f"角点 {i+1}: ({corner.x:.3f}, {corner.y:.3f})")
    
    # 输出尺子中心点信息
    print(f"\n尺子中心点位置: ({ruler_position.x:.3f}, {ruler_position.y:.3f})")
    
    # 将书本角点转换为二维坐标数组，忽略z坐标
    book_points = np.array([(p.x, p.y) for p in book_corners])
    
    # 创建书本的多边形路径
    poly_path = Path(book_points)
    
    # 尺子中心点的二维坐标
    ruler_point = (ruler_position.x, ruler_position.y)
    
    # 检查点是否在多边形内
    # 使用 radius=-1e-10 处理边界情况（负值表示在边界上也算内部）
    result = poly_path.contains_point(ruler_point, radius=-1e-10)
    
    # 输出最终判断结果
    print(f"\n尺子是否在书本上: {'是' if result else '否'}")
    return bool(result)

#*********************************************************************************
# def order_book_corners(corners):
#     """
#     将书本角点排序为：左上、右上、右下、左下（顺时针顺序）
#     保留原始点对象
    
#     参数:
#         corners: 包含4个点对象的列表
        
#     返回:
#         排序后的点对象列表
#     """
#     if len(corners) != 4:
#         raise ValueError("需要恰好4个角点")
    
#     # 提取坐标
#     points = np.array([(pt.x, pt.y) for pt in corners])
    
#     # 计算中心点
#     centroid = np.mean(points, axis=0)
    
#     # 计算角度并排序
#     angles = np.arctan2(points[:,1] - centroid[1], points[:,0] - centroid[0])
#     sorted_indices = np.argsort(-angles)
    
#     # 检查左上角是否正确
#     sorted_points = points[sorted_indices]
#     if np.argmin(np.sum(sorted_points, axis=1)) == 0:
#         return [corners[i] for i in sorted_indices]
    
#     # 如果角度排序不正确，使用和值方法
#     sums = np.sum(points, axis=1)
#     top_left_idx = np.argmin(sums)
#     bottom_right_idx = np.argmax(sums)
    
#     remaining_idxs = [i for i in range(4) if i != top_left_idx and i != bottom_right_idx]
#     diff_x = points[remaining_idxs[0]][0] - points[remaining_idxs[1]][0]
    
#     # 创建排序索引
#     if diff_x > 0:
#         ordered_indices = [top_left_idx, remaining_idxs[0], bottom_right_idx, remaining_idxs[1]]
#     else:
#         ordered_indices = [top_left_idx, remaining_idxs[1], bottom_right_idx, remaining_idxs[0]]
    
#     return [corners[i] for i in ordered_indices]

#*********************************************************************************
# def determine_push_direction(book_corners, ruler_angle):
#     """
#     确定push方向
#     参数:
#         book_corners: 书本角点列表 (原始顺序)
#         ruler_angle: 尺子角度 (度)
#     返回: 'top' (推向书本上边) 或 'left' (推向书本左边) ####################### Maybe the angle of the edge is also necessary.
#     """
#     if not book_corners or ruler_angle is None:
#         rospy.logwarn("书本或尺子信息缺失，无法确定push方向")
#         return 'top'  # 默认推向顶部
    
#     # 确保有4个角点
#     if len(book_corners) < 4:
#         rospy.logwarn("书本角点不足4个")
#         return 'top'
    
#     try:
#         # 在函数内部排序书本角点
#         ordered_corners = order_book_corners(book_corners)
        
#         # 提取角点坐标
#         top_left = np.array([ordered_corners[0].x, ordered_corners[0].y])
#         top_right = np.array([ordered_corners[1].x, ordered_corners[1].y])
#         bottom_left = np.array([ordered_corners[3].x, ordered_corners[3].y])
        
#         # 书本上边向量 (从左到右)
#         top_vector = top_right - top_left
#         # 书本左边向量 (从上到下)
#         left_vector = bottom_left - top_left
        
#         # 计算书本角度 (上边与水平轴的夹角)
#         book_angle = math.degrees(math.atan2(top_vector[1], top_vector[0]))
        
#         # 计算尺子角度与书本上边角度的差值
#         angle_diff_top = abs(ruler_angle - book_angle) % 180
#         angle_diff_top = min(angle_diff_top, 180 - angle_diff_top)
        
#         # 计算尺子角度与书本左边角度的差值 (左边是上边+90度)
#         angle_diff_left = abs(ruler_angle - (book_angle + 90)) % 180
#         angle_diff_left = min(angle_diff_left, 180 - angle_diff_left)
        
#         # 选择角度差值较大的方向进行push
#         if angle_diff_top > angle_diff_left:
#             rospy.loginfo(f"选择push方向: 书本上边 (角度差: 尺子{ruler_angle:.1f}° vs 书本{book_angle:.1f}°)")
#             return 'top' #'top'
#         else:
#             rospy.loginfo(f"选择push方向: 书本左边 (角度差: 尺子{ruler_angle:.1f}° vs 书本{book_angle+90:.1f}°)")
#             return 'left'
    
#     except Exception as e:
#         rospy.logerr(f"确定push方向时出错: {str(e)}")
#         return 'top'

#*********************************************************************************
def determine_push_direction(angle1, angle2):
    """
    判断两条直线的夹角是否小于45度，并返回推杆方向
    
    参数:
        angle1 (float): 第一条直线的角度（范围：-90到90度）
        angle2 (float): 第二条直线的角度（范围：-90到90度）
    
    返回:
        str: 推杆方向 - "longEdge"（夹角<45°）或"shortEdge"（夹角≥45°）
    """
    # 计算角度差的绝对值
    diff = abs(angle1 - angle2)
    
    # 处理周期性（当角度差超过180°时）
    if diff > 180:
        diff = 360 - diff
    
    # 判断夹角是否小于45度
    if diff < 45 or diff > 135:  # 注意：diff>135°对应实际小角度
        return "longEdge"
    else:
        return "shortEdge"
    
import math

#*********************************************************************************
def rotationOpen_direction(angle_deg, A, B):
    """
    判断给定角度表示的向量与向量AB的夹角是否为锐角
    
    参数:
    angle_deg -- 给定的角度（度数）
    A -- 点A的坐标 (Ax, Ay)
    B -- 点B的坐标 (Bx, By)
    
    返回:
    True -- 夹角为锐角（小于90度）
    False -- 夹角为钝角或直角（90度及以上）
    """
    # 将角度转换为弧度

    angle = angle_deg + 180 # min_rect_angle -- angle of camera coordinate -- Y axis 

    angle_rad = math.radians(angle)
    
    # 计算参考向量（单位向量）
    ref_vector = (math.cos(angle_rad), math.sin(angle_rad))
    
    # 计算向量AB
    vector_ab = (B[0] - A[0], B[1] - A[1])
    
    # 计算点积
    dot_product = ref_vector[0] * vector_ab[0] + ref_vector[1] * vector_ab[1]
    
    # 根据点积判断夹角
    return dot_product > 0

#*********************************************************************************
def calculate_min_rotation(pen_angle, long_edge):
    """
    计算笔需要旋转的最小角度，使其对齐书本的长边或短边
    
    参数:
        pen_angle (float): 笔的当前角度（-90°到90°）
        book_long_edge (float): 书本长边的角度（-90°到90°）
    
    返回:
        float: 最小旋转角度（-45°到45°）
    """
    # 计算并规范化短边角度
    short_edge = long_edge + 90
    short_edge = (short_edge + 180) % 360 - 180  # 规范到[-180, 180]
    if short_edge > 90:
        short_edge -= 180
    elif short_edge < -90:
        short_edge += 180
    
    # 计算所有可能的目标角度
    targets = [long_edge, short_edge]
    min_rotation = 360  # 初始化为较大的值
    
    for target in targets:
        # 计算原始角度差
        raw_diff = target - pen_angle
        
        # 计算两种可能的旋转路径
        rotation1 = (raw_diff + 180) % 360 - 180  # 直接旋转
        rotation2 = rotation1 - 180 if rotation1 > 0 else rotation1 + 180  # 反向旋转
        
        # 选择绝对值较小的旋转路径
        if abs(rotation1) <= abs(rotation2):
            rotation = rotation1
        else:
            rotation = rotation2
        
        # 确保旋转角度在[-45°, 45°]范围内
        if rotation > 45:
            rotation -= 180
        elif rotation < -45:
            rotation += 180
        
        # 更新最小旋转角度
        if abs(rotation) < abs(min_rotation):
            min_rotation = rotation

    print("最小旋转角度:", min_rotation)
    
    return min_rotation

#*********************************************************************************
def calculate_foot_of_perpendicular(book_corners, push_direction, ruler_position):
    """
    计算尺子中心到书边的垂足位置（只使用x,y坐标）
    :param book_corners: 书的四个角点 [(x1, y1, z1), (x2, y2, z2), ...]
    :param push_direction: 推边方向，'longEdge' 或 'shortEdge'
    :param ruler_position: 尺子中心坐标 (x, y, z)
    :return: 距离更近的垂足位置 (x, y) - 只包含二维坐标
    """
    # 提取x,y坐标（忽略z坐标）
    book_corners_2d = [(p.x, p.y) for p in book_corners]
    ruler_position_2d = (ruler_position.x, ruler_position.y)
    
    # 计算四个角点的质心
    cx = sum(p[0] for p in book_corners_2d) / 4.0
    cy = sum(p[1] for p in book_corners_2d) / 4.0
    center = (cx, cy)
    
    # 根据相对于质心的极角排序角点（顺时针或逆时针）
    def angle_from_center(point):
        return math.atan2(point[1] - center[1], point[0] - center[0])
    
    sorted_corners = sorted(book_corners_2d, key=angle_from_center)
    
    # 构建矩形的四条边（点按顺序连接）
    edges = []
    n = len(sorted_corners)
    for i in range(n):
        p1 = sorted_corners[i]
        p2 = sorted_corners[(i + 1) % n]
        # 计算边长度
        edge_length = math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
        edges.append((p1, p2, edge_length))
    
    # 按边长度降序排序
    sorted_edges = sorted(edges, key=lambda edge: edge[2], reverse=True)
    
    # 根据推边方向选择目标边
    if push_direction == "longEdge":
        # 选择最长的两条边（长边）
        target_edges = [sorted_edges[0][:2], sorted_edges[1][:2]]
    elif push_direction == "shortEdge":
        # 选择最短的两条边（短边）
        target_edges = [sorted_edges[-1][:2], sorted_edges[-2][:2]]
    else:
        raise ValueError("Invalid push_direction. Must be 'longEdge' or 'shortEdge'")
    
    # 计算尺子中心到每条目标边的垂足位置
    P = ruler_position_2d
    foot_points = []  # 存储垂足位置
    
    for edge in target_edges:
        A, B = edge
        # 向量 AB 和 AP
        AB = (B[0] - A[0], B[1] - A[1])
        AP = (P[0] - A[0], P[1] - A[1])
        
        # 计算点积
        dot_AB_AP = AB[0] * AP[0] + AB[1] * AP[1]
        dot_AB_AB = AB[0] * AB[0] + AB[1] * AB[1]
        
        # 处理边长为零的情况（理论上不会发生）
        if dot_AB_AB == 0:
            t = 0.0
        else:
            t = dot_AB_AP / dot_AB_AB
        
        # 根据 t 值确定垂足位置
        if t < 0:
            F = A  # 垂足为起点
        elif t > 1:
            F = B  # 垂足为终点
        else:
            # 垂足在线段上
            F = (A[0] + t * AB[0], A[1] + t * AB[1])
        foot_points.append(F)
    
    # 计算尺子中心到两个垂足的距离
    dist1_sq = (foot_points[0][0] - P[0])**2 + (foot_points[0][1] - P[1])**2
    dist2_sq = (foot_points[1][0] - P[0])**2 + (foot_points[1][1] - P[1])**2
    
    # 返回距离更近的垂足（使用平方距离比较避免开方运算）
    if dist1_sq <= dist2_sq:
        return foot_points[0]
    else:
        return foot_points[1]


# RulerPrimitiveDesktopEdge ######################################################################################################

def _sorted_rect_edges_2d(corners):
    """
    将四边形角点按极角排序并构建四条边。
    返回: [(p1, p2, length), ...] ，p 为 (x, y)
    """
    corners_2d = [(p.x, p.y) for p in corners]
    cx = sum(p[0] for p in corners_2d) / float(len(corners_2d))
    cy = sum(p[1] for p in corners_2d) / float(len(corners_2d))

    def angle_from_center(point):
        return math.atan2(point[1] - cy, point[0] - cx)

    sorted_corners = sorted(corners_2d, key=angle_from_center)
    edges = []
    n = len(sorted_corners)
    for i in range(n):
        p1 = sorted_corners[i]
        p2 = sorted_corners[(i + 1) % n]
        edge_length = math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
        edges.append((p1, p2, edge_length))
    return edges


def get_upper_long_edge(desktop_corners):
    """
    获取桌面两条长边中、中点 y 更小的那条（相机视野上方长边）。

    参数:
        desktop_corners: 桌面角点列表（含 x,y 属性）
    返回:
        (p1, p2): 上方长边两端点的 (x, y) 元组；失败返回 None
    """
    if not desktop_corners or len(desktop_corners) < 4:
        rospy.logerr("desktop角点不足，无法获取上方长边")
        return None

    edges = _sorted_rect_edges_2d(desktop_corners)
    sorted_edges = sorted(edges, key=lambda e: e[2], reverse=True)
    long_edges = [sorted_edges[0][:2], sorted_edges[1][:2]]

    def midpoint(edge):
        a, b = edge
        return ((a[0] + b[0]) * 0.5, (a[1] + b[1]) * 0.5)

    edge0, edge1 = long_edges
    mid0, mid1 = midpoint(edge0), midpoint(edge1)
    upper_edge = edge0 if mid0[1] <= mid1[1] else edge1
    mid = midpoint(upper_edge)
    rospy.loginfo(
        f"选择桌面上方长边: 中点=({mid[0]:.3f}, {mid[1]:.3f}), "
        f"端点1=({upper_edge[0][0]:.3f}, {upper_edge[0][1]:.3f}), "
        f"端点2=({upper_edge[1][0]:.3f}, {upper_edge[1][1]:.3f})"
    )
    return upper_edge


def foot_on_edge(edge, point_2d):
    """
    计算点到指定边线段的垂足（限制在线段上）。

    参数:
        edge: ((x1, y1), (x2, y2))
        point_2d: (x, y) 或含 x,y 属性的对象
    返回:
        (x, y) 垂足
    """
    A, B = edge
    if hasattr(point_2d, 'x'):
        P = (point_2d.x, point_2d.y)
    else:
        P = (point_2d[0], point_2d[1])

    AB = (B[0] - A[0], B[1] - A[1])
    AP = (P[0] - A[0], P[1] - A[1])
    dot_AB_AB = AB[0] * AB[0] + AB[1] * AB[1]
    if dot_AB_AB == 0:
        return A

    t = (AB[0] * AP[0] + AB[1] * AP[1]) / dot_AB_AB
    t = max(0.0, min(1.0, t))
    return (A[0] + t * AB[0], A[1] + t * AB[1])


def _segment_intersection(p1, p2, p3, p4, eps=1e-9):
    """
    线段 p1-p2 与 p3-p4 求交。
    返回 (t, point)：t 为在 p1->p2 上的参数 [0,1]；无交点返回 None。
    """
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4

    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(den) < eps:
        return None

    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
    u = ((x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2)) / den
    if t < -eps or t > 1.0 + eps or u < -eps or u > 1.0 + eps:
        return None

    t = max(0.0, min(1.0, t))
    return t, (x1 + t * (x2 - x1), y1 + t * (y2 - y1))


def intersect_push_path_with_book(book_corners, start_2d, end_2d, outward_offset=0.005):
    """
    计算推路径线段与书边界的交点（出书点），并沿推方向外扩一小段。

    参数:
        book_corners: 书本角点
        start_2d: 推路径起点 (x, y)
        end_2d: 推路径终点 (x, y)
        outward_offset: 出书后沿推方向外扩距离 (m)
    返回:
        (x, y) 出书安全点；失败返回 None
    """
    if not book_corners or len(book_corners) < 3:
        rospy.logwarn("书本角点不足，无法计算推路径交点")
        return None
    if start_2d is None or end_2d is None:
        return None

    start = (float(start_2d[0]), float(start_2d[1]))
    end = (float(end_2d[0]), float(end_2d[1]))
    direction = (end[0] - start[0], end[1] - start[1])
    path_len = math.sqrt(direction[0] ** 2 + direction[1] ** 2)
    if path_len < 1e-9:
        rospy.logwarn("推路径长度过短，无法计算交点")
        return None

    book_points = [(p.x, p.y) for p in book_corners]
    poly_path = Path(book_points)
    start_inside = bool(poly_path.contains_point(start, radius=-1e-10))

    edges = _sorted_rect_edges_2d(book_corners)
    intersections = []
    for p1, p2, _ in edges:
        hit = _segment_intersection(start, end, p1, p2)
        if hit is not None:
            intersections.append(hit)

    if not intersections:
        rospy.logwarn("推路径与书边界无交点，使用路径中点作为退化出书点")
        exit_point = (0.5 * (start[0] + end[0]), 0.5 * (start[1] + end[1]))
    else:
        intersections.sort(key=lambda item: item[0])
        # 起点在书内：取第一个交点（出书）；起点在书外：取最后一个交点（离开书区）
        t, exit_point = intersections[0] if start_inside else intersections[-1]
        rospy.loginfo(
            f"推路径出书交点: t={t:.3f}, 位置=({exit_point[0]:.3f}, {exit_point[1]:.3f}), "
            f"start_inside={start_inside}"
        )

    unit = (direction[0] / path_len, direction[1] / path_len)
    safe_point = (
        exit_point[0] + outward_offset * unit[0],
        exit_point[1] + outward_offset * unit[1],
    )
    return safe_point


# PaperPrimitive & BookPrimitive #################################################################################################
# RulerPrimitive get_push_pose function

def rotation_matrix(theta):
    """创建2D旋转矩阵"""
    return np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta), np.cos(theta)]
    ])

def calculate_edge_centers(center, width, height, angle):
    """
    计算矩形的两个长边中心点
    
    参数:
        center: 矩形中心点 (2D) [x, y]
        width: 矩形宽度
        height: 矩形高度
        angle: 矩形角度（弧度）
        
    返回:
        edge1_center: 第一个长边中心点 (2D)
        edge2_center: 第二个长边中心点 (2D)
        is_width_longer: 是否宽度大于高度
    """
    # 确定长边方向
    is_width_longer = width > height
    short_edge_length = min(width, height)
    
    # 计算两个长边的中心点
    rot_mat = rotation_matrix(angle)
    if is_width_longer:
        # 长边平行于x轴（在矩形坐标系）
        offset = np.array([0, short_edge_length/2])
        edge1_center = center + rot_mat.dot(offset)
        edge2_center = center - rot_mat.dot(offset)
    else:
        # 长边平行于y轴（在矩形坐标系）
        offset = np.array([short_edge_length/2, 0])
        edge1_center = center + rot_mat.dot(offset)
        edge2_center = center - rot_mat.dot(offset)
    
    return edge1_center, edge2_center, is_width_longer
