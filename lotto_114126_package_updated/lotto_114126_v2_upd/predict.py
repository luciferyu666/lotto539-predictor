    """
    predict.py
    Load trained artifacts and output human‑readable report.
    """

    import json, sys, textwrap

    def main(path):
        with open(path) as f:
            data=json.load(f)
        pool=data['core_pool']
        combos=data['combo']
        rep=textwrap.dedent(f"""
            核心號碼池 (K={len(pool)}):
            {', '.join(f'{n:02d}' for n in pool)}

            ── 排輪組合 ──
        """)
        for i,(combo,risk) in enumerate(combos,1):
            rep+=f"{i:2d}. {' '.join(f'{n:02d}' for n in combo)} [{risk}]
"
        print(rep)

    if __name__=='__main__':
        main(sys.argv[1])
