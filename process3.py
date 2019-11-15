#!/usr/bin/env python3

def greek_char(ch):
    return 0x1F00 <= ord(ch) <= 0x1FFF or 0x0370 <= ord(ch) <= 0x03FF


SEPARATOR = 1
MAIN = 2
LEVEL_0 = 3
LEVEL_1 = 4
LEVEL_2 = 5
LEVEL_3 = 6
LEVEL_4 = 7

print("""
<meta charset="utf-8">
<style>
  pre {
    font-family: Menlo;
  }
  .state {
    font-size: 8pt;
    color: grey;
  }
  .s1 {
    color: red;
  }
  .s2 {
    color: green;
  }
  .s3 {
    color: orange;
  }
  .s4 {
    color: purple;
  }
  .s5 {
    color: brown;
  }
  .s6 {
    color: gray;
  }
  .s7 {
    color: #CCC;
  }
</style>
""")
print("<pre>")
with open("out2.txt") as f:
    state = 0
    for line in f:
        line = line.rstrip()
        if line:
            if line[0] == "*":
                if line[1] == "†":
                    assert state in [SEPARATOR], state
                    state = MAIN
                elif greek_char(line[1]):
                    assert state in [SEPARATOR], state
                    state = MAIN
                else:
                    assert False, line
            elif line[0] == " ":
                if line.startswith(" " * 4) and line[4] != " ":
                    assert state in [LEVEL_0, LEVEL_1, LEVEL_2, LEVEL_3], state
                    state = LEVEL_1
                elif line.startswith(" " * 8) and line[8] != " ":
                    assert state in [LEVEL_1, LEVEL_2, LEVEL_3], state
                    state = LEVEL_2
                elif line.startswith(" " * 12) and line[12] != " ":
                    assert state in [LEVEL_2, LEVEL_3, LEVEL_4], state
                    state = LEVEL_3
                elif line.startswith(" " * 16) and line[16] != " ":
                    assert state in [LEVEL_3, LEVEL_4], state
                    state = LEVEL_4
                else:
                    assert False, line
            elif line[0] in "123456789":
                if line[1] in ".":
                    if len(line) == 2:
                        assert state in [MAIN, LEVEL_0, LEVEL_1, LEVEL_2], state
                        state = LEVEL_0
                    else:
                        assert line[2] == " "
                        assert state in [MAIN, LEVEL_0, LEVEL_1, LEVEL_2], state
                        state = LEVEL_0
                elif line[1] in "012345678":
                    assert line[2] == "."
                    if len(line) == 3:
                        assert state in [LEVEL_0, LEVEL_1], state
                        state = LEVEL_0
                    else:
                        assert line[3] == " "
                        assert state in [LEVEL_0, LEVEL_1], state
                        state = LEVEL_0
                else:
                    assert False, line
            elif line[0] in "IV":
                if line.startswith(("I. ", "II. ", "III. ", "IV. ", "V. ")):
                    assert state in [MAIN, LEVEL_0, LEVEL_1, LEVEL_2], state
                    state = LEVEL_0
                elif line in ["I.", "II.", "VI."]:
                    assert state in [MAIN, LEVEL_0, LEVEL_2], state
                    state = LEVEL_0
                else:
                    assert False, line
            elif line[0] in "ABC":
                if line.startswith(("A. ", "B. ", "C. ")):
                    assert state in [MAIN, LEVEL_0, LEVEL_1], state
                    state = LEVEL_0
                elif line == "B.":
                    assert state in [LEVEL_1], state
                    state = LEVEL_0
                else:
                    assert False, line
            elif line[0] in "abcd":
                if line.startswith(("a. ", "b. ", "c. ", "d. ")):
                    assert state in [MAIN, LEVEL_0], state
                    state = LEVEL_0
                else:
                    assert False, line
            elif line[0] == "†":
                if greek_char(line[1]):
                    assert state in [SEPARATOR], state
                    state = MAIN
                elif line[1] == "*":
                    assert greek_char(line[2]), line
                    assert state in [SEPARATOR], state
                    state = MAIN
                elif line[1] == "†":
                    assert greek_char(line[2]), line
                    assert state in [SEPARATOR], state
                    state = MAIN
                else:
                    assert False, line
            elif greek_char(line[0]):
                assert state in [0, SEPARATOR], state
                state = MAIN
            else:
                assert False, line
        else:  # blank line
            assert state in [MAIN, LEVEL_0, LEVEL_1, LEVEL_2, LEVEL_3], state
            state = SEPARATOR

        print(f"""<span class="s{state}">{line}</span> <span class="state">s{state}</span>""")
print("</pre>")
