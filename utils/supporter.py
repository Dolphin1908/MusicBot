def format_duration(seconds):
    """Chuyển đổi thời gian từ giây sang hh:mm:ss"""
    if seconds is None:
        return "N/A"
    h, m, s = seconds // 3600, (seconds % 3600) // 60, seconds % 60
    return f"{h:02}:{m:02}:{s:02}" if h > 0 else f"{m:02}:{s:02}"