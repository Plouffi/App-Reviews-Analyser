CREATE TABLE "GPS_TABLE" (
	"appId"	TEXT NOT NULL,
	"title" TEXT NOT NULL,
	"developer" TEXT NOT NULL,
	"versison" TEXT NOT NULL,
	"appLogo"	TEXT NOT NULL,
  "appBackground"	TEXT NOT NULL,
	"score" NUMERIC NOT NULL,
	"reviews" NUMERIC NOT NULL,
  "released"	DATE NOT NULL,
	"exportPath"	TEXT,
	"exportDate"	DATE,
  "exporting"	BOOLEAN,
	PRIMARY KEY("appId")
);