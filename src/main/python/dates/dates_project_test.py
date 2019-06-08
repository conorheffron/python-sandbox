import dates_project as dp

print(dp.days_in_month(2019, 5))
print(dp.days_in_month(2005, 12))
print(dp.days_in_month(12, 12))

print(dp.is_valid_date(2019, 1, 11))
print(dp.is_valid_date(2019, 1, 32))
print(dp.is_valid_date(9998, 12, 31))

print(dp.days_between(1973, 8, 14, 1973, 8, 13))
print(dp.days_between(1, 1, 1, 1, 1, 1))

print(dp.days_in_month(2000, 1))
print(dp.days_in_month(2000, 12))
print(dp.is_valid_date(2000, 1, 1))
print(dp.is_valid_date(2000, 12, 31))
print(dp.days_between(2000, 1, 1, 2000, 12, 31))

print(dp.age_in_days(2019, 1, 1))
print(dp.age_in_days(1989, 3, 18))

print(dp.age_in_days(2016, 12, 31))

print(dp.age_in_days(1, 1, 1))
print(dp.age_in_days(0, 1, 21))
print(dp.age_in_days(2001, 2, 30))

