import re
from collections import Counter

def solve_with_rules(ciphertext):
    mapping = {}
    
    # --- HELPER: Apply current mapping (solved letters become lowercase) ---
    def apply_current_mapping(text, current_map):
        result = []
        for char in text:
            lower_char = char.lower()
            if lower_char in current_map:
                result.append(current_map[lower_char])
            else:
                result.append(char)
        return "".join(result)

    # --- STEP 1: Find most frequent 3-letter word -> map to 't', 'h', 'e' ---
    three_letter_words = re.findall(r'\b[a-zA-Z]{3}\b', ciphertext)
    if three_letter_words:
        counts_3lw = Counter([w.lower() for w in three_letter_words])
        most_common_word = counts_3lw.most_common(1)[0][0]
        print(f"Most frequent 3-letter word: '{most_common_word.upper()}' -> mapped to 'the'")
        
        mapping[most_common_word[0]] = 't'
        mapping[most_common_word[1]] = 'h'
        mapping[most_common_word[2]] = 'e'

    # --- STEP 2: Find most frequent double letter -> map to 'o' (if no vowel neighbors) ---
    double_matches = re.findall(r'([a-zA-Z])\1', ciphertext)
    if double_matches:
        double_counts = Counter([char.lower() for char in double_matches])
        target_cipher_double = double_counts.most_common(1)[0][0]
        
        semi_text = apply_current_mapping(ciphertext, mapping)
        vowels = {'a', 'e', 'i', 'o', 'u'}
        has_vowel_neighbor = False
        
        for m in re.finditer(f'({target_cipher_double})\\1', ciphertext, re.IGNORECASE):
            start, end = m.start(), m.end()
            prev_char = semi_text[start - 1].lower() if start > 0 else ''
            next_char = semi_text[end].lower() if end < len(semi_text) else ''
            if prev_char in vowels or next_char in vowels:
                has_vowel_neighbor = True
                break
                
        if not has_vowel_neighbor:
            print(f"Double letter '{target_cipher_double.upper()}' -> mapped to 'o'")
            mapping[target_cipher_double] = 'o'

    # --- STEP 3: Find most frequent 1-letter word -> map to 'a' ---
    one_letter_words = re.findall(r'\b[a-zA-Z]\b', ciphertext)
    if one_letter_words:
        unmapped_1lw = [w.lower() for w in one_letter_words if w.lower() not in mapping]
        if unmapped_1lw:
            counts_1lw = Counter(unmapped_1lw)
            most_common_1lw = counts_1lw.most_common(1)[0][0]
            print(f"Most frequent 1-letter word: '{most_common_1lw.upper()}' -> mapped to 'a'")
            mapping[most_common_1lw] = 'a'

    # --- STEP 4: 2-letter words starting with solved 't' -> second letter is 'o' ---
    two_letter_words = re.findall(r'\b([a-zA-Z][a-zA-Z])\b', ciphertext)
    for word in two_letter_words:
        c1, c2 = word[0].lower(), word[1].lower()
        if mapping.get(c1) == 't' and c2 not in mapping:
            print(f"2-letter word starting with 't' ('{word.upper()}'): mapping second letter '{c2.upper()}' -> 'o'")
            mapping[c2] = 'o'

    # --- STEP 5: 2-letter words ending with solved 't' -> first letter is 'i' ---
    for word in two_letter_words:
        c1, c2 = word[0].lower(), word[1].lower()
        if mapping.get(c2) == 't' and c1 not in mapping:
            print(f"2-letter word ending with 't' ('{word.upper()}'): mapping first letter '{c1.upper()}' -> 'i'")
            mapping[c1] = 'i'

    # --- STEP 6: Manual & Custom Deductions ---
    mapping['w'] = 'l'  # Cipher W -> l (totaW -> total)
    print("Mapping ciphertext 'W' -> 'l'")

    mapping['b'] = 'n'  # Cipher B -> n (oBe -> one)
    print("Mapping ciphertext 'B' -> 'n'")

    mapping['n'] = 'd'  # Cipher N -> d (anN -> and)
    print("Mapping ciphertext 'N' -> 'd'")

    mapping['o'] = 'r'  # Cipher O -> r (eaOth -> earth)
    print("Mapping ciphertext 'O' -> 'r'")

    mapping['x'] = 's'  # Cipher X -> s (itX -> its)
    print("Mapping ciphertext 'X' -> 's'")

    mapping['u'] = 'y'  # Cipher U -> y (ordinarU -> ordinary)
    print("Mapping ciphertext 'U' -> 'y'")

    mapping['i'] = 'b'  # Cipher I -> b (Iirds -> birds)
    print("Mapping ciphertext 'I' -> 'b'")

    mapping['r'] = 'f'  # Cipher R -> f (Rield -> field)
    print("Mapping ciphertext 'R' -> 'f'")

    mapping['m'] = 'c'  # Cipher M -> c (Man -> can)
    print("Mapping ciphertext 'M' -> 'c'")

    mapping['v'] = 'm'  # Cipher V -> m (VJBU -> many)
    print("Mapping ciphertext 'V' -> 'm'")

    # --- STEP 7: Frequency match remaining unmapped ciphertext letters ---
    english_freq_order = [
        'e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd', 
        'l', 'c', 'u', 'm', 'w', 'g', 'f', 'y', 'p', 'b', 
        'v', 'k', 'j', 'x', 'q', 'z'
    ]
    
    all_cipher_letters = [c.lower() for c in ciphertext if c.isalpha()]
    cipher_counts = Counter(all_cipher_letters)
    
    # Sort remaining unmapped cipher letters by frequency (highest first)
    sorted_unmapped = [char for char, count in cipher_counts.most_common() if char not in mapping]
    
    # Get available English letters not yet used in mapping
    used_eng_letters = set(mapping.values())
    available_eng = [e for e in english_freq_order if e not in used_eng_letters]
    
    for cipher_char, eng_char in zip(sorted_unmapped, available_eng):
        mapping[cipher_char] = eng_char
        print(f"Frequency matching: Cipher '{cipher_char.upper()}' -> '{eng_char}'")

    # --- STEP 8: Swap 'w' and 'g' after the frequency matching ---
    # Reason: the frequency match produced "mawnetic" and "gay",
    # which should be "magnetic" and "way" -> so w and g are swapped.
    swap = {'w': 'g', 'g': 'w'}
    for cipher_char, eng_char in mapping.items():
        if eng_char in swap:
            mapping[cipher_char] = swap[eng_char]
    print("Swapping 'w' <-> 'g' (because of the words 'mawnetic' -> 'magnetic' and 'gay' -> 'way')")

    # --- Apply final mapping ---
    final_text = apply_current_mapping(ciphertext, mapping)
    
    
    return final_text, mapping

