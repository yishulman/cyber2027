"""
Homework 2 - student11
Monoalphabetic substitution analysis and frequency-only experiment.

Run:
    python hw2.py

Requires matplotlib:
    python -m pip install matplotlib

The key was recovered from the repeated word patterns and readable plaintext.
Important: ciphertext symbols F and Z never occur, so their plaintext
assignments cannot be determined from this ciphertext. The script uses
F->J and Z->Z as one arbitrary completion; swapping those two is equally
consistent with the supplied ciphertext.
"""
from collections import Counter
import random
import string
import matplotlib.pyplot as plt

CIPHERTEXT = """V PNOCHL BJHQ YDPISQ NIS PVJRKCVN VAOCPP NIS RVXS EVPNSO NIVH VHG CE DP IVQ ICYSQ WCRDHNSSOP ARSVHSQ NIS KSVAI VHQ ACRRSANSQ MCOS YRVPNJA KCNNRSP NIVH VHGCHS IVQ STYSANSQ OSAGARJHL CHS VRDMJHDM AVH PVWSP SHCDLI SHSOLG NC ODH V NSRSWJPJCH ECO PSWSOVR ICDOP NIS EJOS QSYVONMSHN WJPJNSQ NIS PAICCR NC NSVAI AIJRQOSH ICB NC RSVWS V KDJRQJHL PVESRG CDO NSVAISO KSRJSWSP NIVN NIS KSPN BVG NC DHQSOPNVHQ VH JQSV JP NC STYRVJH JN NC V EOJSHQ MCPN CE NIS BVNSO CH CDO YRVHSN JP PVRNG VHQ CHRG V PMVRR YVON AVH KS DPSQ ECO QOJHXJHL NIS ECCNKVRR NSVM YOVANJASQ JH NIS OVJH DHNJR NIS ACVAI EJHVRRG PSHN SWSOGCHS ICMS V AVOSEDR QOJWSO AISAXP NIS MJOOCOP KSECOS AIVHLJHL RVHSP SWSH CH VH SMYNG OCVQ QCANCOP OSACMMSHQ QOJHXJHL BVNSO NIOCDLICDN NIS QVG SPYSAJVRRG QDOJHL ICN BSVNISO NIS MDPSDM CYSHSQ V HSB IVRR QSWCNSQ NC NIS IJPNCOG CE ACQSP MVAIJHSP VHQ PSAOSN MSPPVLSP PAJSHNJPNP PNDQGJHL NIS QSSY CASVH IVWS ECDHQ VHJMVRP NIVN MVXS NISJO CBH RJLIN JH NCNVR QVOXHSPP CDO ARVPP WJPJNSQ V EVOM BISOS NIS ACBP BCOS ACRRVOP NIVN PSHN NISJO RCAVNJCH NC V YICHS KSSP ACMMDHJAVNS NIS QJOSANJCH CE ERCBSOP NC SVAI CNISO KG YSOECOMJHL V XJHQ CE QVHAS V LCCQ YVPPBCOQ JP RCHL OVHQCM VHQ HSWSO DPSQ CH MCOS NIVH CHS BSKPJNS ICHSG HSWSO PYCJRP KSAVDPS KSSP OSMCWS MCPN CE NIS BVNSO KSECOS NISG PSVR NIS ICHSGACMK NIS ESPNJWVR SHQSQ BJNI MDPJA JH NIS PUDVOS VHQ RJLINP IVHLJHL KSNBSSH NIS NOSSP NIS OJWSO ERCCQSQ NIS EJSRQP SWSOG PYOJHL VHQ RSEN KSIJHQ OJAI PCJR ECO NIS EVOMSOP V PJHLRS ARCDQ AVH BSJLI MCOS NIVH V IDHQOSQ SRSYIVHNP GSN JN ERCVNP VKCWS DP NIS CRQ MVY PICBSQ OCVQP NIVN HC RCHLSO STJPNSQ VHQ WJRRVLSP NIVN IVQ KSSH VKVHQCHSQ BISH NIS YCBSO EVJRSQ NIS BICRS HSJLIKCOICCQ LVNISOSQ CDNPJQS NC RCCX VN NIS PNVOP NIS NOVJH BVP QSRVGSQ KSAVDPS V NOSS IVQ EVRRSH VAOCPP NIS NOVAXP QDOJHL NIS PNCOM NIS AVPNRS BVRRP BSOS KDJRN PC NIJAX NIVN AVHHCHP ACDRQ KVOSRG QVMVLS NISM QDOJHL NIS SARJYPS NIS KJOQP PNCYYSQ PJHLJHL VHQ NIS VJO PDQQSHRG ESRN ACRQ NIS PMVRR IVOKCO NCBH BCXS PRCBRG VP NIS EJPIJHL KCVNP OSNDOHSQ BJNI NIS MCOHJHL NJQS"""

