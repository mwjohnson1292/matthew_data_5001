"""hive: the beehive inspection pipeline from Assignments 5 and 6, as a package.

A package is a folder of modules with an __init__.py file. Python runs this file
the first time anything in the package is imported, so it holds no code that does
work. It only documents what lives where.

Modules:
    data      RAW_INSPECTIONS, the starter records (Assignment 5)
    cleaning  parse_date, to_bool, normalize_record, clean_records (Assignment 5)
    grouping  hive_ids, records_for_hive: group by hive, order by date
              (shared by risk, summary and weights)
    risk      risk thresholds, calculate_risk, add_risk_fields
              (Assignment 6, Question 1)
    summary   summarize_hive and its helpers, plus the Hive class
              (Assignment 6, Questions 2 and 4)
    pipeline  run_pipeline: runs data -> cleaning -> risk in order (Assignment 7)
    weights   weight_changes: each hive's weight change between valid weighings
              (Assignment 7, Question 3)
"""
