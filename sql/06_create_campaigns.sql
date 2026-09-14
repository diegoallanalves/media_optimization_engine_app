/* Step 6: Campaign-level constraints. SQL stores values; Python enforces them mathematically. */
USE MediaOptimizationDB;
GO
IF OBJECT_ID('dbo.Campaigns','U') IS NULL
CREATE TABLE dbo.Campaigns (
    CampaignID INT IDENTITY(1,1) PRIMARY KEY,
    CampaignName VARCHAR(150) NOT NULL,
    TotalBudget DECIMAL(12,2) NOT NULL,
    Objective VARCHAR(50) NOT NULL,
    MinimumMarkets INT NOT NULL,
    MaximumMarkets INT NOT NULL,
    StartDate DATE NOT NULL,
    EndDate DATE NOT NULL,
    IsActive BIT DEFAULT 1
);
GO
IF NOT EXISTS (SELECT 1 FROM dbo.Campaigns WHERE CampaignName='Brazil National Awareness Campaign')
INSERT INTO dbo.Campaigns (CampaignName,TotalBudget,Objective,MinimumMarkets,MaximumMarkets,StartDate,EndDate,IsActive)
VALUES ('Brazil National Awareness Campaign',100000.00,'Maximize Impressions',3,6,'2026-10-01','2026-10-31',1);
GO
SELECT * FROM dbo.Campaigns;
