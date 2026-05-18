# EWDB R01 Word Data Type Recheck

日期：2026-05-16

## Summary

- Word tables: 75
- R01 SQL tables: 75
- Word only tables: None
- R01 only tables: None
- Field mismatch tables: 0
- Data type mismatches after regeneration: 0

## Data Type Rule

Data types are parsed from the semicolon-separated field description in Word. Recognized markers include `AUTO_INCREMENT`, `varchar(n)`, `int`, `float`, `double`, `DATE`, `datetime`, `timestamp`, and `longtext`. Fields that describe enum-like values using `數值如下` are interpreted as `INT`.

## Field Difference

No field differences detected between Word and R01.

## Data Type Difference

No data type differences detected after regeneration.
