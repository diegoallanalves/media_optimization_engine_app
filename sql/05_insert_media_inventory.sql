/* Step 5: Sample inventory. Run once on an empty MediaInventory table. */
USE MediaOptimizationDB;
GO
INSERT INTO dbo.MediaInventory (MarketID,Channel,Publisher,AvailableImpressions,CPM,ExpectedCTR,MinimumPurchase,IsActive)
VALUES
(1,'Display','Google',5000000,8.50,0.0120,100000,1),(1,'Social','Meta',4200000,7.20,0.0150,100000,1),(1,'Video','YouTube',3000000,11.00,0.0180,50000,1),
(2,'Display','Google',3500000,8.10,0.0110,100000,1),(2,'Social','Meta',3000000,7.00,0.0140,100000,1),(2,'Video','YouTube',2200000,10.50,0.0170,50000,1),
(3,'Display','Google',2000000,7.40,0.0100,50000,1),(3,'Social','Meta',1800000,6.80,0.0130,50000,1),(3,'Video','YouTube',1200000,9.80,0.0160,50000,1),
(4,'Display','Google',2300000,7.80,0.0110,50000,1),(4,'Social','Meta',2100000,7.10,0.0145,50000,1),(4,'Video','YouTube',1500000,10.20,0.0175,50000,1),
(5,'Display','Google',1900000,6.90,0.0100,50000,1),(5,'Social','Meta',1700000,6.30,0.0130,50000,1),(5,'Video','YouTube',1100000,9.20,0.0150,50000,1),
(6,'Display','Google',1800000,7.30,0.0105,50000,1),(6,'Social','Meta',1600000,6.70,0.0135,50000,1),(6,'Video','YouTube',1000000,9.60,0.0160,50000,1),
(7,'Display','Google',1500000,6.70,0.0095,50000,1),(7,'Social','Meta',1400000,6.10,0.0125,50000,1),(7,'Video','YouTube',900000,8.90,0.0145,50000,1),
(8,'Display','Google',1400000,7.00,0.0100,50000,1),(8,'Social','Meta',1300000,6.50,0.0130,50000,1),(8,'Video','YouTube',850000,9.30,0.0155,50000,1);
GO
SELECT m.MarketName,i.Channel,i.Publisher,i.AvailableImpressions,i.CPM,i.ExpectedCTR,i.MinimumPurchase
FROM dbo.MediaInventory i INNER JOIN dbo.Markets m ON i.MarketID=m.MarketID
ORDER BY m.PriorityScore DESC,i.CPM;
