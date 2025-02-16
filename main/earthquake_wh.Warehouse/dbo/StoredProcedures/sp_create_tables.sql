CREATE PROCEDURE sp_create_tables
AS

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name ='dim_mag_type' AND SCHEMA_NAME(schema_id) = 'dbo' )
    CREATE TABLE dbo.dim_mag_type (
        mag_type_id    SMALLINT NOT NULL ,
        mag_type_desc  VARCHAR(50) NOT NULL ,
        created_at      DATETIME2(0)  NOT NULL ,
        last_updated_at DATETIME2(0)  NOT NULL  
        
    )
ALTER TABLE dbo.dim_mag_type add CONSTRAINT PK_dim_mag_type PRIMARY KEY NONCLUSTERED (mag_type_id) NOT ENFORCED ;

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name ='dim_sig_class' AND SCHEMA_NAME(schema_id) = 'dbo' )
    CREATE TABLE dbo.dim_sig_class (
        sig_class_id    SMALLINT NOT NULL ,
        sig_class_desc  VARCHAR(50) NOT NULL ,
        created_at      DATETIME2(0)  NOT NULL ,
        last_updated_at DATETIME2(0)  NOT NULL  
        
    )
ALTER TABLE dbo.dim_sig_class add CONSTRAINT PK_dim_sig_class PRIMARY KEY NONCLUSTERED (sig_class_id) NOT ENFORCED ;


IF NOT EXISTS (SELECT * FROM sys.tables WHERE name ='fact_earthquake' AND SCHEMA_NAME(schema_id) = 'dbo' )
    CREATE TABLE dbo.fact_earthquake (
        earthquake_id           VARCHAR(100) NOT NULL ,
        title                   VARCHAR(100) NOT NULL ,
        place_description       VARCHAR(100) NOT NULL ,
        sig                     INT          NOT NULL ,
        mag                     FLOAT        NOT NULL ,
        mag_type_id             SMALLINT     NOT NULL ,
        sig_class_id            SMALLINT     NOT NULL ,
        country_id              SMALLINT     NOT NULL ,
        earthquake_datetime     DATETIME2(0)    NOT NULL , 
        earthquake_date         DATE            NOT NULL ,
        created_at              DATETIME2(0)    NOT NULL ,
        last_updated_at         DATETIME2(0)    NOT NULL  
        
    )
ALTER TABLE dbo.fact_earthquake add CONSTRAINT PK_fact_earthquake PRIMARY KEY NONCLUSTERED (earthquake_id) NOT ENFORCED ;