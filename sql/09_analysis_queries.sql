/* Helpful analytical queries for exploration and debugging. */
USE MediaOptimizationDB;
GO
SELECT m.MarketName, m.PriorityScore, SUM(i.AvailableImpressions) AS InventoryImpressions,
       AVG(i.CPM) AS AverageCPM
FROM dbo.Markets m JOIN dbo.MediaInventory i ON m.MarketID=i.MarketID
WHERE m.IsActive=1 AND i.IsActive=1
GROUP BY m.MarketName,m.PriorityScore
ORDER BY m.PriorityScore DESC;
