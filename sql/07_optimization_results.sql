USE MediaOptimizationDB;
GO
-- Run ONLY this file on your existing database.
-- It adds persistence tables without deleting your existing Markets/Inventory/Campaign data.
IF OBJECT_ID('dbo.OptimizationRuns') IS NULL
CREATE TABLE dbo.OptimizationRuns(
 RunID INT IDENTITY(1,1) PRIMARY KEY,
 CampaignID INT NOT NULL REFERENCES dbo.Campaigns(CampaignID),
 RunDate DATETIME2 NOT NULL DEFAULT SYSDATETIME(),
 Tier1AllocatedBudget DECIMAL(18,2),Tier2ActualSpend DECIMAL(18,2),
 TotalImpressions BIGINT,SolverStatus NVARCHAR(50));
GO
IF OBJECT_ID('dbo.OptimizationMarketResults') IS NULL
CREATE TABLE dbo.OptimizationMarketResults(
 ResultID INT IDENTITY(1,1) PRIMARY KEY,
 RunID INT NOT NULL REFERENCES dbo.OptimizationRuns(RunID),
 MarketID INT NOT NULL,MarketName NVARCHAR(100),MarketBudget DECIMAL(18,2),
 TotalSpend DECIMAL(18,2),RemainingBudget DECIMAL(18,2),
 TotalImpressions BIGINT,SolverStatus NVARCHAR(50));
GO
IF OBJECT_ID('dbo.OptimizationMediaResults') IS NULL
CREATE TABLE dbo.OptimizationMediaResults(
 ResultID INT IDENTITY(1,1) PRIMARY KEY,
 RunID INT NOT NULL REFERENCES dbo.OptimizationRuns(RunID),
 MarketID INT NOT NULL,InventoryID INT NOT NULL,MarketName NVARCHAR(100),
 Channel NVARCHAR(50),Publisher NVARCHAR(100),PurchasedImpressions BIGINT,
 Spend DECIMAL(18,2),Used BIT);
GO
