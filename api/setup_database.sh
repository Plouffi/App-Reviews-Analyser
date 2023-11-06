#!/bin/sh

sqlite3 ./api/resources/database/ara.db <<'END_SQL'
echo "$(<./api/resources/database/create.db)"
END_SQL