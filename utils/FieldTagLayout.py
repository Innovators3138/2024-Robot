import os

from wpimath.geometry import Pose3d
from robotpy_apriltag import AprilTagFieldLayout


class FieldTagLayout(object):
    field_tags: AprilTagFieldLayout

    def __init__(self):
        exp_path = os.path.abspath((os.path.join(os.path.dirname(__file__),
                                                 "..",
                                                 "deploy",
                                                 "apriltagLayouts",
                                                 "2024-crescendo.json"
                                                 )))
        try:
            self.field_tags = AprilTagFieldLayout(exp_path)
        except Exception:
            self.field_tags = None

    def lookup(self, tag_id: int) -> Pose3d:
        if self.field_tags is not None:
            return self.field_tags.getTagPose(tag_id)
        else:
            return None