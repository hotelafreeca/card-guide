#!/usr/bin/env python3
"""앱 아이콘 생성 — 초록 배경 + 흰 신용카드 모양. 순수 stdlib PNG 출력."""
import zlib, struct, math, os

def render(size):
    S = 4  # supersample
    W = size * S
    px = bytearray(W * W * 3)

    # colors
    bg_top = (31, 92, 77)    # #1f5c4d
    bg_bot = (18, 61, 50)
    card = (250, 249, 245)   # #faf9f5
    stripe = (42, 43, 48)    # dark stripe
    chip = (212, 175, 55)    # gold chip

    def inside_rrect(x, y, x0, y0, x1, y1, r):
        if x < x0 or x > x1 or y < y0 or y > y1:
            return False
        cx = min(max(x, x0 + r), x1 - r)
        cy = min(max(y, y0 + r), y1 - r)
        return (x - cx) ** 2 + (y - cy) ** 2 <= r * r

    # geometry (in supersampled px)
    m = 0.0  # full-bleed bg; iOS masks corners itself, but round a bit for Android
    bg_r = W * 0.18
    # card: centered, landscape, slight vertical offset
    cw, ch = W * 0.62, W * 0.42
    cx0 = (W - cw) / 2
    cy0 = (W - ch) / 2
    cr = W * 0.045
    # stripe across card near top
    st0 = cy0 + ch * 0.18
    st1 = cy0 + ch * 0.36
    # chip
    chw, chh = cw * 0.16, cw * 0.12
    chx0 = cx0 + cw * 0.10
    chy0 = cy0 + ch * 0.52
    chr = W * 0.012

    for y in range(W):
        t = y / W
        bg = tuple(int(bg_top[i] + (bg_bot[i] - bg_top[i]) * t) for i in range(3))
        row = y * W * 3
        for x in range(W):
            c = bg if inside_rrect(x, y, m, m, W - 1 - m, W - 1 - m, bg_r) else (0, 0, 0)
            if inside_rrect(x, y, cx0, cy0, cx0 + cw, cy0 + ch, cr):
                c = card
                if st0 <= y <= st1:
                    c = stripe
                elif inside_rrect(x, y, chx0, chy0, chx0 + chw, chy0 + chh, chr):
                    c = chip
            o = row + x * 3
            px[o], px[o + 1], px[o + 2] = c
    # downsample S x S
    out = bytearray(size * size * 3)
    for y in range(size):
        for x in range(size):
            r = g = b = 0
            for dy in range(S):
                ro = ((y * S + dy) * W + x * S) * 3
                for dx in range(S):
                    o = ro + dx * 3
                    r += px[o]; g += px[o + 1]; b += px[o + 2]
            n = S * S
            o = (y * size + x) * 3
            out[o], out[o + 1], out[o + 2] = r // n, g // n, b // n
    return out

def write_png(path, size, rgb):
    raw = b''.join(b'\x00' + bytes(rgb[y * size * 3:(y + 1) * size * 3]) for y in range(size))
    def chunk(tag, data):
        c = tag + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c))
    ihdr = struct.pack('>IIBBBBB', size, size, 8, 2, 0, 0, 0)
    png = (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr)
           + chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b''))
    open(path, 'wb').write(png)
    print(path, size, 'x', size, len(png), 'bytes')

os.makedirs('app', exist_ok=True)
for s, name in [(180, 'app/icon-180.png'), (512, 'app/icon-512.png'), (192, 'app/icon-192.png')]:
    write_png(name, s, render(s))
