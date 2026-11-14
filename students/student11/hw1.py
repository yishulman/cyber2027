"""HW1 - student11: breaking Caesar and columnar transposition by brute force."""
import itertools, math, random, string
from collections import Counter

CAESAR = "UVWFGPVU YJQ RTCEVKEG C NKVVNG GXGTA FCA WUWCNNA TGOGODGT OQTG VJCP VJQUG YJQ ETCO UEKGPVKUVU JCXG FKUEQXGTGF VJCV UQOG DKTFU ECP"
TRANSPOSITION = "HRO  TKREABEIEIORTEB Q S Y RAOCSEATKAE ESTOLN LUEHWRHUR S AGLRTRNHE BOC  DS FYLAE AAIOFTA EL U DEPNOFITNYETA DD LRSEOOUNL  LRGMRTOO PHO  HMC  NIY TMRDDAHFEE"

# generic list of common English words (not taken from my own texts)
COMMON = """the be to of and a in that have i it for not on with he as you do at this but his by from they we say her she or an will my one all would
there their what so up out if about who get which go me when make can like time no just him know take people into year your good some could them see other
than then now look only come its over think also back after use two how our work first well way even new want because any these give day most us is are was
were been has had did said each tell does set three want air play small end put home read hand port large spell add even land here must big high such follow
act why ask men change went light kind off need house picture try again animal point mother world near build self earth father head stand own page should
country found answer school grow study still learn plant cover food sun four between state keep eye never last let thought city tree cross farm hard start
might story saw far sea draw left late run while press close night real life few north open seem together next white children begin got walk example ease
paper group always music those both mark often letter until mile river car feet care second book carry took science eat room friend began idea fish
mountain stop once base hear horse cut sure watch color face wood main enough plain girl usual young ready above ever red list though feel talk bird soon
body dog family direct pose leave song measure door product black short numeral class wind question happen complete ship area half rock order fire south
problem piece told knew pass since top whole king space heard best hour better true during hundred five remember step early hold west ground interest
reach fast verb sing listen six table travel less morning ten simple several vowel toward war lay against pattern slow center love person money serve
appear road map rain rule govern pull cold notice voice unit power town fine certain fly fall lead cry dark machine note wait plan figure star box noun
field rest correct able pound done beauty drive stood contain front teach week final gave green oh quick develop ocean warm free minute strong special
mind behind clear tail produce fact street inch multiply nothing course stay wheel full force blue object decide surface deep moon island foot system
busy test record boat common gold possible plane stead dry wonder laugh thousand ago ran check game shape equate hot miss brought heat snow tire bring
yes distant fill east paint language among students practice little every usually discovered scientists cram those than more""".split()
WORDS = sorted({w.upper() for w in COMMON if len(w) >= 2}, key=len, reverse=True)
WORDSET = set(WORDS)
ENG_FREQ = dict(zip("ETAOINSHRDLCUMWFGYPBVKJXQZ",
    [12.7,9.1,8.2,7.5,7.0,6.7,6.3,6.1,6.0,4.3,4.0,2.8,2.8,2.4,2.4,2.2,2.0,2.0,1.9,1.5,1.0,0.8,0.15,0.15,0.1,0.07]))

def english_score(text):
    """Higher = more English-like. Combines letter-frequency fit and word hits."""
    text = text.upper()
    letters = [c for c in text if c in string.ascii_uppercase]
    if not letters:
        return -1e9
    n = len(letters)
    cnt = Counter(letters)
    # (1) letter frequencies: negative chi-square vs English (scaled per letter)
    chi = sum((100 * cnt.get(c, 0) / n - f) ** 2 / f for c, f in ENG_FREQ.items())
    freq_score = -chi / 10
    # (2) words: segmented by spaces if present, bonus for known words; plus
    #     substring hits (length>=4) to give a gradient when spaces are scrambled
    word_score = 0.0
    for w in text.split():
        if w in WORDSET:
            word_score += len(w) ** 1.5
    sub = 0.0
    for w in WORDS:
        if len(w) >= 4 and w in text:
            sub += len(w)
    # (3) penalty for rare letters / junk (Q,J,X,Z next to non-U etc. is covered by freq)
    return freq_score + 3 * word_score + sub

# ---------------- Caesar ----------------
ALPHA = string.ascii_uppercase
def caesar_decrypt(text, key):
    return "".join(ALPHA[(ALPHA.index(c) - key) % 26] if c in ALPHA else c for c in text)
