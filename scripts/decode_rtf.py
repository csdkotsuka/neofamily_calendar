import re

with open('prvided data/261024 イベント情報.rtf', 'rb') as f:
    data = f.read()

text = data.decode('latin1')

tokens = re.finditer(r'\\([a-zA-Z]+(-?\d+)? ?|\'([0-9a-fA-F]{2})|\\|\{|\}|u(-?\d+) ?|.)', text)

pos = 0
sjis_buf = bytearray()
out_chars = []
unicode_buf = []

def flush_sjis():
    global sjis_buf
    if sjis_buf:
        try:
            out_chars.append(sjis_buf.decode('shift_jis', errors='replace'))
        except:
            out_chars.append(sjis_buf.decode('latin1'))
        sjis_buf = bytearray()

def flush_unicode():
    global unicode_buf
    if unicode_buf:
        # decode UTF-16 code units (handling surrogates)
        try:
            raw_bytes = bytearray()
            for u in unicode_buf:
                raw_bytes.extend(u.to_bytes(2, 'little'))
            out_chars.append(raw_bytes.decode('utf-16le', errors='replace'))
        except:
            pass
        unicode_buf = []

for m in tokens:
    prefix = text[pos:m.start()]
    if prefix:
        flush_unicode()
        flush_sjis()
        out_chars.append(prefix)
        
    token = m.group(0)
    pos = m.end()
    
    if token.startswith(r"\'"):
        flush_unicode()
        hex_val = int(token[2:4], 16)
        sjis_buf.append(hex_val)
    elif token.startswith(r"\u") and not token.startswith(r"\uc"):
        flush_sjis()
        val_match = re.match(r'\\u(-?\d+)', token)
        if val_match:
            val = int(val_match.group(1))
            if val < 0: val += 65536
            unicode_buf.append(val)
    elif token in (r'\\', r'\{', r'\}'):
        flush_unicode()
        flush_sjis()
        out_chars.append(token[1])
    elif token.startswith(r'\par') or token == "\\\n":
        flush_unicode()
        flush_sjis()
        out_chars.append('\n')
    else:
        flush_unicode()
        flush_sjis()

flush_unicode()
flush_sjis()
full_text = ''.join(out_chars)

with open('scripts/rtf_decoded.txt', 'w', encoding='utf-8') as f:
    f.write(full_text)

print('Successfully decoded RTF with full emoji & surrogates! Total chars:', len(full_text))
