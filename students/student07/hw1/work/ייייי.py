import random
import re
import matplotlib.pyplot as plt

with open("words") as file:
    known_words = {line.strip().lower() for line in file if line.strip()}


def english_score(text):
    count = 0
    for word in text.lower().split():
        if word in known_words:
            count += 1
    return count


def encrypt(text, key):
    result = ""
    for char in text:
        if "A" <= char <= "Z":
            result += chr((ord(char) - ord("A") + key) % 26 + ord("A"))
        else:
            result += char
    return result


def break_caesar(ciphertext):
    best_score = -1
    best_key = None

    for key in range(26):
        current_try = ""
        for char in ciphertext:
            if "A" <= char <= "Z":
                current_try += chr((ord(char) - ord("A") - key) % 26 + ord("A"))
            else:
                current_try += char

        score = english_score(current_try)
        if score > best_score:
            best_score = score
            best_key = key

    return best_key


sentences = [
    "The morning train was late again, so we waited on the cold platform and watched the sun slowly rise over the town.",
    "She opened the old wooden box and found a handful of letters that her grandmother had written many years ago.",
    "Learning a new language takes time and patience, but every small step makes the next one a little bit easier.",
    "After the storm passed, the children ran outside to play in the puddles while their parents cleaned the garden.",
    "My brother likes to cook dinner on weekends, and he always tries a new recipe that nobody in the family has tasted.",
    "There is a small bakery near the station that sells fresh bread every morning, and people line up before it opens.",
    "The teacher asked us to read the first chapter tonight and to write a short summary of what we think happened.",
    "When we reached the top of the hill, we could see the whole city spread out below us like a map of lights.",
    "He forgot his keys at the office, so he had to walk back through the rain to get them before the doors were locked.",
    "Our team worked late on Friday to finish the project, and everyone agreed that the final result was worth the effort.",
    "A good book can take you to places you have never been and show you things that you would never see by yourself.",
    "The old man sat by the window every afternoon and watched the birds that came to eat the seeds he left outside.",
    "I would like to thank everyone who came to the party, because without your help it would not have been such a great night.",
    "They decided to build a small house near the lake, where the water is clear and the mountains are always covered with snow.",
    "It was a quiet evening, and the only sound in the room was the soft ticking of the clock on the wall above the table.",
    "The doctor told him to drink more water and to get some sleep, because his body needed time to recover from the long week.",
    "We spent the whole summer travelling by bus through small villages, meeting friendly people and tasting food from every region.",
    "The computer stopped working in the middle of the lesson, so the students had to finish their exercises with pen and paper.",
    "Every year in the spring, the family gathers at my aunt's house to celebrate the holiday with music, dancing and a big meal.",
    "If you want to get better at playing the guitar, you should practice a little every day instead of a lot once a week.",
    "The river was so high after the rain that the bridge was closed, and the drivers had to find another way into the village.",
    "She smiled when she heard the news, because she had worked hard for many months and had almost given up on the dream.",
    "A group of tourists stood in front of the museum and listened carefully while the guide explained the history of the building.",
    "He packed his bag, locked the door behind him, and set out on the long road that led to the town where he was born.",
    "The market was full of colors and smells, with fresh fruit on every table and sellers calling out the prices to the crowd.",
    "At the end of the long day, they sat together around the fire and talked about everything that had happened since they met.",
    "The new library has a quiet reading room on the second floor, where students can study without being disturbed by the noise.",
    "Some people prefer to wake up early and go for a run, while others like to stay in bed and enjoy the silence of the house.",
    "The captain looked at the sky and decided that it was safer to stay in the harbor until the strong wind had died down.",
    "My grandfather used to tell us stories about his youth, and we would listen for hours without ever getting tired of them.",
]

words = " ".join(re.sub(r"[^A-Za-z ]", "", s).upper() for s in sentences).split()


def texts_of_length(length, count=30):
    windows = []
    for start in range(len(words)):
        for end in range(start + 1, len(words) + 1):
            piece = " ".join(words[start:end])
            if len(piece) >= length:
                if len(piece) == length:
                    windows.append(piece)
                break
    windows = list(dict.fromkeys(windows))       
    return random.sample(windows, count)


random.seed(1)
lengths = [5, 10, 20, 50, 100]
percentages = []

for length in lengths:
    correct = 0
    for text in texts_of_length(length):
        key = random.randint(1, 25)
        if break_caesar(encrypt(text, key)) == key:
            correct += 1
    percentages.append(correct / 30 * 100)
    print(length, "characters:", round(percentages[-1], 1), "% correct")

plt.plot(lengths, percentages, marker="o")
plt.xlabel("Text length (characters)")
plt.ylabel("Correct key (%)")
plt.title("Caesar breaker accuracy by text length")
plt.ylim(0, 105)
plt.grid(True)
plt.savefig("caesar_experiment.png")
plt.show()
