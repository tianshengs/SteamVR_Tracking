import asyncio

from pyquaternion import Quaternion
from xamla_motion.data_types import CartesianPath, JointPath, Pose
from xamla_motion.v2.motion_client import EndEffector, MoveGroup
from xamla_motion.utility import register_asyncio_shutdown_handler
from xamla_motion import MoveJointsCollisionFreeOperation, MoveCartesianCollisionFreeOperation
import pickle
import numpy as np

def main():

    # create move group instance
    move_group = MoveGroup()
    # get default endeffector of the movegroup
    end_effector = move_group.get_end_effector()
    
    file_path = open('test.obj', 'rb') 
    data = pickle.load(file_path)
    start = end_effector.get_current_pose()
    path = []
    for point in data:
        coordinate = point[0]
        coordinate.tolist()
        coordinate[0], coordinate[1],coordinate[2] = -coordinate[0], coordinate[2], coordinate[1]
        coordinate = np.array(coordinate) + start.translation
        quat_element = point[1].elements
        quat = Quaternion(quat_element[0], -quat_element[1], quat_element[3], quat_element[2])
        quat = quat * start.quaternion
        pose = Pose(coordinate,quat)
        path.append(pose)
    
    cartesian_path = CartesianPath(path)
    joint_path = end_effector.inverse_kinematics_many(cartesian_path,
                                                      False).path

    loop = asyncio.get_event_loop()
    register_asyncio_shutdown_handler(loop)

    async def example_moves():
        print('test MoveGroup class')
        print('----------------          move joints                 -------------------')
        move_joints = move_group.move_joints(joint_path)
        move_joints = move_joints.with_velocity_scaling(0.2)

        move_joints_plan = move_joints.plan()

        await move_joints_plan.execute_async()

    try:
        loop.run_until_complete(example_moves())
    finally:
        loop.close()


if __name__ == '__main__':
    main()