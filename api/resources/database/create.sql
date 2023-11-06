CREATE TABLE "GPS_TABLE" (
	"appId"	TEXT NOT NULL,
	"appLogo"	TEXT NOT NULL,
  "appBackground"	TEXT NOT NULL,
	"exportPath"	TEXT,
	"exportDate"	DATE,
  "exporting"	BOOLEAN,
	PRIMARY KEY("appId")
);