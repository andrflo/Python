def main():
    x=input("What is x? ")
    print("x squared is", square(float(x)))
    y=input("What is y? ")

    z=round(float(x)/float(y), 2)

    print(f"{z:,}")

def square(n):
    return n*n

main()



