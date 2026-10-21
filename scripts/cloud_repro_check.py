"""Cloud byte-reproducibility check (goal-R5 cloud migration).

Compares sha256 of the 14 recomputed result files between the local sealed
tree and the cloud rerun outputs observed via SSH (hashes below were observed
from `sha256sum` on seetacloud-h3 on 2026-09-07; re-observe to re-verify).
Writes results/cloud_repro.json. Exit nonzero on any mismatch.
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]

# Observed cloud hashes (seetacloud-h3, RTX 3090, python 3.10+scipy), 2026-09-07.
CLOUD = {
    "analysis.json": "6028d376494013197aac4a4f7e8482f0aefd7257e1b67b684f6a55a810e8c2fb",
    "cloud_new.json": "9de15d30b58459db095489b648409d64c9b5f3e1b0bac3c10fa1491ad18db0e5",
    "analysis_120.json": "d2846258c403ce09147124cffc23c216b1f65d2526178f9b6552ea5550c80d38",
    "local_new.json": "ade6e55fa0af14724766ef20965f9227f7a4a593c2697e21e5b3742b97381253",
    "analysis_180.json": "ae3ce79f67580553e776930e316b3a54cf525e1b56c99e7fc0213d9b1a3858eb",
    "guard_v31.json": "3c829f88a94713ed525b5a061745d044efd42c5a75deaf93e63c02b2f87fe7f3",
    "tempscale.json": "34f4fbcff541bc7423b80902bfd6a45f078a69cc7e6dcf0e09ce745ea611e626",
    "isotonic.json": "51332961c64181ed4c3a12fff1268f91d0c2cfb735852b193b2ee9f9530465ca",
    "ablation.json": "32650b123617d5dd452d6189ede5ce55b65e6e6a05f42213325287e72aec7860",
    "flips.json": "3c82079127b110f26774048a6f49c6927d2ff290813ec6090526f9667af53908",
    "flips_new60.json": "f85c988f30667b028dc46e26253a01f270788e237fb89c57d63660cc7e6296af",
    "flips_local60.json": "7fe91d70b3a0132bc25843d03c6deabd63b7201933443d5180c0f3f6df5104d1",
    "power_update_120.json": "1211edfa73217db14d8d31bb03e0a515aa2a80bbaae1695fbf17a8eef8e135d6",
    "power_local60.json": "5906ab48068037a9854f007b148c3c1c24fec388516c646ad636d181f89fe76f",
}


def main() -> int:
    rows = []
    for name, ch in CLOUD.items():
        p = HERE / "results" / name
        lh = hashlib.sha256(p.read_bytes()).hexdigest()
        ok = lh == ch
        rows.append({"file": f"results/{name}", "identical": ok})
        print(f"{'OK ' if ok else 'DIFF'} {name}")
    n_ok = sum(1 for r in rows if r["identical"])
    out = {"host": "seetacloud-h3 (RTX 3090)", "n_files": len(rows),
           "n_identical": n_ok, "files": [r["file"] for r in rows if r["identical"]]}
    (HERE / "results" / "cloud_repro.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"identical {n_ok}/{len(rows)}")
    return 0 if n_ok == len(rows) else 1


if __name__ == "__main__":
    sys.exit(main())
