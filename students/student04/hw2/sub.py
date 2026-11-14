from collections import Counter
from wordfreq import zipf_frequency, top_n_list
import string
import re

MAX_NODES = 500000
GOOD_ENOUGH = 0.90
text = (
        "HDLW SDL QBHLO PKXZLV SDL HDBZL WLXUDCBODBBV UKSDLOLV BASIXVL SB ZBBN "
        "KS SDL ISKOI SDL DXNLOI PBZZBHLV SDL OXGLO PBO SHB VKEI AWSXZ SDLE "
        "OLKMDLV SDL HKSLOPKZZ SDL QXZBS KWWBAWMLV SDKS HL HBAZV ZKWV LKOZE "
        "CLMKAIL BP K ISOBWU SKXZ HXWV SDL WLH CXMEMZL QKSD MBWWLMSI SDL SOKXW "
        "ISKSXBW HXSD SDL AWXGLOIXSE MKFQAI SDL IFKZZ DKOCBO SBHW HBNL IZBHZE KI "
        "SDL PXIDXWU CBKSI OLSAOWLV HXSD SDL FBOWXWU SXVL FBAWSKXWI XW SDL WBOSD "
        "KOL MBGLOLV HXSD IWBH PBO DKZP SDL ELKO KWV HXSD PZBHLOI PBO SDL OLIS "
        "HBZGLI HLOL COBAUDS CKMN SB SDL WKSXBWKZ QKON KWV SDL HDBZL LMBIEISLF "
        "IZBHZE MDKWULV SDL CKNLO ISKOSI HBON KS SDOLL XW SDL FBOWXWU IB SDL "
        "COLKV XI HKOF HDLW SDL IDBQ BQLWI CLLI MBFFAWXMKSL SDL VXOLMSXBW BP "
        "PZBHLOI SB LKMD BSDLO CE QLOPBOFXWU K NXWV BP VKWML SDL FAILAF BQLWLV "
        "K WLH DKZZ VLGBSLV SB SDL DXISBOE BP MBVLI FKMDXWLI KWV ILMOLS FLIIKULI "
        "IMXLWSXISI ISAVEXWU SDL VLLQ BMLKW DKGL PBAWV KWXFKZI SDKS FKNL SDLXO "
        "BHW ZXUDS XW SBSKZ VKONWLII SDL GXZZKUL HLZZ HKI SDL QZKML HDLOL QLBQZL "
        "FLS SKZNLV KWV IDKOLV SDL ZKSLIS WLHI DBWLE WLGLO IQBXZI CLMKAIL CLLI "
        "OLFBGL FBIS BP SDL HKSLO CLPBOL SDLE ILKZ SDL DBWLEMBFC IBFL CXOVI MKW "
        "ILWIL SDL FKUWLSXM PXLZV BP SDL LKOSD KWV AIL XS SB PXWV SDLXO HKE "
        "IBASD SDL SBHW MBAWMXZ GBSLV SB SAOW SDL LFQSE QKONXWU ZBS XWSB K QACZXM "
        "UKOVLW SDL ZXCOKOE BW SDL MBOWLO NLQS XSI VBBOI BQLW ZKSL IB SDKS "
        "ISAVLWSI MBAZV PXWXID SDLXO QOBRLMSI K MKOLPAZ VOXGLO MDLMNI SDL FXOOBOI "
        "CLPBOL MDKWUXWU ZKWLI LGLW BW KW LFQSE OBKV FE UOKWVPKSDLO QZKWSLV K "
        "ZLFBW SOLL XW SDL EKOV SDL ELKO FE FBSDLO HKI CBOW K IQXVLO HLC XI "
        "ISOBWULO PBO XSI HLXUDS SDKW FKWE NXWVI BP ISLLZ FE ZXSSZL COBSDLO KINLV "
        "HDE SDL INE XI CZAL KWV WBWL BP AI MBAZV LTQZKXW XS IXFQZE K FLIIKUL "
        "DXVVLW XWIXVL KW BOVXWKOE ZLSSLO XI FAMD DKOVLO SB WBSXML SDKW K MBVLV "
        "BWL K IXWUZL MZBAV MKW HLXUD FBOL SDKW K DAWVOLV LZLQDKWSI ELS XS "
        "PZBKSI KCBGL AI QLWUAXWI MKWWBS PZE CAS SDLE IHXF IB PKIS SDKS SDLE "
        "ILLF SB PZE SDOBAUD SDL HKSLO GBZAWSLLOI MZLKWLV SDL CLKMD KWV "
        "MBZZLMSLV FBOL QZKISXM CBSSZLI SDKW KWEBWL DKV LTQLMSLV"
    )

common_words = {
    "the": 15, "and": 14, "you": 14,
    "that": 13, "was": 12, "for": 12,
    "are": 11, "with": 11, "his": 10,
    "they": 10, "have": 10, "this": 10,
    "from": 9, "not": 9, "but": 9,
    "she": 9, "her": 8, "one": 8,
    "all": 8, "can": 8, "a": 15,
    "i": 15, "to": 12, "of": 12,
    "in": 11, "it": 11, "is": 11,
    "be": 10, "as": 10, "at": 10,
    "he": 10, "on": 10, "my": 9,
    "we": 9, "do": 9, "if": 8,
    "no": 8, "so": 8
}


