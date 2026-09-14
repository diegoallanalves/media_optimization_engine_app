from database import *
from heuristic import run_heuristic
from mip_optimizer import run_mip,validate_channel_shares

def run_full_optimization(save_to_database=False):
    campaign=load_active_campaign()
    ranking,tier1=run_heuristic(campaign=campaign)
    summary,details=run_mip(tier1)
    validation=validate_channel_shares(summary,details)
    run_id=None
    if save_to_database:
        c=campaign.iloc[0]
        run_id=save_optimization_run(c.CampaignID,tier1.AllocatedBudget.sum(),
          summary.TotalSpend.sum(),summary.TotalImpressions.sum(),
          "Optimal" if (summary.SolverStatus=="Optimal").all() else "Review")
        save_market_results(run_id,summary); save_media_results(run_id,details)
    return {"campaign":campaign,"ranking":ranking,"tier1":tier1,
      "tier2_summary":summary,"tier2_details":details,"validation":validation,"run_id":run_id}

if __name__=="__main__":
    r=run_full_optimization(True)
    print("Complete. SQL RunID:",r["run_id"])
