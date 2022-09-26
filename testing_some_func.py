from datetime import datetime, timezone

t1 = datetime.now()
for _ in range(1000):
    for _ in range(1000):
        pass

t2 = datetime.now()
t3 = datetime.now()
print(t3.strftime("%Y-%m-%d %H:%M:%S")[11:13])


