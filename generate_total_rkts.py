from pathlib import Path

from third_party.wylieconvert import wylie2unicode


def w2u(string):
    module_path = 'third_party/wylieconvert/Lingua-BO-Wylie'
    return wylie2unicode(string, module_path)


def parse_rkts(in_files):
    total = {}
    missing = {}
    m = 0
    for f in in_files:
        content = f.read_text().strip().split('\n')
        for line in content:
            parts = line.split('\t')
            rkts, ed, loc, name = parts[:4]
            bo_name = w2u(name)
            if rkts:
                rkts = int(rkts)
                if rkts not in total:
                    total[rkts] = {}

                if ed not in total[rkts]:
                    total[rkts][ed] = []

                total[rkts][ed].extend([bo_name, loc, name])
            else:
                m += 1
                ref = str(m)
                if ref not in missing:
                    missing[ref] = {}

                if ed not in missing[ref]:
                    missing[ref][ed] = []

                missing[ref][ed].extend([bo_name, loc, name])
    return total, missing


def format_parsed(struct):
    out = ''
    for rkts in sorted(struct.keys()):
        ref = 'K' + str(rkts).rjust(4, '0')
        out += ref + '\n'
        for ed_ref in sorted(struct[rkts].keys()):
            bo_name, loc, name = struct[rkts][ed_ref]
            out += f'\t{ed_ref}\t{bo_name}\t{loc}\t{name}\n'
        out += '\n'
    return out


if __name__ == '__main__':
    in_files = Path('output/tanjur').glob('*.txt')
    parsed, missing = parse_rkts(in_files)
    Path('output/total_rkts.csv').write_text(format_parsed(parsed))
    Path('output/missing_rkts.csv').write_text(format_parsed(missing))
