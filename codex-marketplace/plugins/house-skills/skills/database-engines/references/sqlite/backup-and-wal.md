# SQLite backup and WAL

Use this reference when backing up SQLite databases or configuring WAL.
SQLite's online backup API copies a live database without locking the source
for long periods.

The authority is the SQLite 3.53.3 Backup API and WAL documentation. Adapt the
backup and checkpoint guidance into step-by-step instructions. Do not reproduce
the C API signatures; describe the operations an application performs.
