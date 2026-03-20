x = 2

def make_subtractor(n): #M
    return lambda x:x-n

sub3 = make_subtractor(3)
print(sub3(5))  # Output: 7