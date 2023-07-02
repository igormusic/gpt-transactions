USE master;
GO

-- Check if the database exists
IF NOT EXISTS (SELECT 1 FROM sys.databases WHERE name = 'accounts')
BEGIN
    -- Create the database
    CREATE DATABASE accounts;
END
GO