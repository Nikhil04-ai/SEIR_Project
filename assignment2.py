import sys
import requests
from bs4 import BeautifulSoup


if len(sys.argv) < 3:
    print("Enter two URl: <url1> <url2>")
    sys.exit()

url1 = sys.argv[1]
url2 = sys.argv[2]

def get_text(url):
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text()

def word_count(text):
    freq = {}
    text = text.lower().split()

    for word in text:
        clean = ""
        for ch in word:
            if ch.isalnum():
                clean += ch
        if clean != "":
            if clean in freq:
                freq[clean] += 1
            else:
                freq[clean] = 1
    return freq


def hash_word(word):
    p = 53
    m = 2**64
    h = 0
    power = 1

    for ch in word:
        h = (h*power + ord(ch)) % m
        power = (power * p) % m
    return h

def simhash(freq):
    bits = [0] * 64

    for word in freq:
        h = hash_word(word)

        for i in range(64):
            if h & (1 << i):
                bits[i] += freq[word]
            else:
                bits[i] -= freq[word]

    result = 0
    for i in range(64):
        if bits[i] > 0:
            result |= (1 << i)

    return result

text1 = get_text(url1)
text2 = get_text(url2)

freq1 = word_count(text1)
freq2 = word_count(text2)

sim1 = simhash(freq1)
sim2 = simhash(freq2)

def common_bits(sim1, sim2):
    xor = sim1 ^ sim2
    different = bin(xor).count("1")
    return 64 - different

commonBits = common_bits(sim1, sim2)

print("Total unique words in freq1:", freq1)
print("Total unique words in freq2:" , freq2)
print("Simhash value sim1:",sim1)
print("Simhash value sim2:",sim2)
print("common bits value" , commonBits)