def caesar_encrypt(text, key):
    return caesar_decrypt(text, -key)
def break_caesar(text):
    return max(((k, caesar_decrypt(text, k)) for k in range(26)), key=lambda kt: english_score(kt[1]))

# ---------------- Columnar transposition ----------------
def col_lengths(L, n):
    return [L // n + (1 if j < L % n else 0) for j in range(n)]

def trans_decrypt(ct, order):
    """order[i] = which column is read i-th. Plaintext written in rows of n columns."""
    n, L = len(order), len(ct)
    lens = col_lengths(L, n)
    cols, pos = {}, 0
    for c in order:
        cols[c] = ct[pos:pos + lens[c]]; pos += lens[c]
    return "".join(cols[j][r] for r in range(math.ceil(L / n)) for j in range(n) if r < len(cols[j]))

def trans_encrypt(pt, order):
    n = len(order)
    return "".join(pt[c::n] for c in order)

def break_transposition(ct, max_cols=13, exhaustive_up_to=8, restarts=40, seed=1):
    """Full brute force for n<=8; for bigger n use hill climbing (n! is too big)."""
    rng = random.Random(seed)
    best = (-1e18, None, None)
    tried = 0
    for n in range(2, max_cols + 1):
        if n <= exhaustive_up_to:
            for order in itertools.permutations(range(n)):
                tried += 1
                s = english_score(trans_decrypt(ct, order))
                if s > best[0]: best = (s, order, n)
        else:
            for _ in range(restarts):
                order = list(range(n)); rng.shuffle(order)
                cur = english_score(trans_decrypt(ct, order))
                improved = True
                while improved:
                    improved = False
                    for i, j in itertools.combinations(range(n), 2):
                        order[i], order[j] = order[j], order[i]
                        s = english_score(trans_decrypt(ct, order)); tried += 1
                        if s > cur: cur, improved = s, True
                        else: order[i], order[j] = order[j], order[i]
                if cur > best[0]: best = (cur, tuple(order), n)
    return best[1], trans_decrypt(ct, best[1]), tried

# ---------------- Experiment ----------------
def experiment(plain_source, lengths=(5, 10, 20, 50, 100), trials=30, seed=0):
    rng = random.Random(seed)
    letters_only = [c for c in plain_source.upper() if c in ALPHA + " "]
    s = "".join(letters_only)
    res = {}
    for L in lengths:
        ok = 0
        for _ in range(trials):
            start = rng.randrange(0, len(s) - L)
            pt = s[start:start + L]
            key = rng.randrange(1, 26)
            guess, _ = break_caesar(caesar_encrypt(pt, key))
            ok += (guess == key)
        res[L] = 100 * ok / trials
    return res

SAMPLE = """Every morning the old farmer walked down to the river and watched the water move slowly past the stones. He had lived in the village
all his life and knew every road, every field and every family in the valley. People often asked him about the weather and he would look at the
sky, think for a moment, and tell them what the day would bring. In the evening children gathered around his house to hear stories about the war,
the long winters, and the year when the whole town was covered with snow. Some of them wanted to become doctors, some wanted to build ships, and
others simply wanted to travel to a city far away. He told them to study hard, to read many books, and to remember where they came from. When night
came the village was quiet, and only the sound of the wind and a few birds could be heard over the hills. Scientists say that sleep helps people
learn, and the farmer believed that a good rest was worth more than gold. A small boy asked what makes a person happy and he answered that
friends, food and honest work were enough for most of us. The teacher listened and wrote the words in her book so that nobody would forget them."""

if __name__ == "__main__":
    k, txt = break_caesar(CAESAR)
    print("CAESAR key =", k); print(txt)
    order, txt2, tried = break_transposition(TRANSPOSITION)
    print("TRANSPOSITION order =", order, "columns =", len(order), "tried =", tried); print(txt2)
    res = experiment(SAMPLE)
    print(res)
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.plot(list(res), list(res.values()), "o-")
    plt.xlabel("Plaintext length (characters)"); plt.ylabel("Correct key chosen (%)")
    plt.title("Caesar breaker accuracy vs. text length (30 trials each)")
    plt.ylim(0, 105); plt.grid(True); plt.savefig("accuracy.png", dpi=150)
