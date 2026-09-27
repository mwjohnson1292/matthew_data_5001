# Pseudocode
```
normalize_record(record):

    hive_id = strip and uppercase record hive_id
    if hive_id is not "H-" + 2 digits: reject

    date = record inspection_date
    if date matches YYYY-MM-DD or MM/DD/YYYY: convert to date
    else: reject
    if date is impossible: reject

    temp = record temp_f
    if temp is None: keep None
    else:
        remove a final "F", convert to float
        if temp < -20 or temp > 130: reject

    weight = try convert record weight_lb to float
    if conversion fails: weight = None
    if weight is negative: reject

    mites = convert record mites to int
    if mites < 0: reject

    queen = record queen_seen
    if queen is "yes": queen = True
    if queen is "no": queen = False
    if queen is not True or False: reject

    notes = record notes
    if notes is None: notes = ""

    return clean record
```

## Edge Cases
1 - dates can easily get messed up, right format, but wrong values
2 - i suppose a temperature given in C or K would need itsown formatting and conversion to F

## Rejection Prediction
I predict **5** records will be rejected. Skimming the data, a few values look clearly invalid (an impossible date, a negative count), and at least one more looks suspicious enough that it may fail a rule.