COUNTER Harvester for Windows
=============================

STARTING THE PROGRAM
--------------------
1. Keep this whole folder together. Do not move COUNTER_Harvester.exe out
   of it - it needs the "_internal" folder that sits next to it.
2. Double-click COUNTER_Harvester.exe.
   Tip: right-click it > Show more options > Send to > Desktop (create shortcut).

The first time, Windows may show "Windows protected your PC".
Click "More info", then "Run anyway". This happens because the program is
not signed by a software company. It is the open-source C5.1 Harvester.
You do NOT need to install Python.


WHERE YOUR FILES ARE SAVED
--------------------------
Everything you create is saved in:

    Documents\COUNTER_Harvester_Data

    providers.tsv       your providers and their COUNTER API credentials
    current_config.py   your settings (change them with the Settings button)
    tsv_folders\        the downloaded reports
    json_folders\       the raw data received from each provider
    counterdata.db      the SQLite database
    infolog.txt         detailed log of the last run

To update to a newer version: delete this program folder and unzip the new
one. Your data in Documents\COUNTER_Harvester_Data is not touched.


IF YOU USED THE HARVESTER BEFORE
--------------------------------
Copy your old providers.tsv into Documents\COUNTER_Harvester_Data before
starting the program. (An older manual install keeps it in
Documents\COUNTER_Harvester\C5.1_Harvester\src\providers.tsv.)


IF IT DOES NOT START
--------------------
A message box will tell you. Send this file to the person who gave you
the program:

    Documents\COUNTER_Harvester_Data\startup_error.txt

Note: infolog.txt contains your API credentials, so be careful who you
share it with.

Documentation:
https://github.com/Melissa-Belvadi-Library-Projects/C5.1_Harvester/tree/main/docs
