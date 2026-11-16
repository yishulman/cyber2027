import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from collections import Counter

CIPHERTEXT = """XTVK IDONX MJB XKBXK ACK VJQBKADM RDKWN TR ACK KJOAC JBN PXK DA AT RDBN ACKDO FJU XTPAC J VKXXJQK CDNNKB DBXDNK JB TONDBJOU WKAAKO DX VPMC CJONKO AT BTADMK ACJB J MTNKN TBK IKRTOK ACK DBHKBADTB TR MWTMSX ZKTZWK VKJXPOKN ADVK FDAC XJBN FJAKO JBN XCJNTFX DB ACK NKXKOA ACK AKVZKOJAPOK MJB NOTZ IKRTF ROKKEDBQ NPODBQ J MWKJO BDQCA ACK XMCTTW QJONKB ZOTNPMKN XT VJBU ATVJATKX ACJA FK XCJOKN ACKV FDAC ACK BKDQCITOX NPODBQ ACK KMWDZXK ACK IDONX XATZZKN XDBQDBQ JBN ACK JDO XPNNKBWU RKWA MTWN ACK KBQDBKKOX NKXDQBKN ACK XAJNDPV OTTR XT ACJA DA MTPWN TZKB JBN MWTXK DB AKB VDBPAKX J QTTN ZJXXFTON DX WTBQ OJBNTV JBN BKHKO PXKN TB VTOK ACJB TBK FKIXDAK ZKBQPDBX MJBBTA RWU IPA ACKU XFDV XT RJXA ACJA ACKU XKKV AT RWU ACOTPQC ACK FJAKO XMDKBADXAX XAPNUDBQ ACK NKKZ TMKJB CJHK RTPBN JBDVJWX ACJA VJSK ACKDO TFB WDQCA DB ATAJW NJOSBKXX VTPBAJDBX DB ACK BTOAC JOK MTHKOKN FDAC XBTF RTO CJWR ACK UKJO JBN FDAC RWTFKOX RTO ACK OKXA ACK RTOKXA OJBQKOX MTPBAKN ACK NKKO ROTV J XVJWW ZWJBK RWUDBQ WTF THKO ACK AOKKX FTWHHX FKOK IOTPQCA IJMS AT ACK BJADTBJW ZJOS JBN ACK FCTWK KMTXUXAKV XWTFWU MCJBKOKN ACK VPXKPV TZKBKN J BKF CJWW NKHTAKN AT ACK CDXATOU TR MTNKX VJMCDBKX JMCKT VEXXJQKX TPO BKDQCITO OKZJDOX TWN OJNDTX JBN MJB AKWW FCJA DX FOTBQ GPXA IU WDXAKBDBQ ACK TWN VJZ XCTFKN OTJNX ACJA BT WTBQKO KYDXAKN JBN HDWWJQKX ACJA CJN IKKB JIJBNTBKN J XAOTBQ FDBN ZPXCKN ACK XJDWITJA JMOTXX ACK WJSK RJXAKO ACJB JBU TR PX CJN CTZKN ACK ATFB MTPBMDW HKN AT APOB ACK KVZAU ZJOSDBQ WTA DBAT J ZPIWDM QJONKB OKMUMWDBQ TBK JWPVDBPV MJB XJHKX KBTPQC KBKOQU AT OPB J AKWKHDXDTB RTO XKHKOJW CTPOX XCK SKZA J BTAKITTS TR KHKOU ITTS XCK OKJN FDAC J XCTOA BTAK JITPA KJMC TBK J XZDNKO FKI DX XAOTBQKO RTO DAX FKDQCA ACJB VJBU SDBNX TR XAKKW ACK VJOSKA XKWWX ROKXC ROPDA ROTV ACK HJWWKU KHKOU RODNJU VTOBDBQ CTBKU BKHKO XZTDWX IKMJPXK IKKX OKVTHE VTXA TR ACK FJAKO IKRTOK ACKU XKJW ACK CTBKUMTVI J XDBQWK MWTPN MJB FKDQC VTOK ACJB J CPBNOKN KWKZCJBAX UKA DA RWTJAX JITHK PX ACK ODHKO RWTTNKN ACK RDKWNX KHKOU XZODBQ JBN WKRA IKCDBN ODMH XTDW RTO ACK RJOVEOX"""

