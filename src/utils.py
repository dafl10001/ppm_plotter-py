import math

def seconds_to_time(milliseconds: int, show_ms=False):
    if milliseconds <= 0:
        return "0ms"

    seconds = milliseconds // 1000

    ms = math.floor(milliseconds % 1000)
    s = math.floor(seconds % 60)
    m = int((seconds // 60) % 60)
    h = int((seconds // 3600) % 24)
    d = int((seconds // 86400) % 30)
    mon = int((seconds // 2592000) % 12)
    yr = int((seconds // 31104000))

    parts = []
    if yr:  parts.append(f"{yr}yr")
    if mon: parts.append(f"{mon}mo")
    if d:   parts.append(f"{d}d")
    if h:   parts.append(f"{h}h")
    if m:   parts.append(f"{m}m")
    if s:   parts.append(f"{s}s")
    if show_ms and ms: parts.append(f"{ms}ms")

    return " ".join(parts) if parts else ("0ms" if show_ms else "0s")


def estimate_time(pixelcount: int):
    x = pixelcount
    return (2.62169E-11) * x ** 2 + 0.00523792 * x + 4683.91111