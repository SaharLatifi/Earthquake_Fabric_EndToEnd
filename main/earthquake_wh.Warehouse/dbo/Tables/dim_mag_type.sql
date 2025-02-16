CREATE TABLE [dbo].[dim_mag_type] (

	[mag_type_id] smallint NOT NULL, 
	[mag_type_desc] varchar(50) NOT NULL, 
	[created_at] datetime2(0) NOT NULL, 
	[last_updated_at] datetime2(0) NOT NULL
);


GO
ALTER TABLE [dbo].[dim_mag_type] ADD CONSTRAINT PK_dim_mag_type primary key NONCLUSTERED ([mag_type_id]);