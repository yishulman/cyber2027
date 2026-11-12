"""HW2 - student10: Tasks 1-3 (substitution cipher, frequency breaker, hardest letters)"""
from collections import Counter

CIPHER = """CWB OIABDC AKMTBAD RIUMCBN CWB NBBA OAIX K DXKHH YHKMB OHJEMT HIL IZBA CWB CABBD CWB MBL GERJRHB YKCW RIMMBRCD CWB CAKEM DCKCEIM LECW CWB UMEZBADECJ RKXYUD CWB MBLDYKYBA YAEMCBN K RIAABRCEIM KOCBA ABKNBAD MICERBN KM BAAIA EM CWB LBKCWBA ABYIAC K DEMTHB RHIUN RKM LBETW XIAB CWKM K WUMNABN BHBYWKMCD JBC EC OHIKCD KGIZB UD CWB OBDCEZKH BMNBN LECW XUDER EM CWB DVUKAB KMN HETWCD WKMTEMT GBCLBBM CWB CABBD XIDC IO CWB LKCBA IM IUA YHKMBC ED DKHCJ KMN IMHJ K DXKHH YKAC RKM GB UDBN OIA NAEMFEMT CWB XUDBUX IYBMBN K MBL WKHH NBZICBN CI CWB WEDCIAJ IO RINBD XKRWEMBD KMN DBRABC XBDDKTBD HIMT KTI FEMTD DBMC XBDDBMTBAD IM WIADBGKRF KMN K ABYHJ RIUHN CKFB XKMJ LBBFD CI KAAEZB WIMBJ MBZBA DYIEHD GBRKUDB GBBD ABXIZB XIDC IO CWB LKCBA GBOIAB CWBJ DBKH CWB WIMBJRIXG CWB IHN XKY DWILBN AIKND CWKC MI HIMTBA BPEDCBN KMN ZEHHKTBD CWKC WKN GBBM KGKMNIMBN CWB NBCBRCEZB MICERBN CWKC CWB RHIRF EM CWB WKHHLKJ WKN DCIYYBN KC BPKRCHJ XENMETWC ZIHUMCBBAD RHBKMBN CWB GBKRW KMN RIHHBRCBN XIAB YHKDCER GICCHBD CWKM KMJIMB WKN BPYBRCBN BKAHJ RIXYUCBAD OEHHBN BMCEAB AIIXD KMN LBAB HBDD YILBAOUH CWKM K XINBAM RKHRUHKCIA GBOIAB CWB EMZBMCEIM IO RHIRFD YBIYHB XBKDUABN CEXB LECW DKMN LKCBA KMN DWKNILD NIRCIAD ABRIXXBMN NAEMFEMT LKCBA CWAIUTWIUC CWB NKJ BDYBREKHHJ NUAEMT WIC LBKCWBA XIUMCKEMD EM CWB MIACW KAB RIZBABN LECW DMIL OIA WKHO CWB JBKA KMN LECW OHILBAD OIA CWB ABDC LWBM CWB YILBA OKEHBN CWB LWIHB MBETWGIAWIIN TKCWBABN IUCDENB CI HIIF KC CWB DCKAD CWB IARWBDCAK CUMBN CWBEA EMDCAUXBMCD LWEHB CWB KUNEBMRB DHILHJ OIUMN CWBEA DBKCD DIXB GEAND RKM DBMDB CWB XKTMBCER OEBHN IO CWB BKACW KMN UDB EC CI OEMN CWBEA LKJ DIUCW YKYBA LKD IMRB DI BPYBMDEZB CWKC XIMFD DRAKYBN IHN YKTBD RHBKM EM IANBA CI LAECB IM CWBX KTKEM IUA MBETWGIA ABYKEAD IHN AKNEID KMN RKM CBHH LWKC ED LAIMT SUDC GJ HEDCBMEMT CWB RKDCHB LKHHD LBAB GUEHC DI CWERF CWKC RKMMIMD RIUHN GKABHJ NKXKTB CWBX DREBMCEDCD DCUNJEMT CWB NBBY IRBKM WKZB OIUMN KMEXKHD CWKC XKFB CWBEA ILM HETWC EM CICKH NKAFMBDD K DCAIMT LEMN YUDWBN CWB DKEHGIKC KRAIDD CWB HKFB OKDCBA CWKM KMJ IO UD WKN WIYBN"""
ABC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ENG_ORDER = "ETAOINSHRDLCUMWFGYPBVKJXQZ"   # English letters, most to least frequent
LENGTHS = [100, 250, 500, 1000, 2000]

# ======================================================================
# TASK 1: Break the cipher (guided manual decryption, every decision documented)
# ======================================================================
PLAIN2CIPHER = "KGRNBOTWESFHXMIYVADCUZLPJQ"   # plain A..Z -> cipher letter
C2P = {c: p for p, c in zip(ABC, PLAIN2CIPHER)}

