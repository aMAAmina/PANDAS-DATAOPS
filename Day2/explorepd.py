import pandas as pd

users = {
    "id":[12, 15, 95],
    "age":[15, 26, 48],
    "country":["Morocco","Algeria","Senegal"]
}

df = pd.DataFrame(users)

print(df)