def load_dictionary():
    words = set()
    
    with open("en_us.dic", "r", encoding="utf-8") as file:
        for line in file:
            word = line.strip().split("/")[0].lower()
            if word.isalpha() and (len(word) > 1 or word in ("a", "i")):
                words.add(word)


    # Include common inflected forms (plurals, past tense, etc.) from wordfreq
    for word in top_n_list("en", 50000):
        word = word.lower()
        if word.isalpha() and (len(word) > 1 or word in ("a", "i")):
            words.add(word)
    return words


def word_pattern(word):
    letters = {}
    result = []
    for letter in word:
        if letter not in letters:
            letters[letter] = len(letters)
        result.append(letters[letter])
    return tuple(result)


def create_candidates(dictionary):
    candidates = {}
    for word in dictionary:
        key = (len(word), word_pattern(word))
        if key not in candidates:
            candidates[key] = []
        candidates[key].append(word)

    return candidates


def is_compatible(cipher_word, plain_word, mapping, reverse):
    for c, p in zip(cipher_word, plain_word):
        if c in mapping and mapping[c] != p:
            return False
        if p in reverse and reverse[p] != c:
            return False
    return True


def add_mapping(cipher_word, plain_word, mapping, reverse):
    new_mapping = mapping.copy()
    new_reverse = reverse.copy()

    for c, p in zip(cipher_word, plain_word):
        new_mapping[c] = p
        new_reverse[p] = c

    return new_mapping, new_reverse


def calculate_word_score(word):
    score = zipf_frequency(word, "en")
    if word in common_words:
        score += common_words[word] / 10
    return score


def find_mapping(text, dictionary):
    word_counts = Counter(re.findall(r"[A-Za-z]+", text.lower()))
    candidate_index = create_candidates(dictionary)
    candidates = {}

    for word in word_counts:
        key = (len(word), word_pattern(word))
        candidates[word] = candidate_index.get(key, [])
    scores = {}
    for word_list in candidates.values():
        for word in word_list:
            if word not in scores:
                scores[word] = calculate_word_score(word)
    best_mapping = {}
    best_score = float("-inf")
    nodes = 0
    stopped_early = False
    total_occurrences = sum(word_counts.values())

    def search(mapping, reverse, remaining, score, decoded_count):
        nonlocal best_mapping, best_score, nodes, stopped_early
        if nodes >= MAX_NODES or stopped_early:
            return
        nodes += 1
        if not remaining:
            if score > best_score:
                best_score = score
                best_mapping = mapping.copy()
                coverage = decoded_count / total_occurrences
                print("New best:", round(coverage * 100, 2), "% dictionary coverage")
                if coverage >= GOOD_ENOUGH:
                    stopped_early = True
            return
        
        possible_words = {}

        for word in remaining:
            possible_words[word] = [
                candidate
                for candidate in candidates[word]
                if is_compatible(word, candidate, mapping, reverse)
            ]

        chosen_word = min(
            remaining,
            key=lambda w: (len(possible_words[w]), -len(w))
        )
        new_remaining = [w for w in remaining if w != chosen_word]

        possible = sorted(
            possible_words[chosen_word],
            key=lambda word: scores[word],
            reverse=True
        )
        for candidate in possible:
            new_mapping, new_reverse = add_mapping(chosen_word, candidate, mapping, reverse)
            count = word_counts[chosen_word]
            new_score = score + count * scores[candidate]
            search(new_mapping, new_reverse, new_remaining, new_score, decoded_count + count)

            if nodes >= MAX_NODES or stopped_early:
                return
        search(mapping, reverse, new_remaining, score, decoded_count)

    words = list(word_counts.keys())
    search({}, {}, words, 0, 0)

    print("\nSearch nodes:", nodes)
    if stopped_early:
        print("Stopped: good enough solution found.")
    elif nodes >= MAX_NODES:
        print("Stopped: node limit reached.")
    print("Best score:", best_score)
    return {k.upper(): v.upper() for k, v in best_mapping.items()}


def complete_mapping(text, mapping):
    english_letters = "ETAOINSHRDLUCMFWGPYBVKXJQZ"
    counter = Counter(c.upper() for c in text if c.upper() in string.ascii_uppercase)
    used = set(mapping.values())
    for letter, _ in counter.most_common():
        if letter not in mapping:
            for plain in english_letters:
                if plain not in used:
                    mapping[letter] = plain
                    used.add(plain)
                    break

    return mapping


def decrypt(text, mapping):
    result = []
    for letter in text:
        upper = letter.upper()
        if upper in mapping:
            new_letter = mapping[upper]
            if letter.islower():
                new_letter = new_letter.lower()
            result.append(new_letter)
        else:
            result.append(letter)
    return "".join(result)


def main():
    
    dictionary = load_dictionary()
    print("Dictionary loaded:", len(dictionary), "words")
    mapping = find_mapping(text, dictionary)
    mapping = complete_mapping(text, mapping)
    print("\nFINAL MAPPING:")
    for letter in sorted(mapping):
        print(letter, "->", mapping[letter])
    result = decrypt(text, mapping)
    print("\nFINAL DECRYPTION:")
    print(result)
    words = re.findall(r"[A-Za-z]+", result.lower())
    correct = sum(1 for word in words if word in dictionary)

    print("\nDictionary coverage:")
    print(correct, "/", len(words))
    if words:
        print("Percentage:", round(correct / len(words) * 100, 2), "%")

if __name__ == "__main__":
    main()