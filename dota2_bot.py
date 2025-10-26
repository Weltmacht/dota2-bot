name = "Bleakill"
print(f"Hello World, {name}!")

grocery: list = ["bananas", "apples", "strawberries", "tampons", "bananas"]
print(grocery)

names: set = { "cory", "daniel", "david", "andrey", "martin", "cory" }

othernames: tuple = ("cory", "daniel", "david", "andrey", "martin", "cory")
othertuple: tuple = ("hotdogs")

people: dict = { "daniel": "faildozer", "cory": "welt", "andrey": "bleakill", "david": "morganfreeman", "test": 5 }
print(people["cory"])

i = 0

for name in names:
    print(i)
    if name := "cory":
        print("\tCory is here and he fucking rules bud!")
    i=i+1