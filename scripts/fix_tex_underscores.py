"""Escape bare underscores in text mode (build fix, no content/number changes)."""
import re

P = "paper/main.tex"
lines = open(P, encoding="utf-8").read().split("\n")

# Protect: \(...\) math, $...$ math spans per line (no multiline math in this file
# except tikz/equation envs which we skip wholesale by environment tracking).
in_env = False
fixed = 0
out = []
for ln in lines:
    if re.search(r"\\begin\{(equation|align|tikzpicture|table|tabular|figure)\}", ln):
        in_env = True
    if in_env:
        out.append(ln)
        if re.search(r"\\end\{(equation|align|tikzpicture|table|tabular|figure)\}", ln):
            in_env = False
        continue
    # split out $...$ spans (keep delimiters); hide \$ first
    work = ln.replace("\\$", "\x00")
    parts = re.split(r"(\$[^$]*\$)", work)
    for i, p in enumerate(parts):
        if i % 2 == 1:  # math span, leave alone
            continue
        # escape _ not already escaped and not inside \command{...} args of
        # label/ref/cite/input/bibliography/bibliographystyle
        def fix_seg(seg):
            res = []
            j = 0
            while j < len(seg):
                ch = seg[j]
                if ch == "\\":
                    m = re.match(r"\\(label|ref|cite[pt]?|input|bibliography|bibliographystyle|texttt|url|emph)\{", seg[j:])
                    if m:
                        # copy whole braced arg verbatim (filenames in texttt stay readable; underscores inside texttt arg still need escape in text mode!)
                        cmd = m.group(1)
                        if cmd in ("label", "ref", "cite", "citet", "citep", "input", "bibliography", "bibliographystyle"):
                            k = seg.index("}", j)
                            res.append(seg[j:k + 1])
                            j = k + 1
                            continue
                    res.append(ch)
                    j += 1
                    if j < len(seg):
                        res.append(seg[j])
                        j += 1
                    continue
                if ch == "_" :
                    # check previous char emitted
                    prev = res[-1] if res else ""
                    if prev == "\\":
                        res.append("_")
                    else:
                        res.append("\\_")
                        global fixed
                    j += 1
                    continue
                res.append(ch)
                j += 1
            return "".join(res)
        parts[i] = fix_seg(p).replace("\x00", "\\$")
    out.append("".join(parts))

open(P, "w", encoding="utf-8").write("\n".join(out))
print("done")
