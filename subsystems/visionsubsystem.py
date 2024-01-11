from typing import List

import wpilib
from wpimath.geometry import Pose3d, Transform3d, Pose2d
from wpimath.units import feetToMeters
from photonlibpy.photonCamera import PhotonCamera, setVersionCheckEnabled

from utils import FieldTagLayout
import constants


class VisionSubsystem(object):
    camera: PhotonCamera
    robot_to_cam: Transform3d

    def __init__(self, robot_to_cam: Transform3d):
        self.pose_estimates = List[Pose2d]
        setVersionCheckEnabled(False)

        self.camera = PhotonCamera(constants.CAMERA_NAME)

    def update(self, prev_est_pose: Pose2d):
        result = self.camera.getLatestResult()
        observation_time = result.getTimestamp()

        self.pose_estimates = []

        for target in result.getTargets():

            target_id = target.getFiducialId()
            if target_id >= 0:
                tag_field_pose = FieldTagLayout().lookup(target_id)
                pose_candidates = [self._to_field_pose(tag_field_pose, target.getBestCameraToTarget()),
                                   self._to_field_pose(tag_field_pose, target.getAlternateCameraToTarget())]

                filtered_candidates = []
                for candidate in pose_candidates:
                    on_field = self._pose_is_on_field(candidate)
                    if on_field:
                        filtered_candidates.append(candidate)

                best_candidate = None
                best_candidate_dist = 99999999.0
                for candidate in filtered_candidates:
                    delta = (candidate - prev_est_pose).translation().norm()
                    if delta < best_candidate_dist:
                        best_candidate = candidate
                        best_candidate_dist = delta

    def _to_field_pose(self, target_pose: Pose3d, cam_to_target: Transform3d) -> Pose2d:
        cam_pose = target_pose.transformBy(cam_to_target.inverse())
        return cam_pose.transformBy(self.robot_to_cam.inverse()).toPose2d()

    def _pose_is_on_field(self, pose: Pose2d) -> bool:
        trans = pose.translation()
        x = trans.x
        y = trans.y
        inY = 0.0 <= y <= feetToMeters(27.0)
        inX = 0.0 <= x <= feetToMeters(54.0)
        return inX and inY
