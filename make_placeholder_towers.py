#!/usr/bin/env python3
"""Generate placeholder pixel-art animated GIFs (idle + attack) for new towers.
Sprites face RIGHT by default, matching SPRITE_FACING_OFFSET_DEG = 0 in index.html.
Swap these out for real art later — just keep the same filenames."""
from PIL import Image, ImageDraw

S = 24          # base resolution (pixel-art grid)
SCALE = 4       # upscale factor -> 96px sprite, crisp blocky pixels
DUR = 140       # ms per frame

def new():
    return Image.new("RGBA", (S, S), (0, 0, 0, 0))

def save(frames, name):
    big = [f.resize((S * SCALE, S * SCALE), Image.NEAREST) for f in frames]
    big[0].save(name, save_all=True, append_images=big[1:],
                duration=DUR, loop=0, disposal=2, transparency=0)
    print("wrote", name)

# ---------- BASIC TOWER: stubby steel cannon, barrel points right ----------
def basic_frame(bob=0, recoil=0, flash=False):
    im = new(); d = ImageDraw.Draw(im)
    y = bob
    # stone base
    d.polygon([(6, 22), (18, 22), (16, 18), (8, 18)], fill=(90, 96, 110, 255))
    d.rectangle([7, 17 + y, 17, 18 + y], fill=(70, 76, 90, 255))
    # steel body
    d.rectangle([8, 10 + y, 16, 18 + y], fill=(96, 128, 196, 255))
    d.rectangle([8, 10 + y, 16, 11 + y], fill=(150, 180, 230, 255))   # top highlight
    d.rectangle([8, 10 + y, 9, 18 + y], fill=(60, 88, 150, 255))       # left shade
    # barrel (points right), recoils left on attack
    bx = 16 - recoil
    d.rectangle([bx, 12 + y, bx + 6, 15 + y], fill=(58, 64, 78, 255))
    d.rectangle([bx, 12 + y, bx + 6, 12 + y], fill=(110, 116, 130, 255))
    if flash:
        d.ellipse([bx + 5, 11 + y, bx + 10, 16 + y], fill=(255, 214, 120, 255))
        d.ellipse([bx + 6, 12 + y, bx + 9, 15 + y], fill=(255, 250, 210, 255))
    return im

basic_idle = [basic_frame(bob=0), basic_frame(bob=0), basic_frame(bob=-1), basic_frame(bob=-1)]
basic_attack = [basic_frame(recoil=0, flash=True), basic_frame(recoil=3, flash=True),
                basic_frame(recoil=3), basic_frame(recoil=1), basic_frame(recoil=0)]
save(basic_idle, "basic_idle.gif")
save(basic_attack, "basic_attack.gif")

# ---------- ARCHER TOWER: hooded figure with a bow, faces right ----------
def archer_frame(draw_amt=0, sway=0):
    im = new(); d = ImageDraw.Draw(im)
    x = sway
    # legs / platform
    d.rectangle([9 + x, 19, 15 + x, 22], fill=(74, 60, 44, 255))
    # green tunic body
    d.rectangle([8 + x, 12, 15 + x, 20], fill=(56, 142, 78, 255))
    d.rectangle([8 + x, 12, 15 + x, 13], fill=(96, 190, 118, 255))     # highlight
    # head + hood
    d.ellipse([9 + x, 6, 15 + x, 12], fill=(228, 190, 150, 255))       # face
    d.polygon([(8 + x, 10), (8 + x, 6), (16 + x, 6), (16 + x, 10)], fill=(40, 110, 62, 255))  # hood
    d.rectangle([8 + x, 5, 16 + x, 7], fill=(40, 110, 62, 255))
    # bow arc on the right, string pulled back by draw_amt
    d.arc([16 + x, 6, 22 + x, 20], start=-70, end=70, fill=(120, 80, 40, 255), width=1)
    tip_x = 22 + x
    string_x = 17 + x - draw_amt
    d.line([(tip_x, 7), (string_x, 13), (tip_x, 19)], fill=(210, 210, 210, 255), width=1)
    # nocked arrow
    d.line([(string_x, 13), (string_x + 6 + draw_amt, 13)], fill=(180, 140, 90, 255), width=1)
    d.polygon([(string_x + 6 + draw_amt, 12), (string_x + 8 + draw_amt, 13),
               (string_x + 6 + draw_amt, 14)], fill=(200, 200, 200, 255))
    return im

archer_idle = [archer_frame(sway=0), archer_frame(sway=0), archer_frame(sway=1), archer_frame(sway=1)]
archer_attack = [archer_frame(draw_amt=0), archer_frame(draw_amt=2),
                 archer_frame(draw_amt=4), archer_frame(draw_amt=4), archer_frame(draw_amt=0)]
save(archer_idle, "archer_idle.gif")
save(archer_attack, "archer_attack.gif")

print("done")
