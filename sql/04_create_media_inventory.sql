/* Step 4: Media inventory. MarketID is a foreign key to Markets. */
USE MediaOptimizationDB;
GO
IF OBJECT_ID('dbo.MediaInventory','U') IS NULL
CREATE TABLE dbo.MediaInventory (
    InventoryID INT IDENTITY(1,1) PRIMARY KEY,
    MarketID INT NOT NULL,
    Channel VARCHAR(50) NOT NULL,
    Publisher VARCHAR(100) NOT NULL,
    AvailableImpressions BIGINT NOT NULL,
    CPM DECIMAL(10,2) NOT NULL, -- cost per 1,000 impressions
    ExpectedCTR DECIMAL(6,4),
    MinimumPurchase INT DEFAULT 0,
    IsActive BIT DEFAULT 1,
    CONSTRAINT FK_MediaInventory_Markets FOREIGN KEY (MarketID) REFERENCES dbo.Markets(MarketID)
);
GO
