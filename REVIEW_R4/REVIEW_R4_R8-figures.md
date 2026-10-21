# REVIEW_R4_R8-figures.md — R4 Round 1（主审执行；R8降级方案，见R19 MISSION D1）

降级说明：deepseek-eyes不在本会话skill目录、无describe_image脚本，R8按documented degradation执行——机械半为scan_figure_claims.py（reports/figures.md：figure labels 1/ref 1/includegraphics缺失0），语义半由主审逐格核验Table 1十五行＋TikZ十五对（tex表非PDF渲染，此替代实际更严）。

## 机械半
- scan_figure_claims.py exit 0：fig:acc定义＋引用各1；includegraphics 0缺失；orphan 0。

## 语义半（Table 1十五行 vs results/账本；TikZ十五对 vs Acc列）
- n加总：30+30+60+60+30+160+40+60+60+20+78+157+157+60+60=1062 ✓
- Pilot/Holdout/Cloud-new/Local-new/Local-en/Local-big/Math/XDt/XDl/PPi/PHo/PCN/PLN/R18/HGe十五行Acc/ECE/flips/b/c与C09/C10/C15/C22/C24/C25/C30/C37/C40/C49/C54及ece_unified.json一致 ✓（hetero 21/60=0.35、29/60=0.4833、0.5143/0.381；R18 15/60=0.25、39/60=0.65）
- TikZ十五对与Acc exact/guarded列逐对一致 ✓（HGe 0.35/0.4833末对）
- caption注记：R18 adjudicated 24（raw 27）✓；hetero adjudicated 8（raw 11）✓；R19-E7追加hetero ECE混口径注后caption与文件housing一致 ✓

## Issues
- 无（C0/M0/m0/n0）。R4-R1-01类指针问题属文字层，已由E6/E7/E7b/E14关闭，本角色复验caption新措辞与文件一致。
- verdict: acceptable。
