CREATE TABLE [dbo].[fact_earthquake] (

	[earthquake_id] varchar(100) NOT NULL, 
	[title] varchar(100) NOT NULL, 
	[place_description] varchar(100) NOT NULL, 
	[sig] int NOT NULL, 
	[mag] float NOT NULL, 
	[mag_type_id] smallint NOT NULL, 
	[sig_class_id] smallint NOT NULL, 
	[country_id] smallint NOT NULL, 
	[earthquake_datetime] datetime2(0) NOT NULL, 
	[earthquake_date] date NOT NULL, 
	[created_at] datetime2(0) NOT NULL, 
	[last_updated_at] datetime2(0) NOT NULL
);


GO
ALTER TABLE [dbo].[fact_earthquake] ADD CONSTRAINT PK_fact_earthquake primary key NONCLUSTERED ([earthquake_id]);
GO
ALTER TABLE [dbo].[fact_earthquake] ADD CONSTRAINT UQ_3f4c2b96_007a_4448_af09_6897f4c08d85 unique NONCLUSTERED ([country_id]);
GO
ALTER TABLE [dbo].[fact_earthquake] ADD CONSTRAINT FK_165c35b0_ccba_4bff_ae24_0da4104138cb FOREIGN KEY ([earthquake_date]) REFERENCES [dbo].[dim_date]([Date]);
GO
ALTER TABLE [dbo].[fact_earthquake] ADD CONSTRAINT FK_2021867e_311c_4194_9e79_b7b70394492b FOREIGN KEY ([sig_class_id]) REFERENCES [dbo].[dim_sig_class]([sig_class_id]);
GO
ALTER TABLE [dbo].[fact_earthquake] ADD CONSTRAINT FK_3873b7ff_6476_4923_bfd4_3d1cab2223e7 FOREIGN KEY ([mag_type_id]) REFERENCES [dbo].[dim_mag_type]([mag_type_id]);