USE MediaOptimizationDB;
DECLARE @RunID INT=(SELECT MAX(RunID) FROM dbo.OptimizationRuns);
SELECT * FROM dbo.OptimizationRuns WHERE RunID=@RunID;
SELECT * FROM dbo.OptimizationMarketResults WHERE RunID=@RunID ORDER BY TotalImpressions DESC;
SELECT MarketName,Channel,SUM(Spend) Spend,SUM(PurchasedImpressions) Impressions
FROM dbo.OptimizationMediaResults WHERE RunID=@RunID
GROUP BY MarketName,Channel ORDER BY MarketName,Channel;
