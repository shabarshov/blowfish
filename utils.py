from typing import Tuple

def string_to_int(value: str) -> int:
  byte_value = value.encode()
  return int.from_bytes(byte_value, byteorder="big")


def int_to_string(value: int) -> str:
  byte_value = value.to_bytes((value.bit_length() + 7) // 8, byteorder="big")
  return byte_value.decode("utf-8")


def get_pair(value: str) -> Tuple[str, int]:
  return string_to_int(value[:4]), string_to_int(value[4:])
