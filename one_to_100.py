#count from 1 to 100
# if %5 print world
# if %3 print hello
# if both hello world


#initialize number range
NUMBERS=list(range(1,100))

# for i in NUMBERS:
#     if i%15: #%15
#         print("Hello World!")
#     elif i%3==0:
#         print("hello")
#     elif i%5==0: 
#         print("world")
#     else:
#         print(i)

# count to 100 and parse each num
def count_to_100(num_list): 
    for i in num_list:
        print(parse_num(i))

#check multiple
def parse_num(a):
        if a%15==0: 
            return "Hello World!"
        elif a%3==0:
            return "hello"
        elif a%5==0: 
            return "world"
        else:
            return a


if __name__=='__main__':
    print("Some test cases")
    assert parse_num(1)==1
    assert parse_num(3)=="hello"
    assert parse_num(5)=="world"
    assert parse_num(125)=="world" #out of NUMBERS range
    assert parse_num(99)=="hello"
    assert parse_num(98)==98
    # count_to_100(NUMBERS)