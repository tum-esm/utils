"""Mathematical functions.

Implements: `distance_between_angles`"""


def distance_between_angles(angle_1: float, angle_2: float) -> float:
    """Calculate the directional distance (in degrees) between two angles."""
    if angle_1 > angle_2:
        return min(angle_1 - angle_2, 360 + angle_2 - angle_1)
    else:
        return min(angle_2 - angle_1, 360 + angle_1 - angle_2)
