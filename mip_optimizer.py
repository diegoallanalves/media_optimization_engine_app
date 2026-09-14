import pandas as pd
import pulp
from database import load_media_inventory,load_channel_constraints
from heuristic import run_heuristic
UNIT=1000

def optimize_market(market,inventory,constraints):
    mid=int(market.MarketID); name=str(market.MarketName); budget=float(market.AllocatedBudget)
    inv=inventory[inventory.MarketID==mid].copy()
    model=pulp.LpProblem(f"MediaOptimization_{mid}",pulp.LpMaximize)
    x={}; y={}
    for _,r in inv.iterrows():
        iid=int(r.InventoryID)
        mx=int(float(r.AvailableImpressions)//UNIT)
        mn=int((float(r.MinimumPurchase)+UNIT-1)//UNIT)
        x[iid]=pulp.LpVariable(f"x_{iid}",0,mx,cat="Integer")
        y[iid]=pulp.LpVariable(f"y_{iid}",cat="Binary")
        model += x[iid] <= mx*y[iid]
        model += x[iid] >= mn*y[iid]
    spend=pulp.lpSum(x[int(r.InventoryID)]*float(r.CPM) for _,r in inv.iterrows())
    model += pulp.lpSum(x.values())
    model += spend <= budget
    for _,rule in constraints.iterrows():
        rows=inv[inv.Channel==rule.Channel]
        if rows.empty: continue
        cs=pulp.lpSum(x[int(r.InventoryID)]*float(r.CPM) for _,r in rows.iterrows())
        model += cs >= budget*float(rule.MinBudgetPercent)
        model += cs <= budget*float(rule.MaxBudgetPercent)
    model.solve(pulp.PULP_CBC_CMD(msg=False))
    status=pulp.LpStatus[model.status]
    out=[]
    for _,r in inv.iterrows():
        iid=int(r.InventoryID); units=int(round(pulp.value(x[iid]) or 0))
        imp=units*UNIT; cost=units*float(r.CPM)
        out.append({"MarketID":mid,"InventoryID":iid,"MarketName":name,"Channel":r.Channel,
        "Publisher":r.Publisher,"CPM":float(r.CPM),"AvailableImpressions":int(r.AvailableImpressions),
        "MinimumPurchase":int(r.MinimumPurchase),"PurchasedImpressions":imp,
        "Spend":round(cost,2),"Used":imp>0})
    d=pd.DataFrame(out); total=float(d.Spend.sum())
    return {"MarketID":mid,"MarketName":name,"MarketBudget":budget,"TotalSpend":round(total,2),
    "RemainingBudget":round(budget-total,2),"TotalImpressions":int(d.PurchasedImpressions.sum()),
    "SolverStatus":status},d

def run_mip(selected=None):
    if selected is None: _,selected=run_heuristic()
    inv=load_media_inventory(); rules=load_channel_constraints(); sums=[]; frames=[]
    for m in selected.itertuples(index=False):
        s,d=optimize_market(m,inv,rules); sums.append(s); frames.append(d)
    return pd.DataFrame(sums),pd.concat(frames,ignore_index=True)

def validate_channel_shares(summary,details,constraints=None):
    rules=load_channel_constraints() if constraints is None else constraints
    out=[]
    for m in summary.itertuples(index=False):
        md=details[details.MarketID==m.MarketID]
        for r in rules.itertuples(index=False):
            s=float(md.loc[md.Channel==r.Channel,"Spend"].sum())
            share=s/m.MarketBudget if m.MarketBudget else 0
            out.append({"MarketName":m.MarketName,"Channel":r.Channel,"Spend":round(s,2),
            "BudgetSharePct":round(share*100,2),"RequiredMinPct":float(r.MinBudgetPercent)*100,
            "RequiredMaxPct":float(r.MaxBudgetPercent)*100,
            "Valid":float(r.MinBudgetPercent)-1e-9<=share<=float(r.MaxBudgetPercent)+1e-9})
    return pd.DataFrame(out)

if __name__=="__main__":
    _,sel=run_heuristic(); s,d=run_mip(sel); v=validate_channel_shares(s,d)
    print("TIER 2 - MIP\n",s.to_string(index=False))
    print("\nALLOCATIONS\n",d.to_string(index=False))
    print("\nCONSTRAINT VALIDATION\n",v.to_string(index=False))
    print("\nSpend:",s.TotalSpend.sum()," Impressions:",s.TotalImpressions.sum())
    print("All optimal:",(s.SolverStatus=="Optimal").all())
    print("All rules valid:",v.Valid.all())
