#!/usr/bin/env python3

def greek_char(ch):
    return 0x1F00 <= ord(ch) <= 0x1FFF or 0x0370 <= ord(ch) <= 0x03FF

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
  .s2, .s3, .s22, .s23, .s24, .s25 {
    color: green;
  }
  .s6 {
    color: purple;
  }
  .s4, .s5, .s7, .s8, .s10 {
    color: blue;
  }
  .s13, .s14, .s15, .s16, .s17, .s18, .s19, .s20, .s21 {
    color: orange;
  }
  .s9 {
    color: brown;
  }
  .s11 {
    color: gray;
  }
  .s12 {
    color: #CCC;
  }
</style>
""")
print("<pre>")
with open("cunliffe.txt") as f:
    state = 0
    for line in f:
        line = line.rstrip()
        if line:
            if line[0] == "*":
                if line[1] == "*":
                    assert line == "************************************************************"
                    assert state in [-3, -4, -5, -6, -7, -8, -9, -14, -16, -22, -25], state
                    state = 1  # -> blank line
                elif line[1] == "†":
                    assert state in [-1], state
                    state = 2
                elif greek_char(line[1]):
                    assert state in [-1], state
                    state = 3
                else:
                    assert False, line
            elif line[0] == " ":
                if line.startswith(" " * 3) and line[3] != " ":
                    assert state in [2, 3, 4, 14, 16, 17, 19, 21, 22, 23, 24, 25], state
                    state = 4
                elif line.startswith(" " * 7) and line[7] != " ":
                    assert state in [5, 6], state
                    state = 5
                elif line.startswith(" " * 8) and line[8] != " ":
                    assert state in [-4, -5, -6, -7, -8, -9, -13, -14, -15, -16, -17, -18, -19, -20], state
                    state = 6
                elif line.startswith(" " * 11) and line[11] != " ":
                    assert state in [7, 9], state
                    state = 7
                elif line.startswith(" " * 15) and line[15] != " ":
                    assert state in [8, 11], state
                    state = 8
                elif line.startswith(" " * 16) and line[16] != " ":
                    assert state in [-5, -6, -7, -8, -9, -11], state
                    state = 9
                elif line.startswith(" " * 19) and line[19] != " ":
                    assert state in [10, 12], state
                    state = 10
                elif line.startswith(" " * 24) and line[24] != " ":
                    assert state in [-7, -8, -9, -10], state
                    state = 11
                elif line.startswith(" " * 32) and line[32] != " ":
                    assert state in [-10, -11], state
                    state = 12
                else:
                    assert False, line
            elif line[0] in "123456789":
                if line[1] in ".":
                    if len(line) == 2:
                        assert state in [-4, -5, -6, -7, -14, -25], state
                        state = 13
                    else:
                        assert line[2] == " "
                        assert state in [-4, -5, -6, -7, -9, -14, -21, -22, -25], state
                        state = 14
                elif line[1] in "012345678":
                    assert line[2] == "."
                    if len(line) == 3:
                        assert state in [-4, -6, -14], state
                        state = 15
                    else:
                        assert line[3] == " "
                        assert state in [-4, -5, -14, -16], state
                        state = 16
                else:
                    assert False, line
            elif line[0] in "IV":
                if line.startswith(("I. ", "II. ", "III. ", "IV. ", "V. ")):
                    assert state in [-4, -5, -6, -7, -25], state
                    state = 17
                elif line in ["I.", "II.", "VI."]:
                    assert state in [-4, -7, -25], state
                    state = 18
                else:
                    assert False, line
            elif line[0] in "ABC":
                if line.startswith(("A. ", "B. ", "C. ")):
                    assert state in [-4, -6, -22, -25, -19], state
                    state = 19
                elif line == "B.":
                    assert state in [-6], state
                    state = 20
                else:
                    assert False, line
            elif line[0] in "abcd":
                if line.startswith(("a. ", "b. ", "c. ", "d. ")):
                    assert state in [-4, -25], state
                    state = 21
                else:
                    assert False, line
            elif line[0] == "†":
                if greek_char(line[1]):
                    assert state in [-1], state
                    state = 22
                elif line[1] == "*":
                    assert greek_char(line[2]), line
                    assert state in [-1], state
                    state = 23
                elif line[1] == "†":
                    assert greek_char(line[2]), line
                    assert state in [-1], state
                    state = 24
                else:
                    assert False, line
            elif greek_char(line[0]):
                assert state in [0, -1], state
                state = 25
            else:
                assert False, line
        else:  # blank line
            assert state in [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 25], state
            state = -state

        print(f"""<span class="s{state}">{line}</span> <span class="state">s{state}</span>""")
print("</pre>")
