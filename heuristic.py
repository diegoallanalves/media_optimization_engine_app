import pandas as pd
from database import load_markets,load_active_campaign

def _norm(s):
    lo,hi=float(s.min()),float(s.max())
    return pd.Series(1.0,index=s.index) if hi==lo else (s-lo)/(hi-lo)

def _allocate(df,budget):
    df=df.copy(); df["AllocatedBudget"]=df.MinimumBudget.astype(float)
    while budget-df.AllocatedBudget.sum()>0.005:
        remaining=budget-df.AllocatedBudget.sum()
        cap=df.MaximumBudget-df.AllocatedBudget
        ok=cap>0.005
        if not ok.any(): break
        w=df.loc[ok,"HeuristicScore"].clip(lower=.000001); w=w/w.sum()
        add=pd.concat([remaining*w,cap[ok]],axis=1).min(axis=1)
        df.loc[ok,"AllocatedBudget"]+=add
    df["AllocatedBudget"]=df.AllocatedBudget.round(2)
    diff=round(budget-df.AllocatedBudget.sum(),2)
    if diff:
        for i in df.sort_values("HeuristicScore",ascending=False).index:
            v=df.at[i,"AllocatedBudget"]+diff
            if df.at[i,"MinimumBudget"]<=v<=df.at[i,"MaximumBudget"]:
                df.at[i,"AllocatedBudget"]=round(v,2); break
    df["BudgetSharePct"]=(df.AllocatedBudget/budget*100).round(2)
    return df

def run_heuristic(markets=None,campaign=None):
    m=load_markets() if markets is None else markets.copy()
    cdf=load_active_campaign() if campaign is None else campaign
    c=cdf.iloc[0]
    m["NormalizedPriority"]=_norm(m.PriorityScore)
    m["NormalizedImpressions"]=_norm(m.PotentialImpressions)
    m["HeuristicScore"]=.6*m.NormalizedPriority+.4*m.NormalizedImpressions
    ranked=m.sort_values(["HeuristicScore","PriorityScore"],ascending=False).reset_index(drop=True)
    selected=ranked.head(int(c.MaximumMarkets)).copy()
    while len(selected)>=int(c.MinimumMarkets) and selected.MinimumBudget.sum()>float(c.TotalBudget):
        selected=selected.iloc[:-1].copy()
    if len(selected)<int(c.MinimumMarkets):
        raise ValueError("Budget cannot satisfy MinimumMarkets.")
    return ranked,_allocate(selected,float(c.TotalBudget))

if __name__=="__main__":
    r,s=run_heuristic()
    print("TIER 1 - HEURISTIC")
    print(r[["MarketName","PriorityScore","PotentialImpressions","HeuristicScore"]].to_string(index=False))
    print("\nSELECTED\n",s[["MarketName","MinimumBudget","MaximumBudget","AllocatedBudget","BudgetSharePct"]].to_string(index=False))
    print("\nTotal:",s.AllocatedBudget.sum())
