"""例題 SVG を描くための小さなレンダラ。

例題 1 問は dict で表す:
  id, chapter, title, problem, explain, answer, point
problem / explain / answer は「要素」のリスト。要素は次のいずれか:
  "文章"                 … 通常の行（**強調** が使える）
  "$ 数式"               … 等幅・背景付きの数式行
  ("h", "見出し")         … 解説のステップ見出し
  ("tables", [(ラベル, 行列), ...])  … 行列・表を横に並べる
  ("gap",)               … 少し空ける
"""
import html
import re
import unicodedata

W = 960
M = 40  # 左右マージン
FONT = "'Noto Sans CJK JP','Noto Sans JP','Hiragino Sans','Yu Gothic','Meiryo','IPAGothic',sans-serif"
MONO = "'DejaVu Sans Mono','Menlo','Consolas','Noto Sans Mono CJK JP','IPAGothic',monospace"
FS, LH = 17, 28

C = {
    "head": "#1e3a8a", "headsub": "#c7d2fe", "text": "#1f2937", "mute": "#6b7280",
    "q": "#2563eb", "qbg": "#eff6ff", "e": "#d97706", "ebg": "#fffbeb",
    "a": "#059669", "abg": "#ecfdf5", "em": "#b91c1c", "mathbg": "#f3f4f6",
    "cell": "#ffffff", "cellb": "#94a3b8", "point": "#7c3aed", "pbg": "#f5f3ff",
}


def text_width(s, size, mono=False):
    w = 0.0
    for ch in s:
        if unicodedata.east_asian_width(ch) in "WF":
            w += 1.0
        else:
            w += 0.6 if mono else 0.56
    return w * size


def rich(s, color):
    """**強調** を tspan に変換する。"""
    out = []
    for i, part in enumerate(re.split(r"\*\*(.+?)\*\*", s)):
        p = html.escape(part)
        out.append(f'<tspan font-weight="700" fill="{color}">{p}</tspan>' if i % 2 else p)
    return "".join(out)


class Canvas:
    def __init__(self, pid):
        self.pid, self.y, self.el, self.warn = pid, 0, [], []

    def add(self, s):
        self.el.append(s)

    def check(self, s, x, size, mono=False):
        plain = s.replace("**", "")
        if x + text_width(plain, size, mono) > W - M + 4:
            self.warn.append(f"[{self.pid}] 行がはみ出します: {plain}")

    def line(self, s, x, color, size=FS):
        if s.startswith("$ "):
            body = s[2:]
            self.check(body, x + 12, size - 1, True)
            self.add(f'<rect x="{x}" y="{self.y + 4}" width="{W - M - x - 20}" height="{LH - 2}" rx="4" fill="{C["mathbg"]}"/>')
            self.add(f'<text x="{x + 12}" y="{self.y + 23}" font-family="{MONO}" font-size="{size - 1}" fill="{C["text"]}" xml:space="preserve">{rich(body, C["em"])}</text>')
            self.y += LH + 2
        else:
            self.check(s, x, size)
            self.add(f'<text x="{x}" y="{self.y + 21}" font-size="{size}" fill="{color}" xml:space="preserve">{rich(s, C["em"])}</text>')
            self.y += LH

    def tables(self, x, items):
        cw, ch = 0, 30
        heights = []
        for label, rows in items:
            heights.append(len(rows) * ch)
        top = self.y + 6
        for label, rows in items:
            ncol = max(len(r) for r in rows)
            cw = max(56, max(text_width(str(c), 15, True) for r in rows for c in r) + 18)
            lw = text_width(label, 16) + 10 if label else 0
            th = len(rows) * ch
            if label:
                self.add(f'<text x="{x}" y="{top + th / 2 + 6}" font-size="16" fill="{C["text"]}">{rich(label, C["em"])}</text>')
            gx = x + lw
            for r, row in enumerate(rows):
                for c, val in enumerate(row):
                    cx, cy = gx + c * cw, top + r * ch
                    v = str(val)
                    hl = v.startswith("*")
                    v = v.lstrip("*")
                    fill = "#fee2e2" if hl else C["cell"]
                    self.add(f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" fill="{fill}" stroke="{C["cellb"]}"/>')
                    self.add(f'<text x="{cx + cw / 2}" y="{cy + 20}" text-anchor="middle" font-family="{MONO}" font-size="15" fill="{C["text"]}">{html.escape(v)}</text>')
            x = gx + ncol * cw + 36
        if x - 36 > W - M:
            self.warn.append(f"[{self.pid}] 表がはみ出します")
        self.y = top + max(heights) + 10

    def items(self, items, x, color):
        for it in items:
            if isinstance(it, str):
                self.line(it, x, color)
            elif it[0] == "h":
                self.y += 4
                self.add(f'<text x="{x}" y="{self.y + 21}" font-size="{FS}" font-weight="700" fill="{C["e"]}">{rich(it[1], C["em"])}</text>')
                self.y += LH
            elif it[0] == "tables":
                self.tables(x + 8, it[1])
            elif it[0] == "gap":
                self.y += 10

    def section(self, label, key, items):
        start = self.y
        idx = len(self.el)
        self.y += 46
        self.items(items, M + 24, C["text"])
        self.y += 12
        h = self.y - start
        box = (f'<rect x="{M}" y="{start}" width="{W - 2 * M}" height="{h}" rx="10" fill="{C[key + "bg"]}" stroke="{C[key]}" stroke-width="1.5"/>'
               f'<rect x="{M}" y="{start}" width="6" height="{h}" rx="3" fill="{C[key]}"/>'
               f'<text x="{M + 24}" y="{start + 32}" font-size="20" font-weight="700" fill="{C[key]}">{label}</text>')
        self.el.insert(idx, box)
        self.y += 18


def render(p, total_label="LLM Internals 計算例題集"):
    cv = Canvas(p["id"])
    cv.add(f'<rect x="0" y="0" width="{W}" height="96" fill="{C["head"]}"/>')
    cv.add(f'<text x="{M}" y="36" font-size="15" fill="{C["headsub"]}">{html.escape(total_label)} ・ 第{int(p["id"].split("-")[0])}章 {html.escape(p["chapter"])}</text>')
    cv.add(f'<text x="{M}" y="74" font-size="28" font-weight="700" fill="#ffffff">例題 {p["id"]}　{html.escape(p["title"])}</text>')
    cv.check(f'例題 {p["id"]}　{p["title"]}', M, 28)
    cv.y = 120
    cv.section("問題", "q", p["problem"])
    cv.section("解説", "e", p["explain"])
    cv.section("解答", "a", p["answer"])
    if p.get("point"):
        cv.add(f'<rect x="{M}" y="{cv.y}" width="{W - 2 * M}" height="{LH * len(p["point"]) + 20}" rx="10" fill="{C["pbg"]}"/>')
        cv.y += 10
        for i, s in enumerate(p["point"]):
            cv.line(("★ " if i == 0 else "　 ") + s, M + 20, C["point"])
        cv.y += 28
    H = cv.y + 30
    cv.add(f'<text x="{W - M}" y="{H - 14}" font-size="12" text-anchor="end" fill="{C["mute"]}">参考: github.com/amitshekhariitbhu/llm-internals</text>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">\n'
           f'<rect width="{W}" height="{H}" fill="#ffffff"/>\n' + "\n".join(cv.el) + "\n</svg>\n")
    return svg, cv.warn
