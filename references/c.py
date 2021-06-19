import sys
import select


class TimeoutOccurred(BaseException):
    pass

def unix_input_with_timeout(prompt='', timeout=3):
    sys.stdout.write(prompt)
    sys.stdout.flush()
    (ready, _, _) = select.select([sys.stdin], [], [], timeout)
    if ready:
        return sys.stdin.readline().rstrip('\n')
    else:
        raise TimeoutOccurred

print(unix_input_with_timeout('test'))