CREATE TABLE [dbo].[dim_sig_class] (

	[sig_class_id] smallint NOT NULL, 
	[sig_class_desc] varchar(50) NOT NULL, 
	[created_at] datetime2(0) NOT NULL, 
	[last_updated_at] datetime2(0) NOT NULL
);


GO
ALTER TABLE [dbo].[dim_sig_class] ADD CONSTRAINT PK_dim_sig_class primary key NONCLUSTERED ([sig_class_id]);