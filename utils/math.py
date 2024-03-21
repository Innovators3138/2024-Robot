def rpm_to_units(rpm, cpr) -> float:
    return rpm * cpr / 600.0


def units_to_rpm(units_per_100ms, cpr) -> float:
    return units_per_100ms * 600 / cpr