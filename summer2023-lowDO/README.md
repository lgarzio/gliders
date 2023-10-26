Collection of plotting and analysis tools for the low DO/pH event off the NJ coast in the summer of 2023

Glider datasets:
- ru28-20230906T1601 - DO sensor
- ru39-20230817T1520 - pH sensor
- ru40-20230817T1522 - DO sensor

Notes:
- ru39 had some bad gps fixes so I removed all latitude and longitude values between dt.datetime(2023, 8, 31, 8, 0) and dt.datetime(2023, 8, 31, 13, 0) and reinterpolated latitude and longitude only (not profile_lat or profile_lon)