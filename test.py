# Prompt the user to enter a number and store the input
# The input() function returns a string, so it needs to be converted to a number
try:
    num_str = input("Please enter a number: ")
    # Convert the string input to an integer
    # Use float() if you expect decimal numbers
    num_int = int(num_str)

    # Output the entered number
    print("You entered:", num_int)

except ValueError:
    # Handle cases where the input is not a valid number
    print("Invalid input. Please enter a valid number.")
