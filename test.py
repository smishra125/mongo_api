class Employee:
    def __init__(self, name, age, salary):
        self.name = name
        self.age = age
        self.salary = salary

    def show(self):
        print("name is",self.name, ", age is",self.age, "with salary", self.salary)

    def hike(self):
        a = int(input("Enter the hike percent you want in the salary "))
        self.salary = self.salary + self.salary * a/100
        print(self.salary)


e1 = Employee("Sam", 36, 60000)
e2 = Employee("Gary", 28, 45000)

print("For Sam salary is")
e1.show()

print("Foe Gary salary is")
e2.show()

e1.hike()
e2.hike()
