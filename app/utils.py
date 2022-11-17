
class RESPDecoder:

  def __init__(self, data) -> None:
      self.data = data
      self.command = ""
      self.args = []

  def decode(self):
      data_type_byte = self.read(1)

      if data_type_byte == b"+":
          return self.decode_simple_string()
      elif data_type_byte == b"$":
          return self.decode_bulk_string()
      elif data_type_byte == b"*":
          return self.decode_array()
      else:
          raise Exception(f"Unknown data type byte: {data_type_byte}")

  
  def decode_simple_string(self):
    return self.read_until_delimiter(b"\r\n")

  def decode_bulk_string(self):
    string_len = int(self.read_until_delimiter(b"\r\n"))
    data = self.read(string_len)
    self.read_until_delimiter(b"\r\n")
    return data

  def decode_array(self):
    data = []
    elements = int(self.read_until_delimiter(b"\r\n"))

    for _ in range(elements):
      data.append(self.decode())
    
    return data

  def read_until_delimiter(self, delimiter):
    if delimiter not in self.data:
      return None

    data_before_delimiter, delimiter, self.data = self.data.partition(delimiter)

    return data_before_delimiter

  def read(self, bytes):
    if not self.data:
      return None

    consumed_data = b""

    if len(self.data) < bytes:
      bytes = len(self.data)

    consumed_data = self.data[0:bytes]

    self.data = self.data[bytes:len(self.data)]

    return consumed_data

    