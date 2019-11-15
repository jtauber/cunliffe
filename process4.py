#!/usr/bin/env python3

import re

def greek_char(ch):
    return 0x1F00 <= ord(ch) <= 0x1FFF or 0x0370 <= ord(ch) <= 0x03FF or ord(ch) in [0x304, 0x306]


GRK = "[\u0300-\u03FF\u1F00-\u1FFF]+"
SQ = "\[[^]]+\]"
PR = "\([^)]+\)"
GRM = "( (and|contr\.|1|2|3|sing\.|dual|pl\.|pres\.|impf\.|fut\.|fut\. in mid\. form|aor\.|pf\.|plupf\.|act\.|mid\.|pass\.|pple\.|pa\.|imp\.|subj\.|opt\.|infin\.|nom\.|acc\.|voc\.|genit\.|dat\.|masc\.|fem\.|neut\.|non-thematic pres\.|superl\.|intrans\.|trans\.))+"
REF = "[ΒΗΘΙΛΝΟΦΩδθμω]\d+"
REFLIST = f"{REF}(, ({REF}|\d+))+"
REGEXES = [
    rf"(?P<lemma>{GRK}) (?P<under>{PR}) (?P<etym>{SQ})\.",                      # 0
    rf"(?P<lemma1>{GRK}) (?P<under>{PR})(?P<lemma2>, {GRK}, ὁ)\.",              # 1
    rf"(?P<lemma>{GRK}) (?P<under>{PR})\.",                                     # 2
    rf"(?P<lemma>{GRK}) (?P<etym>{SQ})\.",                                      # 3
    rf"(?P<lemma>{GRK}, -{GRK}, {GRK}) (?P<etym>{SQ})\.",                       # 4
    rf"(?P<lemma>{GRK}, {GRK}) (?P<under>{PR}) (?P<etym>{SQ})\.",               # 5
    rf"(?P<lemma>{GRK}, {GRK}) (?P<etym>{SQ})\.",                               # 6
    rf"(?P<lemma>{GRK}, {GRK} and -{GRK}, -{GRK}) (?P<etym>{SQ})\.",            # 7
    rf"(?P<lemma>{GRK}, {GRK}, -{GRK}) (?P<etym>{SQ})\.",                       # 8
    rf"(?P<lemma>{GRK}, {GRK}, {GRK}) (?P<under>{PR}) (?P<etym>{SQ})\.",        # 9
    rf"(?P<lemma>{GRK}, {GRK}, {GRK}) (?P<under>{PR})\.",                       # 10
    rf"(?P<lemma>{GRK}, {GRK}, {GRK}) (?P<etym>{SQ})\.",                        # 11
    rf"(?P<lemma>{GRK}, {GRK}, {GRK} and -{GRK}, -{GRK}) (?P<etym>{SQ})\.",     # 12
    rf"(?P<lemma>{GRK}, {GRK}, ὁ, ἡ) (?P<etym>{SQ})\.",                         # 13
    rf"(?P<lemma>{GRK}, {GRK}, ὁ, ἡ)\.",                                        # 14
    rf"(?P<lemma>{GRK}, {GRK}, {GRK}), also (?P<also>{GRK}) {REF}\.",           # 15
    rf"(?P<lemma>{GRK}, {GRK}, {GRK}, and -{GRK}, -{GRK}) (?P<etym>{SQ})\.",    # 16
    rf"(?P<lemma>{GRK}, {GRK}, {GRK})\.",                                       # 17
    rf"(?P<lemma>{GRK}, {GRK}, {SQ})\.",                                        # 18
    rf"(?P<lemma>{GRK}, {GRK}, and -{GRK}, -{GRK}) (?P<etym>{SQ})\.",           # 19                   # 19
    rf"(?P<form>{GRK}, {GRK}),(?P<prop>{GRM}) (?P<lemma>{GRK})\.",              # 20
    rf"{GRK}, {GRK},{GRM} {SQ}\.",
    rf"(?P<lemma>{GRK}, {GRK})\.",                                      # 22
    rf"{GRK}, also {GRK} {REF} {SQ}\.",
    rf"{GRK}, also {GRK} {REFLIST} {SQ}\.",
    rf"{GRK}, also {GRK}, {REF}\. {SQ}\.",
    rf"{GRK}, also written {GRK} {PR} {SQ}\.",
    rf"{GRK}, also written {GRK} {SQ}\.",
    rf"(?P<form>{GRK}),(?P<prop>{GRM}) (?P<lemma>{GRK} {PR})\.",        # 28
    rf"{GRK},{GRM} {GRK} {REFLIST}\.",  # @@@
    rf"{GRK},{GRM} {GRK},{GRM} {GRK}\.",
    rf"(?P<form>{GRK}),(?P<prop>{GRM}) (?P<lemma>{GRK})\.",             # 31
    rf"{GRK},{GRM} {PR} {SQ}\.",
    rf"{GRK},{GRM} {SQ}\.",
    rf"{GRK},{GRM} iterative{GRM} {GRK}\.",
    rf"{GRK},{GRM} iterative\.",
    rf"{GRK},{GRM} See {GRK}\.",
    rf"(?P<lemma>{GRK}\(ς\))\.",                                        # 37
    rf"(?P<form>{GRK})(?P<prop>{GRM}) (?P<lemma>{GRK})\.",              # 38
    rf"{GRK}\(ν\) {SQ}\.",
    rf"(?P<lemma>{GRK})\.",                                             # 40
    rf"{GRK}\(ν\),{GRM} {GRK}\.",
    rf"{GRK}, {GRK}, ὁ, ἡ {PR}\.",
    rf"{GRK}, -{GRK}, ἠ\.",
    rf"{GRK}, enclitic\.",
    rf"{GRK},{GRM} {PR}\.",
    rf"{GRK},{GRM} iterative {GRK}\.",
    rf"γέντο, 3 sing. aor. To",
    rf"γόνος, ου, ὁ {SQ}",

    rf"{GRK} =",
    rf"{GRK}=",
    rf"{GRK}, {GRK} =",
    rf"{GRK} {SQ} =",
    rf"{GRK}, {GRK}, ἡ =",
]


