-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- Link to schema: https://app.quickdatabasediagrams.com/#/d/m2mvF9
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.


CREATE TABLE "stock_price_data" (
    "Symbol" text,   NOT NULL,
    "Name" text   NOT NULL,
    "Date" text   NOT NULL,
    "Adj_close" int   NOT NULL,
    "Close" int   NOT NULL,
    "High" int   NOT NULL,
    "Low" int   NOT NULL,
    "Open" int   NOT NULL,
    "Volume" text   NOT NULL,
    CONSTRAINT "pk_stock_price_data" PRIMARY KEY (
        "Symbol"
     )
);

CREATE TABLE "stock_transcript_data" (
    "Title" text   NOT NULL,
    "URL" text   NOT NULL,
    "Date" text   NOT NULL,
    "Symbol" text   NOT NULL,
    CONSTRAINT "pk_stock_transcript_data" PRIMARY KEY (
        "Symbol"
     )
);

CREATE TABLE "stock_detail_data" (
    "Symbol" text   NOT NULL,
    "Name" text   NOT NULL,
    "GICS_Sector" text   NOT NULL,
    "GICS_SubIndustry" text   NOT NULL,
    "Headquarters_Location" text   NOT NULL,
    "Date_first_added" varchar   NOT NULL,
    "CIK" int   NOT NULL,
    "Founded" text   NOT NULL,
    CONSTRAINT "pk_stock_detail_data" PRIMARY KEY (
        "Symbol"
     )
);

ALTER TABLE "stock_price_data" ADD CONSTRAINT "fk_stock_price_data_Symbol" FOREIGN KEY("Symbol")
REFERENCES "stock_transcript_data" ("Symbol");

ALTER TABLE "stock_detail_data" ADD CONSTRAINT "fk_stock_detail_data_Symbol" FOREIGN KEY("Symbol")
REFERENCES "stock_transcript_data" ("Symbol");

