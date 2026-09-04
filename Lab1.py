# print("====================")
# print("Welcome")
# print("1st Post")
# print("====================")


# username = "cool_creator"
# bio = "Fun Blogger"
# followers = 100

# print("Username: " + str(username))
# print("Bio: " + str(bio))
# print("Followers: " + str(followers))

# followers += 50
# print("Day 1:", followers)

# followers += 20
# print("Day 2:", followers)

# followers -= 10
# print("Day 3:", followers)

username = input("Enter Username: ")
age = int(input("Enter Age: "))
category = input("Enter Content Category: ")


print("Instagram Profile: ")
print("=====================")
print("Username: ", username)
print("Age: ", age)
print("Category: ", category)

if age>40 and category == "fun":
    print("You are too old what is fun for you??")
    