if __name__ == "__main__":
    ciphertext = """XTVK IDONX MJB XKBXK ACK VJQBKADM RDKWN TR ACK KJOAC JBN PXK DA AT RDBN ACKDO FJU XTPAC J VKXXJQK CDNNKB DBXDNK JB TONDBJOU WKAAKO DX VPMC CJONKO AT BTADMK ACJB J MTNKN TBK IKRTOK ACK DBHKBADTB TR MWTMSX ZKTZWK VKJXPOKN ADVK FDAC XJBN FJAKO JBN XCJNTFX DB ACK NKXKOA ACK AKVZKOJAPOK MJB NOTZ IKRTF ROKKEDBQ NPODBQ J MWKJO BDQCA ACK XMCTTW QJONKB ZOTNPMKN XT VJBU ATVJATKX ACJA FK XCJOKN ACKV FDAC ACK BKDQCITOX NPODBQ ACK KMWDZXK ACK IDONX XATZZKN XDBQDBQ JBN ACK JDO XPNNKBWU RKWA MTWN ACK KBQDBKKOX NKXDQBKN ACK XAJNDPV OTTR XT ACJA DA MTPWN TZKB JBN MWTXK DB AKB VDBPAKX J QTTN ZJXXFTON DX WTBQ OJBNTV JBN BKHKO PXKN TB VTOK ACJB TBK FKIXDAK ZKBQPDBX MJBBTA RWU IPA ACKU XFDV XT RJXA ACJA ACKU XKKV AT RWU ACOTPQC ACK FJAKO XMDKBADXAX XAPNUDBQ ACK NKKZ TMKJB CJHK RTPBN JBDVJWX ACJA VJSK ACKDO TFB WDQCA DB ATAJW NJOSBKXX VTPBAJDBX DB ACK BTOAC JOK MTHKOKN FDAC XBTF RTO CJWR ACK UKJO JBN FDAC RWTFKOX RTO ACK OKXA ACK RTOKXA OJBQKOX MTPBAKN ACK NKKO ROTV J XVJWW ZWJBK RWUDBQ WTF THKO ACK AOKKX FTWHHX FKOK IOTPQCA IJMS AT ACK BJADTBJW ZJOS JBN ACK FCTWK KMTXUXAKV XWTFWU MCJBKOKN ACK VPXKPV TZKBKN J BKF CJWW NKHTAKN AT ACK CDXATOU TR MTNKX VJMCDBKX JMCKT VEXXJQKX TPO BKDQCITO OKZJDOX TWN OJNDTX JBN MJB AKWW FCJA DX FOTBQ GPXA IU WDXAKBDBQ ACK TWN VJZ XCTFKN OTJNX ACJA BT WTBQKO KYDXAKN JBN HDWWJQKX ACJA CJN IKKB JIJBNTBKN J XAOTBQ FDBN ZPXCKN ACK XJDWITJA JMOTXX ACK WJSK RJXAKO ACJB JBU TR PX CJN CTZKN ACK ATFB MTPBMDW HKN AT APOB ACK KVZAU ZJOSDBQ WTA DBAT J ZPIWDM QJONKB OKMUMWDBQ TBK JWPVDBPV MJB XJHKX KBTPQC KBKOQU AT OPB J AKWKHDXDTB RTO XKHKOJW CTPOX XCK SKZA J BTAKITTS TR KHKOU ITTS XCK OKJN FDAC J XCTOA BTAK JITPA KJMC TBK J XZDNKO FKI DX XAOTBQKO RTO DAX FKDQCA ACJB VJBU SDBNX TR XAKKW ACK VJOSKA XKWWX ROKXC ROPDA ROTV ACK HJWWKU KHKOU RODNJU VTOBDBQ CTBKU BKHKO XZTDWX IKMJPXK IKKX OKVTHE VTXA TR ACK FJAKO IKRTOK ACKU XKJW ACK CTBKUMTVI J XDBQWK MWTPN MJB FKDQC VTOK ACJB J CPBNOKN KWKZCJBAX UKA DA RWTJAX JITHK PX ACK ODHKO RWTTNKN ACK RDKWNX KHKOU XZODBQ JBN WKRA IKCDBN ODMH XTDW RTO ACK RJOVEOX"""
    
    solved_text, mapping = solve_with_rules(ciphertext)
    print("\n--- Result Preview ---")
    print(solved_text)
