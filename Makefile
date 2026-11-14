# --- acceptance_backfill (EVAL_ACCEPTANCE_STANDARD.md P4) ---
# 证据来源: scripts/check_tmlr_compliance.py
# 命令逐字取自该来源，未增删任何参数。
.PHONY: eval

eval:
	python3 scripts/check_tmlr_compliance.py --selftest
