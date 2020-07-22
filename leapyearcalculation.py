# Merve Turhan
# Leap Year Calculation

print("Please input a year")
input_year = int(input())


if input_year % 4 == 0:
    if input_year % 100 != 0 :
        if input_year % 400 == 0 :
            print("%d  is a leap year"%(input_year))
        else:
            print("%d is not a leap year" % (input_year))
    else:
        print("%d is not a leap year"%(input_year) )
else:
    print("%d is not a leap year" % (input_year))


