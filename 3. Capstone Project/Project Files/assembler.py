import sys

PREDEFINED = {
    "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
    "SCREEN": 16384, "KBD": 24576
}
for i in range(16):
    PREDEFINED[f"R{i}"] = i

COMP = {
    "0": "0101010", "1": "0111111", "-1": "0111010",
    "D": "0001100", "A": "0110000", "!D": "0001101", "!A": "0110001",
    "-D": "0001111", "-A": "0110011", "D+1": "0011111", "A+1": "0110111",
    "D-1": "0001110", "A-1": "0110010", "D+A": "0000010", "D-A": "0010011",
    "A-D": "0000111", "D&A": "0000000", "D|A": "0010101",
    "M": "1110000", "!M": "1110001", "-M": "1110011", "M+1": "1110111",
    "M-1": "1110010", "D+M": "1000010", "D-M": "1010011", "M-D": "1000111",
    "D&M": "1000000", "D|M": "1010101"
}

DEST = {
    "": "000", "M": "001", "D": "010", "MD": "011", "DM": "011",
    "A": "100", "AM": "101", "MA": "101", "AD": "110", "DA": "110",
    "AMD": "111", "ADM": "111", "MAD": "111", "MDA": "111", "DAM": "111", "DMA": "111"
}

JUMP = {
    "": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"
}


def valid_symbol(s):
    if not s:
        return False
    first = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_.$:"
    rest = first + "0123456789"
    return s[0] in first and all(c in rest for c in s[1:])


def translate_c(inst):
    dest, rest = "", inst
    if "=" in inst:
        parts = inst.split("=")
        if len(parts) != 2:
            return None
        dest, rest = parts[0].strip(), parts[1].strip()

    comp, jump = rest, ""
    if ";" in rest:
        parts = rest.split(";")
        if len(parts) != 2:
            return None
        comp, jump = parts[0].strip(), parts[1].strip()

    if dest not in DEST or comp not in COMP or jump not in JUMP:
        return None
    return "111" + COMP[comp] + DEST[dest] + JUMP[jump]


def main():
    if len(sys.argv) != 2:
        print("Usage: python assembler.py file.asm")
        return

    in_file = sys.argv[1]
    with open(in_file, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()

    symbols = dict(PREDEFINED)
    clean_lines = []
    rom_addr = 0

    # First reading: remove comments/blank lines and record labels
    for line_no, line in enumerate(raw_lines, start=1):
        if "//" in line:
            line = line[:line.index("//")]
        line = line.strip()
        if not line:
            continue

        if line.startswith("(") and line.endswith(")"):
            label = line[1:-1].strip()
            if not valid_symbol(label):
                print(f"Line {line_no}: invalid instruction")
                return
            if label not in symbols:
                symbols[label] = rom_addr
        else:
            clean_lines.append((line_no, line))
            rom_addr += 1

    # Second reading: convert to 16 bits, variables start at RAM 16
    next_var = 16
    output = []

    for line_no, inst in clean_lines:
        if inst.startswith("@"):
            val = inst[1:].strip()
            if val.isdigit():
                num = int(val)
                if num < 0 or num > 32767:
                    print(f"Line {line_no}: invalid instruction")
                    return
                output.append(f"{num:016b}")
            else:
                if not valid_symbol(val):
                    print(f"Line {line_no}: invalid instruction")
                    return
                if val not in symbols:
                    symbols[val] = next_var
                    next_var += 1
                output.append(f"{symbols[val]:016b}")
        else:
            bits = translate_c(inst)
            if bits is None:
                print(f"Line {line_no}: invalid instruction")
                return
            output.append(bits)

    out_file = in_file[:-4] + ".hack" if in_file.endswith(".asm") else in_file + ".hack"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("\n".join(output) + "\n")


if __name__ == "__main__":
    main()