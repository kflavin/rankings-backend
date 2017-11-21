from datetime import date, timedelta


start = date(2017, 9, 2)
end = date(2017, 12, 2)
delta = timedelta(days=7)

saturdays = []

curr = start
while curr != end:
    saturdays.append(curr)
    curr += delta

print(saturdays)
print(len(saturdays))
