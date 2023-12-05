CREATE TABLE "GPS_APP" (
	"appId"	TEXT NOT NULL,
	"title" TEXT NOT NULL,
	"developer" TEXT NOT NULL,
	"versison" TEXT NOT NULL,
  "icon"	TEXT NOT NULL,
  "headerImage"	TEXT NOT NULL,
	"score" NUMERIC NOT NULL,
	"realInstalls" NUMERIC NOT NULL,
  "released"	DATE NOT NULL,
	"exportPath"	TEXT,
	"exportDate"	DATE,
  "exportStatus"	BOOLEAN,
	PRIMARY KEY("appId")
);