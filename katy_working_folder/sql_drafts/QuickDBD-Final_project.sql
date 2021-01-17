-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- Link to schema: https://app.quickdatabasediagrams.com/#/d/m2mvF9
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.


SET XACT_ABORT ON

BEGIN TRANSACTION QUICKDBD

CREATE TABLE [stock_data] (
    [Symbol] string,  NOT NULL ,
    [Name] string  NOT NULL ,
    [Date] date  NOT NULL ,
    [Adj_close] int  NOT NULL ,
    [Close] int  NOT NULL ,
    [High] int  NOT NULL ,
    [Low] int  NOT NULL ,
    [Open] int  NOT NULL ,
    [Volume] int  NOT NULL ,
    CONSTRAINT [PK_stock_data] PRIMARY KEY CLUSTERED (
        [Symbol] ASC
    )
)

CREATE TABLE [stock_transcript_data] (
    [Symbol] string  NOT NULL ,
    [Name] string  NOT NULL ,
    [Date] date  NOT NULL ,
    [Transcript] string  NOT NULL ,
    CONSTRAINT [PK_stock_transcript_data] PRIMARY KEY CLUSTERED (
        [Symbol] ASC
    )
)

ALTER TABLE [stock_data] WITH CHECK ADD CONSTRAINT [FK_stock_data_Symbol] FOREIGN KEY([Symbol])
REFERENCES [stock_transcript_data] ([Symbol])

ALTER TABLE [stock_data] CHECK CONSTRAINT [FK_stock_data_Symbol]

COMMIT TRANSACTION QUICKDBD