# English letters ordered from most to least frequent (E first, T second, ...)
ENGLISH_ORDER = "etaoinshrdlcumwgfypbvkjxqz"

# The key from section 1 (cipher letter -> plain letter)
TRUE_KEY = {
    'a': 't', 'c': 'h', 'k': 'e', 'j': 'a', 't': 'o', 'd': 'i', 'b': 'n',
    'n': 'd', 'o': 'r', 'x': 's', 'w': 'l', 'r': 'f', 'u': 'y', 'i': 'b',
    'm': 'c', 'v': 'm', 'p': 'u', 'q': 'g', 'f': 'w', 'z': 'p', 'h': 'v',
    's': 'k', 'g': 'j', 'e': 'z', 'y': 'x',
}


def frequency_crack(sample):
    """Map cipher letters to English letters by frequency rank only."""
    counts = Counter(c.lower() for c in sample if c.isalpha())
    # most frequent first; ties broken alphabetically so results are deterministic
    ranked = sorted(counts, key=lambda ch: (-counts[ch], ch))
    return {cipher: ENGLISH_ORDER[i] for i, cipher in enumerate(ranked)}


def decrypt(text, mapping):
    return "".join(mapping.get(c.lower(), c) if c.isalpha() else c for c in text)


def evaluate(sample):
    mapping = frequency_crack(sample)
    present = set(c.lower() for c in sample if c.isalpha())
    correct_letters = sum(1 for c in present if mapping.get(c) == TRUE_KEY.get(c))

    truth = decrypt(sample, TRUE_KEY)
    guess = decrypt(sample, mapping)
    letter_positions = [i for i, c in enumerate(sample) if c.isalpha()]
    correct_chars = sum(1 for i in letter_positions if truth[i] == guess[i])
    return correct_letters, len(present), correct_chars / len(letter_positions) * 100, guess


if __name__ == "__main__":
    lengths = [100, 250, 500, 1000, 2000]
    results = []
    print(f"{'Length':>7} | {'Correct letters':>16} | {'Letters in sample':>17} | {'Chars decrypted OK':>18}")
    print("-" * 70)
    for n in lengths:
        correct, present, char_pct, guess = evaluate(CIPHERTEXT[:n])
        results.append((n, correct, present, char_pct))
        print(f"{n:>7} | {correct:>16} | {present:>17} | {char_pct:>17.1f}%")
        print(f"          preview: {guess[:70]}...")

    # ---- Graph ----
    fig, ax1 = plt.subplots(figsize=(8, 5))
    xs = [r[0] for r in results]
    ax1.plot(xs, [r[1] for r in results], marker="o", linewidth=2, color="#1f77b4",
             label="Correctly mapped letters")
    ax1.set_xlabel("Sample length (characters)")
    ax1.set_ylabel("Correctly mapped letters (out of 25)", color="#1f77b4")
    ax1.set_ylim(0, 26)
    ax1.set_xscale("log")
    ax1.set_xticks(xs)
    ax1.set_xticklabels([str(x) for x in xs])
    for x, r in zip(xs, results):
        ax1.annotate(str(r[1]), (x, r[1]), textcoords="offset points", xytext=(0, 8), ha="center")

    ax2 = ax1.twinx()
    ax2.plot(xs, [r[3] for r in results], marker="s", linestyle="--", linewidth=2,
             color="#d62728", label="Characters decrypted correctly (%)")
    ax2.set_ylabel("Characters decrypted correctly (%)", color="#d62728")
    ax2.set_ylim(0, 100)

    lines = ax1.get_lines() + ax2.get_lines()
    ax1.legend(lines, [l.get_label() for l in lines], loc="lower right")
    ax1.set_title("Frequency-only cracker: accuracy vs. sample length")
    ax1.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig("frequency_cracker_graph.png", dpi=150)
    print("Saved graph: frequency_cracker_graph.png")
