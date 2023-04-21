"""Tools to deal with descriptive json files."""

def win_time(mtime:int)->int:
    """Returns modification time as windows file time.

    Args:
        mtime (int): file modification time in nanoseconds (as in `Path().stat().st_mtime_ns`).

    Returns:
        int: windows file time.
    """
    return mtime // 100 + 116444736000000000