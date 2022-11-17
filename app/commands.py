import time
from .database import key_to_value, key_to_expiry

def echo(*args):
    return b"$%d\r\n%b\r\n" % (len(args[0]), args[0])

def ping(*args):
    return (b"+PONG\r\n")

def set(key, value, *args):
  key_to_value[key] = value

  if args and args[0] == b"px":
    key_to_expiry[key] = ((time.time() * 1000) + int(args[1]))
    print(key_to_expiry)
  return b"+OK"

def get(key):
  if key not in key_to_value:
    return b"$-1\r\n"

  print(time.time() * 1000)
  if key in key_to_expiry and key_to_expiry[key] <= (time.time() * 1000):
    key_to_expiry.pop(key)
    value = key_to_value.pop(key)
    return b"$%d\r\n%b\r\n" % (len(value), value)
    #return b"$-1\r\n"

  return b"$%d\r\n%b\r\n" % (len(key_to_value[key]), key_to_value[key])

command_dispatch = {
    "echo": echo,
    "ping": ping,
    "set": set,
    "get": get,
}