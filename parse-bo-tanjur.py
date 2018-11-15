from pathlib import Path
import re

in_files = Path('rKTs-raw/Tanjur/').glob('*.xml')
out_dir = Path('output/tanjur')
out_dir.mkdir(exist_ok=True)

for f in in_files:
    content = f.read_text()
    # header
    content = re.sub(r'</?outline>', '', content)
    content = re.sub(r'<name>.*?</name>', '', content)
    content = content.replace('<creator type="hasScribe">Bruno Lainé</creator>', '')
    content = content.replace('<?xml version="1.0" encoding="UTF-8"?>', '')
    content = content.replace('<outline xmlns:outline="http://www.tbrc.org/models/outline#">', '')
    # unnecessary tags
    content = re.sub(r'<skttrans>.*?</skttrans>', '', content)
    content = re.sub(r'<coloph>.*?</coloph>', '', content)
    content = re.sub(r'<note>.*?</note>', '', content)
    content = re.sub(r'(</?item>\n?)+', '—', content)
    content = content.replace('—\n—', '\n')
    content = re.sub(r'\n+', '\n', content)
    content = content.strip().strip('—')
    # content
    content = re.sub(r'<rktst>(.*?)</rktst>', r'\1\t', content)
    content = re.sub(r'\n<ref>(.*?)</ref>', r'\1\t', content)
    content = re.sub(r'\n<loc>(.*?)</loc>', r'\1\t', content)
    content = re.sub(r'\n<tib>(.*?)</tib>', r'\1\t', content)

    out_file = out_dir / f'{f.stem}.txt'
    out_file.write_text(content)
