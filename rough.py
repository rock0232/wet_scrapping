import sys

lst = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

print(lst[:-6])

A = 10, 20, 30
print(id(A))

A = 1, 2, 3, 4
a, b, c, d = A
print(a, b, c, d)

a = 0o101
b = 2
c = a + b

a = "Hello world"
c = a

print(a is c)  # Returns true if the two variables are pointing to the same object
print(id(a))  # 64450416
print(id(c))  # 64450416

print(sys.version)

a = [1, 2, 3, 4, 5, 6, 7, 8]
print(str(a))

numbers = ','.join(str(i) for i in a)
print(numbers)

a = [100, 200, 300, 400, 500, 600, 700, 800]

print(a[3:])  # Prints the values from index 3 till the end [400, 500, 600, 700, 800]
print(a[3:6])  # Prints the values from index 3 to index 6. [400, 500, 600]
print(a[2::2])  # Prints the values from index 2 till the end of the list with step count 2. [300, 500, 700]

print(a[-2])
list = ["1", "4", "0", "6", "9"]
list = [int(i) for i in list]
list.sort()
print(list)
