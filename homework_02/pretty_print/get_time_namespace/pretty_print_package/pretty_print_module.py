from datetime import datetime as dt
from get_time_package.get_time_module import get_time


def unix_to_pretty(unixtime: int) -> str:
    formatted_time = dt.fromtimestamp(unixtime).strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time

def main() -> int:
    unixtime = get_time()
    print(unix_to_pretty(unixtime))

    return 0

if __name__ == "__main__":
    main()