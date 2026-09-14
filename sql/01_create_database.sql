/* Step 1: Create the project database. */
USE master;
GO
IF DB_ID('MediaOptimizationDB') IS NULL
    CREATE DATABASE MediaOptimizationDB;
GO
USE MediaOptimizationDB;
GO
SELECT DB_NAME() AS CurrentDatabase, 'Database ready' AS Status;
