def hello(to="world"):
    print("hello", to)

def main():
    # Ask user for his/her name
    name=input ("What is your name? ")

    first, last=name.split(" ")

    # First letter capitalized
    first=first.capitalize()

    # Say hello to user
    hello()
    print ("hello", first+", how are you?")

    """
    Multiline 
    comment
    """

main()