"""SQL Server data-access layer for the Media Optimization Engine."""
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
import pandas as pd

SERVER = r"LAPTOP-HSERDTUR\SQLEXPRESS"
DATABASE = "MediaOptimizationDB"


def get_engine():
    cs = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        f"SERVER={SERVER};DATABASE={DATABASE};"
        "Trusted_Connection=yes;TrustServerCertificate=yes;"
    )
    return create_engine(URL.create("mssql+pyodbc", query={"odbc_connect": cs}), pool_pre_ping=True)


def test_connection():
    with get_engine().connect() as conn:
        return conn.execute(text("SELECT DB_NAME();")).scalar()


def load_markets():
    return pd.read_sql("""SELECT MarketID,MarketName,Country,Population,PotentialImpressions,
        PriorityScore,MinimumBudget,MaximumBudget FROM dbo.Markets
        WHERE IsActive=1 ORDER BY PriorityScore DESC;""", get_engine())


def load_media_inventory():
    return pd.read_sql("""SELECT InventoryID,MarketID,Channel,Publisher,AvailableImpressions,
        CPM,ExpectedCTR,MinimumPurchase FROM dbo.MediaInventory
        WHERE IsActive=1 ORDER BY MarketID,CPM;""", get_engine())


def load_active_campaign():
    return pd.read_sql("""SELECT TOP 1 CampaignID,CampaignName,TotalBudget,Objective,
        MinimumMarkets,MaximumMarkets,StartDate,EndDate FROM dbo.Campaigns
        WHERE IsActive=1 ORDER BY CampaignID DESC;""", get_engine())


def load_channel_constraints():
    return pd.read_sql("""SELECT ConstraintID,Channel,MinBudgetPercent,MaxBudgetPercent
        FROM dbo.ChannelConstraints WHERE IsActive=1 ORDER BY ConstraintID;""", get_engine())


def save_optimization_run(campaign_id, tier1_budget, tier2_spend, impressions, status):
    q = text("""INSERT dbo.OptimizationRuns
        (CampaignID,Tier1AllocatedBudget,Tier2ActualSpend,TotalImpressions,SolverStatus)
        OUTPUT INSERTED.RunID VALUES(:c,:b,:s,:i,:st);""")
    with get_engine().begin() as conn:
        return conn.execute(q, {"c": int(campaign_id), "b": float(tier1_budget),
            "s": float(tier2_spend), "i": int(impressions), "st": str(status)}).scalar()


def save_market_results(run_id, df):
    x = df.copy(); x["RunID"] = run_id
    x[["RunID","MarketID","MarketName","MarketBudget","TotalSpend","RemainingBudget",
       "TotalImpressions","SolverStatus"]].to_sql("OptimizationMarketResults", get_engine(),
       schema="dbo", if_exists="append", index=False)


def save_media_results(run_id, df):
    x = df.copy(); x["RunID"] = run_id
    x[["RunID","MarketID","InventoryID","MarketName","Channel","Publisher",
       "PurchasedImpressions","Spend","Used"]].to_sql("OptimizationMediaResults", get_engine(),
       schema="dbo", if_exists="append", index=False)


def load_run_history(limit=25):
    """Load saved optimization runs. Returns an empty frame before result tables exist."""
    try:
        q = text("""SELECT TOP (:n) r.RunID,r.RunDate,c.CampaignName,r.Tier1AllocatedBudget,
            r.Tier2ActualSpend,r.TotalImpressions,r.SolverStatus
            FROM dbo.OptimizationRuns r
            LEFT JOIN dbo.Campaigns c ON c.CampaignID=r.CampaignID
            ORDER BY r.RunID DESC;""")
        return pd.read_sql(q, get_engine(), params={"n": int(limit)})
    except Exception:
        return pd.DataFrame()


if __name__ == "__main__":
    print("Connected to:", test_connection())
    print("\nMarkets\n", load_markets().to_string(index=False))
    print("\nInventory\n", load_media_inventory().to_string(index=False))
    print("\nCampaign\n", load_active_campaign().to_string(index=False))
    print("\nConstraints\n", load_channel_constraints().to_string(index=False))
