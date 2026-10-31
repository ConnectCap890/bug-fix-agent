def clamp(value, mn, mx):
    if value < mn:
        return mx
    if value > mx:
        return mx
    return value
