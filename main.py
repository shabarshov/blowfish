from typing import List, Tuple
from sys import argv

from P_BOXES import P_BOXES
from S_BOXES import S_BOXES
from utils import *


def F(x: int) -> int:
  x %= (0x1 << 32)

  a = S_BOXES[0][x >> 24]
  b = S_BOXES[1][x >> 16 & 0xff]
  c = S_BOXES[2][x >> 8 & 0xff]
  d = S_BOXES[3][x & 0xff]

  return (a + b) ^ c + d


def encrypt(left: int, right: int) -> Tuple[int, int]:
  for i in range(16):
    left ^= P_BOXES[i]
    right ^= F(left)
    left, right = right, left

  left, right = right, left
  right ^= P_BOXES[16]
  left ^= P_BOXES[17]

  return [left, right]


def decrypt(left: int, right: int) -> Tuple[int, int]:
  for i in reversed(range(2, 18)):
    left ^= P_BOXES[i]
    right ^= F(left)
    left, right = right, left
  
  left, right = right, left
  left ^= P_BOXES[0]
  right ^= P_BOXES[1]

  return [left, right]


def expand_open_key(value: str, bit_length: int = 576) -> List[int]:
  required_length = int(bit_length / 8)
  expanded_value = value

  expanded_key = []

  while len(expanded_value.encode("utf-8")) < required_length:
    expanded_value += value

  expanded_value = expanded_value[:required_length]

  chunk_size = 4
  for i in range(0, len(expanded_value), chunk_size):
    chunk = expanded_value[i:i + chunk_size]
    expanded_key.append(string_to_int(chunk))

  return expanded_key


def expand_close_key(initial_key: List[int]) -> None:
  for i in range(18):
    P_BOXES[i] ^= initial_key[i]

  left, right = 0, 0
  for i in range(0, 18, 2):
    left, right = encrypt(left, right)
    P_BOXES[i] = left
    P_BOXES[i + 1] = right

  for i in range(4):
    for j in range(0, 256, 2):
      S_BOXES[i][j], S_BOXES[i][j + 1] = encrypt(S_BOXES[i][j], S_BOXES[i][j + 1])


def prepare_message(message: str) -> Tuple[int, List[Tuple[int, int]]]:
  count_of_extra_chars = 8 - len(message) % 8
  message += count_of_extra_chars * "0"

  chunk_size = 8
  message_arr = [message[i:i + chunk_size] for i in range(0, len(message), chunk_size)]
  return count_of_extra_chars, message_arr


def extract_message(decrypted_message: List[Tuple[int, int]], count_of_extra_chars: int) -> str:
  extracted_message = ""

  for i in decrypted_message:
    for j in i:
      extracted_message += int_to_string(j)

  return extracted_message[:-count_of_extra_chars]


def main(silent_mode: bool = False):
  open_key = input("" if silent_mode else "Input key: ")
  expanded_open_key = expand_open_key(open_key)
  expand_close_key(expanded_open_key)

  message = input("" if silent_mode else "Input message: ")
  count_of_extra_chars, prepared_message = prepare_message(message)

  encrypted_message = []

  for i in prepared_message:
    encrypted_message.append(encrypt(*get_pair(i)))

  # print("Encrypted message:", *encrypted_message, sep=" ")

  decrypted_message = []
  for i in encrypted_message:
    left, right = decrypt(i[0], i[1])
    decrypted_message.append([left, right])

  print("Decrypted message:", extract_message(decrypted_message, count_of_extra_chars), sep=" ")


if __name__ == "__main__":
  if len(argv) == 2:
    if argv[1] == "--silent":
      main(silent_mode=True)
    else:
      print("Usage: python main.py [--silent]")

  if len(argv) == 1:
    main()

  if len(argv) > 2:
    print("Usage: python main.py [--silent]")
