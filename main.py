import random

a = 0
while a < 1 or a > 100: 
    s = input("загадай число от 1 до 100: ")
    a = int(s)

b = 0
min = 1
max = 100

a = list(range(min,max+1))

rules = [0, 1, 2, 3, 4]

while True:
    if len(a) == 1:
        break
    b = random.choice(a)
    rule = random.choice(rules)
    if rule == 0:
        a = [b] if str(input(f"это число {b}? ")) == 'y' else a[0: a.index(b)] + a[a.index(b) + 1:]
    if rule == 1:
        a = a[a.index(b) + 1:] if str(input(f"это число больше {b}? ")) == 'y' else a[0: a.index(b) + 1]
    if rule == 2:
        a = a[0: a.index(b)] if str(input(f"это число меньше {b}? ")) == 'y' else a[a.index(b):]
    if rule == 3:
        a = [n for n in a if n % 2 == 0] if str(input(f"это число четное? ")) == 'y' else [n for n in a if n % 2 == 1]
        rules.remove(3)

print(f"это число {a[0]}")

import hashlib
import math
from operator import itemgetter

def frequency(text):
  count = {}
  for key in text:
    count[key] = count[key] + 1 if count.get(key) else 1
  return count

def convert(obj):
  return sorted(list(map(lambda key: [key, obj[key]], obj.keys())), key=itemgetter(0))

def multisort(xs, specs):
  for key, reverse in reversed(specs):
    xs.sort(key=itemgetter(key), reverse=reverse)
  return xs

def sort(array):
  return multisort(list(array), ((1,True), (0, False)))

def chars(text):
  freq = frequency(text)
  items = convert(freq)
  sort_items = sort(items)
  return {
    "char": list(map(itemgetter(0), sort_items)),
    "freq": list(map(itemgetter(1), sort_items))
  }

IV = 1
shift = 2021

alphabet = [chr(c) for c in [126, 33, 64, 35, 36, 37, 94, 38, 42, 40, 41, 95, 43, 81, 87, 69, 82, 84, 89, 85, 73, 79, 80, 123, 125, 124, 65, 83, 68, 70, 71, 72, 74, 75, 76, 58, 34, 90, 88, 67, 86, 66, 78, 77, 60, 62, 63, 96, 49, 50, 51, 52, 53, 54, 55, 56, 57, 48, 45, 61, 113, 119, 101, 114, 116, 121, 117, 105, 111, 112, 91, 93, 92, 97, 115, 100, 102, 103, 104, 106, 107, 108, 59, 39, 122, 120, 99, 118, 98, 110, 109, 44, 46, 47, 32, 10, 1049, 1062, 1059, 1050, 1045, 1053, 1043, 1064, 1065, 1047, 1061, 1066, 1060, 1067, 1042, 1040, 1055, 1056, 1054, 1051, 1044, 1046, 1069, 1071, 1063, 1057, 1052, 1048, 1058, 1068, 1041, 1070, 1081, 1094, 1091, 1082, 1077, 1085, 1075, 1096, 1097, 1079, 1093, 1098, 1092, 1099, 1074, 1072, 1087, 1088, 1086, 1083, 1076, 1078, 1101, 1103, 1095, 1089, 1084, 1080, 1090, 1100, 1073, 1102]]
sha_alphabet = hashlib.sha3_512("".join(alphabet).encode("utf-8")).hexdigest()

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
# seed = time.time()

rnd = prng(seed)

def random():
  global rnd
  return math.floor(rnd.next(min, max))

def size():
  return len(alphabet)

def previous_position(alphabet, char):
  j = random()
  position = alphabet.index(char)
  return size() - 1 - ((size() - position + j) % size())

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
  shuffle(alphabet, array[0])
  shuffle(alphabet, array[1])
  shuffle(alphabet, array[2])
  shuffle(alphabet, array[3])
  shuffle(alphabet, array[4])
  shuffle(alphabet, array[5])
  shuffle(alphabet, array[6])
  shuffle(alphabet, array[7])
  shuffle(alphabet, array[8])
  shuffle(alphabet, array[9])
  shuffle(alphabet, array[10])
  shuffle(alphabet, array[11])
  shuffle(alphabet, array[12])
  shuffle(alphabet, array[13])
  shuffle(alphabet, array[14])
  shuffle(alphabet, array[15])

def cipher_function(cipher):
  def function(random, shift, alphabet, array, sha_alphabet, sha_plaintext):
    global rnd
    shuffle_binb(alphabet, sha_alphabet)
    shuffle_binb(alphabet, sha_plaintext)
    rnd = prng(random)
    i = 0
    while i < shift:
      array = list(map(cipher(alphabet), array))
      i = i + 1
    return list(array)
  return function

def shift_decrypt(alphabet):
  def enc(char):
    if char == '' or (not char in alphabet): raise Exception("undefined char '" + char + "'")
    position = alphabet.index(char)
    newPosition = previous_position(alphabet, char)
    while newPosition == position:
      newPosition = previous_position(alphabet, char)
    return alphabet[newPosition]
  return enc

def decrypt_cipher(IV, shift, alphabet, plaintext, sha_alphabet, sha_plaintext):
  return cipher_function(shift_decrypt)(IV, shift, alphabet, plaintext, sha_alphabet, sha_plaintext)

sha_plaintext = "70a230ba73a083a6c6b21a777894def363325828ad7b940c6042da047679751bed3c00b57f150a292afccaa2c6bdd189b9b52e641e2c44928da087df5b25975b"
encoded = [chr(c) for c in [1046, 63, 1076, 68, 38, 83, 65, 44, 69, 1084, 1070, 99, 1099, 1095, 1078, 94, 1103, 55, 107, 1072, 1089, 116, 56, 1049, 1065, 57, 48, 120, 45, 1053, 57, 1046, 71, 39, 1042, 80, 1101, 1053, 103, 1070]]
decoded = decrypt_cipher(IV, shift, [*alphabet], [*encoded], sha_alphabet, sha_plaintext)
print("".join(decoded))
