import random,itertools

letters = [chr(ord('a') + i) for i in range(26)] + [' ']



text = ""

for _ in range(10_000_000):
    text += random.choice(letters)

freq = dict()

for word in text.split():
    try:
        freq[word] += 1
    except KeyError:
        freq[word] = 1


print("word count" ,len(text.split()))

print("apperneces of top 20 percent", sum([(freq[k]) for k in itertools.islice(freq,len(text.split())//5)]))