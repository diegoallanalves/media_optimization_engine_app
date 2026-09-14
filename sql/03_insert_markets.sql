/* Step 3: Sample market data. Run once on an empty Markets table. */
USE MediaOptimizationDB;
GO
INSERT INTO dbo.Markets (MarketName,Country,Population,PotentialImpressions,PriorityScore,MinimumBudget,MaximumBudget,IsActive)
VALUES
('São Paulo','Brazil',12300000,18500000,92.50,10000,50000,1),
('Rio de Janeiro','Brazil',6700000,11200000,86.20,8000,40000,1),
('Belo Horizonte','Brazil',2500000,6200000,78.40,5000,28000,1),
('Brasília','Brazil',3100000,7100000,82.10,6000,32000,1),
('Salvador','Brazil',2900000,5800000,74.80,4500,24000,1),
('Curitiba','Brazil',1900000,4900000,76.50,4500,25000,1),
('Recife','Brazil',1650000,4200000,71.30,4000,22000,1),
('Porto Alegre','Brazil',1500000,3900000,69.90,4000,21000,1);
GO
SELECT * FROM dbo.Markets ORDER BY PriorityScore DESC;
