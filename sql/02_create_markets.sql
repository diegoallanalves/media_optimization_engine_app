/* Step 2: Markets and market-level business limits. */
USE MediaOptimizationDB;
GO
IF OBJECT_ID('dbo.Markets','U') IS NULL
CREATE TABLE dbo.Markets (
    MarketID INT IDENTITY(1,1) PRIMARY KEY,
    MarketName VARCHAR(100) NOT NULL,
    Country VARCHAR(100) NOT NULL,
    Population INT,
    PotentialImpressions BIGINT,
    PriorityScore DECIMAL(5,2),
    MinimumBudget DECIMAL(12,2),
    MaximumBudget DECIMAL(12,2),
    IsActive BIT DEFAULT 1
);
GO
