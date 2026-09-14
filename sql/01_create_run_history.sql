USE MediaOptimizationDB;
GO
IF OBJECT_ID('dbo.OptimizationRuns','U') IS NULL
BEGIN
 CREATE TABLE dbo.OptimizationRuns(
   RunID INT IDENTITY(1,1) PRIMARY KEY,
   RunDate DATETIME2 NOT NULL DEFAULT SYSDATETIME(),
   CampaignID INT NOT NULL,
   Tier1AllocatedBudget DECIMAL(18,2) NOT NULL,
   Tier2ActualSpend DECIMAL(18,2) NOT NULL,
   TotalImpressions BIGINT NOT NULL,
   SolverStatus NVARCHAR(50) NOT NULL
 );
END;
GO