DECISIONS = [
    ("C->T, W->H, B->E", "CWB opens the text and is the most frequent word: THE"),
    ("K->A", "K appears as a single-letter word and is very frequent: A"),
    ("O->F, I->O, A->R, D->S", "OIABDC = FOREST (followed by AKMTBAD = RANGERS)"),
    ("M->N, T->G", "AKMTBAD = RANGERS, EMDCAUXBMCD = INSTRUMENTS"),
    ("R->C, U->U, N->D", "RIUMCBN = COUNTED"),
    ("X->M, H->L, Y->P, J->Y", "DXKHH YHKMB OHJEMT = SMALL PLANE FLYING"),
    ("E->I, L->W, Z->V, G->B", "LECW = WITH, IZBA = OVER, GBCLBBM = BETWEEN"),
    ("F->K, P->X", "FEMTD = KINGS, BPKRCHJ = EXACTLY"),
    ("S->J, V->Q", "SUDC GJ = JUST BY, DVUKAB = SQUARE"),
    ("Q->Z", "Plain Z never appears in the text; assigned by elimination "
             "(cipher Q is the only unused letter)"),
]


def decrypt(text, c2p):
    return "".join(c2p.get(ch, ch) for ch in text)


# ======================================================================
# TASK 2: Automatic breaker that maps letters by frequency rank only
# ======================================================================
def freq_break(ct):
    """Most frequent cipher letter -> E, second -> T, and so on."""
    cnt = Counter(ch for ch in ct if ch.isalpha())
    ranked = sorted(cnt, key=lambda c: (-cnt[c], c))   # ties broken alphabetically
    return {c: ENG_ORDER[i] for i, c in enumerate(ranked)}


def evaluate(segment):
    """Compare the automatic mapping with the real key (from Task 1)."""
    guess = freq_break(segment)
    letters = {ch for ch in segment if ch.isalpha()}
    correct = {c for c in letters if guess[c] == C2P[c]}
    chars = [ch for ch in segment if ch.isalpha()]
    char_acc = sum(guess[ch] == C2P[ch] for ch in chars) / len(chars)
    return guess, letters, correct, char_acc


# ======================================================================
# TASK 3: Hardest letters
# Difficulty = average, over the 5 text lengths, of |rank of the letter in the
# text segment - rank of the letter in English|. A large gap means the
# frequency-rank breaker puts the letter in the wrong place.
# ======================================================================
def hardest_letters():
    total_gap = Counter()
    wrong_runs = Counter()
    for n in LENGTHS:
        seg = CIPHER[:n]
        cnt = Counter(C2P[ch] for ch in seg if ch.isalpha())   # plain letter counts
        ranked = sorted(cnt, key=lambda p: (-cnt[p], p))
        guess = freq_break(seg)
        for i, p in enumerate(ranked):
            total_gap[p] += abs(i - ENG_ORDER.index(p))
            if guess[PLAIN2CIPHER[ABC.index(p)]] != p:
                wrong_runs[p] += 1
    avg_gap = {p: total_gap[p] / len(LENGTHS) for p in total_gap}
    return sorted(avg_gap.items(), key=lambda kv: -kv[1]), wrong_runs


if __name__ == "__main__":
    print("=" * 60)
    print("TASK 1: BREAKING THE CIPHER")
    print("=" * 60)
    print("Key (plain A..Z -> cipher):", PLAIN2CIPHER)
    print("Cipher -> plain mapping:")
    print("  " + " ".join(f"{c}->{C2P[c]}" for c in sorted(C2P)))
    print("\nManual decisions and reasons:")
    for mapping, reason in DECISIONS:
        print(f"  {mapping:26s} {reason}")
    print("\nFull decrypted text:\n")
    print(decrypt(CIPHER, C2P))

    print("\n" + "=" * 60)
    print("TASK 2: EXPERIMENT - FREQUENCY-RANK BREAKER")
    print("=" * 60)
    print("Length | correct letters | letters in segment | % correct characters")
    results = {}
    for n in LENGTHS:
        _, letters, correct, char_acc = evaluate(CIPHER[:n])
        results[n] = (len(correct), len(letters), char_acc)
        print(f"{n:6d} | {len(correct):15d} | {len(letters):18d} | {char_acc * 100:6.1f}%")
    print("(Graph of these results: hw2_graph.png)")

    print("\n" + "=" * 60)
    print("TASK 3: THREE HARDEST LETTERS")
    print("=" * 60)
    ranking, wrong_runs = hardest_letters()
    print("Letter | avg rank gap vs English | lengths mapped wrong (out of 5)")
    for p, gap in ranking[:8]:
        print(f"  {p}    | {gap:23.2f} | {wrong_runs[p]}")
    print("\nThe three hardest letters:", ", ".join(p for p, _ in ranking[:3]))