def process_mainline(line):
    match = False
    for i, regex in enumerate(REGEXES):
        m = re.match(regex, line)
        if m:
            if i == 0:
                print(f"** {i:02}", m.groupdict()["lemma"])  # under, etym
            elif i == 1:
                print(f"** {i:02}", m.groupdict()["lemma1"] + m.groupdict()["lemma2"])  # under
            elif i == 2:
                print(f"** {i:02}", m.groupdict()["lemma"])  # under
            elif i == 3:
                print(f"** {i:02}", m.groupdict()["lemma"])  # etym
            elif i == 4:
                print(f"** {i:02}", m.groupdict()["lemma"])  # etym
            elif i == 5:
                print(f"** {i:02}", m.groupdict()["lemma"])  # under, etym
            elif i == 6:
                print(f"** {i:02}", m.groupdict()["lemma"])  # etym
            elif i == 8:
                print(f"** {i:02}", m.groupdict()["lemma"])  # etym
            elif i == 9:
                print(f"** {i:02}", m.groupdict()["lemma"])  # under, etym
            elif i == 10:
                print(f"** {i:02}", m.groupdict()["lemma"])  # under
            elif i == 11:
                print(f"** {i:02}", m.groupdict()["lemma"])  # etym
            elif i == 7:
                print(f"** {i:02}", m.groupdict()["lemma"])  # etym
            elif i == 12:
                print(f"** {i:02}", m.groupdict()["lemma"])  # etym
            elif i == 16:
                print(f"** {i:02}", m.groupdict()["lemma"])  # etym
            elif i == 19:
                print(f"** {i:02}", m.groupdict()["lemma"])  # etym
            elif i == 13:
                print(f"** {i:02}", m.groupdict()["lemma"])  # etym
            elif i == 14:
                print(f"** {i:02}", m.groupdict()["lemma"])
            elif i == 17:
                print(f"** {i:02}", m.groupdict()["lemma"])
            elif i == 18:
                print(f"** {i:02}", m.groupdict()["lemma"])
            elif i == 22:
                print(f"** {i:02}", m.groupdict()["lemma"])
            elif i == 37:
                print(f"** {i:02}", m.groupdict()["lemma"])
            elif i == 40:
                print(f"** {i:02}", m.groupdict()["lemma"])

            elif i == 20:
                print(f"** {i:02}", m.groupdict()["form"] + " > " + m.groupdict()["lemma"])  # form, prop
            elif i == 28:
                print(f"** {i:02}", m.groupdict()["form"] + " > " + m.groupdict()["lemma"])  # form, prop
            elif i == 31:
                print(f"** {i:02}", m.groupdict()["form"] + " > " + m.groupdict()["lemma"])  # form, prop
            elif i == 38:
                print(f"** {i:02}", m.groupdict()["form"] + " > " + m.groupdict()["lemma"])  # form, prop

            elif i == 15:
                print(f"** {i:02}", m.groupdict()["lemma"])  # also

            elif i in [41, 42, 43, 44]:
                print(i+16, i, line)
            else:
                print(i + 16, i, m.group(0))
            return
    assert False, line

with open("out2.txt") as f:
    state = 0
    for line in f:
        line = line.rstrip()
        if line:
            if line[0] == "*":
                pass
            elif line[0] == "†":
                pass
            elif greek_char(line[0]):
                process_mainline(line)
            elif line.strip()[0] in "123456789abcdefghijklzABCIV":
                pass
            else:
                assert False, line
