# -*- coding: utf-8 -*-
"""Convert paper/main.tex to a readable HTML review copy (numbers current)."""
import re, html, pathlib

SRC = pathlib.Path("paper/main.tex")
DST = pathlib.Path("paper/main_review_r24.html")

t = SRC.read_text(encoding="utf-8")

# Take document body only
m = re.search(r"\\begin\{document\}(.*)\\end\{document\}", t, re.S)
body = m.group(1)

# Drop comments (unescaped %)
body = re.sub(r"(?<!\\)%.*", "", body)

# Title / abstract
title_m = re.search(r"\\title\{([^}]*)\}", t)
title = title_m.group(1) if title_m else "Review copy"

out = []
out.append("<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'>")
out.append("<title>" + html.escape(title) + " (review copy R24)</title>")
out.append("<style>body{max-width:900px;margin:2em auto;font-family:Georgia,serif;line-height:1.65;padding:0 1em;}"
           "h1{font-size:1.5em;}h2{font-size:1.25em;margin-top:1.8em;border-bottom:1px solid #ccc;padding-bottom:.3em;}"
           "h3{font-size:1.1em;}table{border-collapse:collapse;margin:1em 0;font-size:.9em;}"
           "th,td{border:1px solid #999;padding:4px 8px;text-align:left;}"
           ".abstract{background:#f7f7f7;padding:1em;border-left:4px solid #888;}"
           ".math{font-family:monospace;background:#f4f4f4;padding:0 2px;}"
           ".note{background:#fff8e1;padding:.6em;border:1px dashed #aaa;margin:1em 0;}"
           "li{margin:.3em 0;}</style></head><body>")
out.append("<h1>" + html.escape(title) + "</h1>")
out.append("<p><b>审稿版说明：</b>由当前 main.tex（含 R22/R24 全部改数）自动转换，公式保留 LaTeX 源码，tikz 图以占位说明代替。旧 PDF（9-7 编）数字已过期，以此版为准。</p>")

def esc(s):
    return html.escape(s)

# Token-based lightweight conversion over body, line by line
lines = body.split("\n")
html_lines = []
in_tabular = False
in_itemize = False
in_abstract = False
para_buf = []

def flush_para():
    if para_buf:
        txt = " ".join(para_buf)
        txt = inline(txt)
        html_lines.append("<p>" + txt + "</p>")
        para_buf.clear()

def inline(s):
    # order matters
    s = re.sub(r"\\cjktext\{([^}]*)\}", r"\1", s)
    s = re.sub(r"\\begin\{CJK\}.*", "", s)
    s = re.sub(r"\\end\{CJK\}.*", "", s)
    s = re.sub(r"\\textbf\{([^}]*)\}", r"<b>\1</b>", s)
    s = re.sub(r"\\textit\{([^}]*)\}", r"<i>\1</i>", s)
    s = re.sub(r"\\emph\{([^}]*)\}", r"<i>\1</i>", s)
    s = re.sub(r"\\texttt\{([^}]*)\}", r"<code>\1</code>", s)
    s = re.sub(r"\\url\{([^}]*)\}", r"<code>\1</code>", s)
    s = re.sub(r"\\footnote\{([^}]*)\}", r" [\1]", s)
    s = re.sub(r"\\cite\{([^}]*)\}", r" [\1]", s)
    s = re.sub(r"\\ref\{([^}]*)\}", r" [\1]", s)
    s = re.sub(r"\\label\{[^}]*\}", "", s)
    # math spans -> code style (escape first, then restore wrappers)
    parts = re.split(r"(\$[^$]+\$|\\\(.*?\\\))", s)
    for i, p in enumerate(parts):
        if p.startswith("$") or p.startswith("\\("):
            parts[i] = "<span class='math'>" + esc(p) + "</span>"
        else:
            p = esc(p)
            p = p.replace("\\%", "%").replace("\\&", "&amp;").replace("\\_", "_")
            p = p.replace("---", "—").replace("--", "–")
            p = p.replace("\\ ", " ").replace("~", " ")
            p = re.sub(r"\\\\", "<br>", p)
            parts[i] = p
    return "".join(parts)

for ln in lines:
    s = ln.strip()
    if not s:
        if not in_tabular:
            flush_para()
        continue
    if s.startswith("\\maketitle"):
        continue
    m_abs = re.match(r"\\begin\{abstract\}", s)
    if m_abs:
        flush_para(); in_abstract = True
        html_lines.append("<div class='abstract'><b>Abstract.</b> "); continue
    if s.startswith("\\end{abstract}"):
        flush_para(); in_abstract = False
        html_lines.append("</div>"); continue
    m_sec = re.match(r"\\section\{(.+)\}", s)
    if m_sec:
        flush_para(); html_lines.append("<h2>" + inline(m_sec.group(1)) + "</h2>"); continue
    m_sub = re.match(r"\\subsection\{(.+)\}", s)
    if m_sub:
        flush_para(); html_lines.append("<h3>" + inline(m_sub.group(1)) + "</h3>"); continue
    if re.match(r"\\begin\{(itemize|enumerate)\}", s):
        flush_para(); in_itemize = True; html_lines.append("<ul>"); continue
    if re.match(r"\\end\{(itemize|enumerate)\}", s):
        flush_para(); in_itemize = False; html_lines.append("</ul>"); continue
    m_item = re.match(r"\\item\s?(.*)", s)
    if m_item and in_itemize:
        flush_para(); html_lines.append("<li>" + inline(m_item.group(1)) + "</li>"); continue
    if re.match(r"\\begin\{table\}", s):
        flush_para(); html_lines.append("<div class='note'>[Table below]</div>"); continue
    if re.match(r"\\end\{table\}", s):
        continue
    m_cap = re.match(r"\\caption\{(.+)\}", s)
    if m_cap:
        html_lines.append("<p><b>Caption:</b> " + inline(m_cap.group(1)) + "</p>"); continue
    m_tab = re.match(r"\\begin\{tabular\}\{([^}]*)\}", s)
    if m_tab:
        flush_para(); in_tabular = True
        html_lines.append("<table>"); continue
    if s.startswith("\\end{tabular}"):
        in_tabular = False; html_lines.append("</table>"); continue
    if re.match(r"\\begin\{figure\}", s):
        flush_para(); html_lines.append("<div class='note'>[Figure below]</div>"); continue
    if re.match(r"\\end\{figure\}", s):
        continue
    if re.match(r"\\begin\{tikzpicture\}", s):
        flush_para()
        html_lines.append("<div class='note'>[tikz 流程图：见 tex 源码 / 旧 PDF；审稿版暂略图形]</div>")
        # skip until end tikzpicture
        continue
    if in_tabular:
        if s.startswith("\\hline") or s.startswith("\\toprule") or s.startswith("\\midrule") or s.startswith("\\bottomrule"):
            continue
        row = s.rstrip("\\").strip()
        if row.endswith("\\\\"):
            row = row[:-2]
        cells = [inline(c.strip()) for c in row.split("&")]
        tag = "td"
        html_lines.append("<tr>" + "".join("<%s>%s</%s>" % (tag, c, tag) for c in cells) + "</tr>")
        continue
    if s.startswith("\\"):
        # other commands alone on a line: skip (e.g. \centering, \label)
        continue
    para_buf.append(s)

flush_para()
out.extend(html_lines)
out.append("</body></html>")
DST.write_text("\n".join(out), encoding="utf-8")
print("wrote", DST, DST.stat().st_size, "bytes")
