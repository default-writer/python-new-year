from datetime import datetime
import math

IV = 1
shift = 2022

class prng:
  def __init__(self, seed):
    self._seed = seed % 2147483647
    if self._seed <= 0:
      self._seed += 2147483646

  def next(self, *argv):
    self._seed = (self._seed * 48271) % 2147483647
    length = len(argv)
    if length == 0:
      return self._seed / 2147483647
    elif length == 1:
      a = argv[0]
      return (self._seed / 2147483647) * a
    elif length == 2:
      a = argv[0]
      b = argv[1]
      return (self._seed / 2147483647) * (b - a) + a

min = 0
max = 2147483647
seed = 1238473661

rnd = prng(seed)

def encode(alphabet, char):
  size = len(alphabet)
  j = math.floor(rnd.next(min, max))
  position = alphabet.index(char)
  return (position + 1 + j) % size

def decode(alphabet, char):
  size = len(alphabet)
  j = math.floor(rnd.next(min, max))
  position = alphabet.index(char)
  return size - 1 - ((size - position + j) % size)

def hex2binb(string):
  result = []
  while len(string) >= 8:
    result.append(int(string[:8], 16))
    string = string[8:]
  return result

def shuffle(array, seed):
  rnd = prng(seed)
  for i in reversed(range(len(array))):
    j = math.floor(rnd.next(i))
    array[i], array[j] = array[j], array[i]

def shuffle_binb(alphabet, str):
  if isinstance(str, bytes):
    array = str
  else:
    array = hex2binb(str)
  for i in range(16):
    shuffle(alphabet, array[i])

def cipher(cipher, next):
  def function(shift, alphabet, array, sha_alphabet, sha_plaintext):
    shuffle_binb(alphabet, sha_alphabet)
    shuffle_binb(alphabet, sha_plaintext)
    i = 0
    while i < shift:
      array = list(map(cipher(alphabet, next), array))
      i = i + 1
    return list(array)
  return function

def caesar(alphabet, next):
  def enc(char):
    position = alphabet.index(char)
    newPosition = next(alphabet, char)
    while newPosition == position:
      newPosition = next(alphabet, char)
    return alphabet[newPosition]
  return enc

def caesar_cipher(next, shift, alphabet, plaintext, sha_alphabet, sha_plaintext):
  return cipher(caesar, next)(shift, alphabet, plaintext, sha_alphabet, sha_plaintext)

alphabet = [chr(c) for c in [126, 33, 64, 35, 36, 37, 94, 38, 42, 40, 41, 95, 43, 81, 87, 69, 82, 84, 89, 85, 73, 79, 80, 123, 125, 124, 65, 83, 68, 70, 71, 72, 74, 75, 76, 58, 34, 90, 88, 67, 86, 66, 78, 77, 60, 62, 63, 96, 49, 50, 51, 52, 53, 54, 55, 56, 57, 48, 45, 61, 113, 119, 101, 114, 116, 121, 117, 105, 111, 112, 91, 93, 92, 97, 115, 100, 102, 103, 104, 106, 107, 108, 59, 39, 122, 120, 99, 118, 98, 110, 109, 44, 46, 47, 32, 10, 1049, 1062, 1059, 1050, 1045, 1053, 1043, 1064, 1065, 1047, 1061, 1066, 1060, 1067, 1042, 1040, 1055, 1056, 1054, 1051, 1044, 1046, 1069, 1071, 1063, 1057, 1052, 1048, 1058, 1068, 1041, 1070, 1081, 1094, 1091, 1082, 1077, 1085, 1075, 1096, 1097, 1079, 1093, 1098, 1092, 1099, 1074, 1072, 1087, 1088, 1086, 1083, 1076, 1078, 1101, 1103, 1095, 1089, 1084, 1080, 1090, 1100, 1073, 1102]]

def countdown_timer():
    timer = (datetime.utcnow() - datetime.utcfromtimestamp(0)).total_seconds() - 1640984399
    return 2147483647 * (int(f"{timer}"[10:]) * 48271 % 2147483647 / 2147483647) if timer <= 0 else 1640984399

seed = countdown_timer()
rnd = prng(seed)

encoded = [chr(c) for c in [43, 1103, 1094, 1087, 58, 1060, 63, 33, 80, 1070, 1042, 79, 1094, 45, 1071, 110, 1042, 1094, 71, 41, 97, 10, 108, 1078, 68, 75, 96, 1084, 1089, 1083, 1044, 109, 1060, 1095, 49, 10, 61, 79, 1055, 1045, 1074, 109, 68, 1056, 64, 1069, 40, 88, 114, 1092, 74, 77, 124, 90, 1062, 1087, 1050, 1055, 118, 84, 55, 1094, 68, 84, 1074, 101, 81, 126, 86, 121, 63, 39, 69, 1069, 57, 1052, 108, 57, 1088, 64, 1094, 117, 1046, 1079, 102, 1057, 1058, 102, 1094, 1046, 1100, 76, 1097, 1081, 68, 1060, 90]]
decoded = caesar_cipher(decode, datetime.now().year, [*alphabet], [*encoded], "7557f484cc389712fabf1de974e17636540d44c1b65884df8cf97b9ebdbcddf61846639a19a19113881e3727c8aff3e55e85a0cbe8794edf4a2e1857d07ea6f8", "367de9fdbd996645f973e0d19b2ea8935bd4ff8f3f145ac5f440682903a74040f6a579e67b08b81522ffab930d63e2293d4ee2580a8db4090c53c714c8a7e33c")
print("".join(decoded))
