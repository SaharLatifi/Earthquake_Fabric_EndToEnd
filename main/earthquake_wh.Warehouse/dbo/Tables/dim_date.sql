CREATE TABLE [dbo].[dim_date] (

	[DateNum] bigint NULL, 
	[Date] date NULL, 
	[YearMonthNum] bigint NULL, 
	[Calendar_Quarter] varchar(8000) NULL, 
	[MonthNum] bigint NULL, 
	[MonthName] varchar(8000) NULL, 
	[MonthShortName] varchar(8000) NULL, 
	[WeekNum] bigint NULL, 
	[DayNumOfYear] bigint NULL, 
	[DayNumOfMonth] bigint NULL, 
	[DayNumOfWeek] bigint NULL, 
	[DayName] varchar(8000) NULL, 
	[DayShortName] varchar(8000) NULL, 
	[Quarter] bigint NULL, 
	[YearQuarterNum] bigint NULL, 
	[DayNumOfQuarter] bigint NULL, 
	[NorthernHemispherSeason] varchar(8000) NULL, 
	[SouthernHemispherSeason] varchar(8000) NULL
);


GO
ALTER TABLE [dbo].[dim_date] ADD CONSTRAINT UQ_cef0026e_0fd6_4aec_92fd_01a85071300f unique NONCLUSTERED ([Date]);