-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- Link to schema: https://app.quickdatabasediagrams.com/#/d/m2mvF9
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.


SET XACT_ABORT ON

BEGIN TRANSACTION QUICKDBD

CREATE TABLE [stock_price_data] (
    [stock_price_id] int  NOT NULL ,
    [stock_id] int  NOT NULL ,
    [Symbol] text  NOT NULL ,
    [Name] text  NOT NULL ,
    [Date] text  NOT NULL ,
    [Adj_close] int  NOT NULL ,
    [Close] int  NOT NULL ,
    [High] int  NOT NULL ,
    [Low] int  NOT NULL ,
    [Open] int  NOT NULL ,
    [Volume] text  NOT NULL ,
    CONSTRAINT [PK_stock_price_data] PRIMARY KEY CLUSTERED (
        [stock_price_id] ASC
    )
)

CREATE TABLE [stock_transcript_data] (
    [stock_trans_id] int  NOT NULL ,
    [stock_id] int  NOT NULL ,
    [Title] text  NOT NULL ,
    [URL] text  NOT NULL ,
    [Date] text  NOT NULL ,
    [Symbol] text  NOT NULL ,
    CONSTRAINT [PK_stock_transcript_data] PRIMARY KEY CLUSTERED (
        [stock_trans_id] ASC
    )
)

CREATE TABLE [stock_detail_data] (
    [stock_id] int  NOT NULL ,
    [Symbol] text  NOT NULL ,
    [Name] text  NOT NULL ,
    [GICS_Sector] text  NOT NULL ,
    [GICS_SubIndustry] text  NOT NULL ,
    [Headquarters_Location] text  NOT NULL ,
    [Date_first_added] varchar  NOT NULL ,
    [CIK] int  NOT NULL ,
    [Founded] text  NOT NULL ,
    CONSTRAINT [PK_stock_detail_data] PRIMARY KEY CLUSTERED (
        [stock_id] ASC
    )
)

ALTER TABLE [stock_price_data] WITH CHECK ADD CONSTRAINT [FK_stock_price_data_stock_id] FOREIGN KEY([stock_id])
REFERENCES [stock_detail_data] ([stock_id])

ALTER TABLE [stock_price_data] CHECK CONSTRAINT [FK_stock_price_data_stock_id]

ALTER TABLE [stock_transcript_data] WITH CHECK ADD CONSTRAINT [FK_stock_transcript_data_stock_id] FOREIGN KEY([stock_id])
REFERENCES [stock_detail_data] ([stock_id])

ALTER TABLE [stock_transcript_data] CHECK CONSTRAINT [FK_stock_transcript_data_stock_id]

COMMIT TRANSACTION QUICKDBD