/* Reusable checks before optimization. */
USE MediaOptimizationDB;
GO
SELECT 'Markets' AS TableName, COUNT(*) AS RowCount FROM dbo.Markets
UNION ALL SELECT 'MediaInventory', COUNT(*) FROM dbo.MediaInventory
UNION ALL SELECT 'Campaigns', COUNT(*) FROM dbo.Campaigns;

SELECT * FROM dbo.Markets WHERE MinimumBudget > MaximumBudget;
SELECT * FROM dbo.MediaInventory WHERE CPM <= 0 OR AvailableImpressions < 0 OR MinimumPurchase < 0;
SELECT * FROM dbo.Campaigns WHERE TotalBudget <= 0 OR MinimumMarkets > MaximumMarkets;