ALPHABET = string.ascii_uppercase
ENGLISH_ORDER = "ETAOINSHRDLCUMWFGYPBVKXJQZ"

# 24 mappings observed and confirmed from the plaintext.
KNOWN_KEY = {
    "V":"A", "P":"S", "N":"T", "O":"R", "C":"O", "H":"N",
    "L":"G", "B":"W", "J":"I", "Q":"D", "Y":"P", "D":"U",
    "I":"H", "S":"E", "R":"L", "K":"B", "A":"C", "X":"K",
    "E":"F", "G":"Y", "W":"V", "M":"M", "T":"X", "U":"Q"
}

# One arbitrary completion of the two unused cipher symbols.
KEY = dict(KNOWN_KEY)
KEY["F"] = "J"
KEY["Z"] = "Z"

def decrypt(text, mapping):
    return "".join(mapping.get(ch, ch) for ch in text)

def frequency_solver(sample):
    counts = Counter(ch for ch in sample if ch in ALPHABET)
    ranked = sorted(ALPHABET, key=lambda ch: (-counts[ch], ch))
    return {ranked[i]: ENGLISH_ORDER[i] for i in range(26)}

def count_correct(prediction, observed_symbols):
    return sum(prediction[ch] == KNOWN_KEY[ch] for ch in observed_symbols)

def insert_random_letters_between_words(text, rng):
    words = text.split()
    result = []
    for i, word in enumerate(words):
        result.append(word)
        if i < len(words) - 1:
            result.append(rng.choice(ALPHABET))
    return " ".join(result)

def encrypt(text, mapping):
    inverse = {plain:cipher for cipher, plain in mapping.items()}
    return "".join(inverse.get(ch, ch) for ch in text)

def main():
    plaintext = decrypt(CIPHERTEXT, KEY)
    print("DECRYPTED TEXT:")
    print(plaintext)
    print("\\nFrequency-only experiment:")
    lengths = [100, 250, 500, 1000, 2000]
    correct_values = []
    denominators = []

    for length in lengths:
        sample = CIPHERTEXT[:length]
        prediction = frequency_solver(sample)
        observed = {ch for ch in sample if ch in KNOWN_KEY}
        correct = count_correct(prediction, observed)
        correct_values.append(correct)
        denominators.append(len(observed))
        print(f"{length} chars: {correct}/{len(observed)} correct")

    plt.figure(figsize=(8, 5))
    plt.plot(lengths, correct_values, marker="o")
    for x, y, d in zip(lengths, correct_values, denominators):
        plt.annotate(f"{y}/{d}", (x, y), textcoords="offset points",
                     xytext=(0, 9), ha="center")
    plt.title("Frequency-only substitution solver: correct mappings")
    plt.xlabel("Prefix length (characters, including spaces)")
    plt.ylabel("Correct mappings among observed cipher letters")
    plt.xticks(lengths)
    plt.ylim(0, 26)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("frequency_graph.png", dpi=180)
    plt.show()

    # Random-letter experiment: one random single-letter word between
    # every pair of words, repeated 30 times.
    rng = random.Random(20261114)
    scores = []
    for _ in range(30):
        noisy_plain = insert_random_letters_between_words(plaintext, rng)
        noisy_cipher = encrypt(noisy_plain, KEY)
        prediction = frequency_solver(noisy_cipher)
        scores.append(count_correct(prediction, set(KNOWN_KEY)))

    print("\\nRandom-letter experiment (30 trials):")
    print("Baseline:", count_correct(frequency_solver(CIPHERTEXT), set(KNOWN_KEY)),
          "/", len(KNOWN_KEY))
    print("Average:", sum(scores) / len(scores), "/", len(KNOWN_KEY))
    print("Minimum:", min(scores), "Maximum:", max(scores))

if __name__ == "__main__":
    main()
