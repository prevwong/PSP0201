def CalculateLevel(correct, level = 1):
    correct -= (5 + 2*level)
    if correct <= 0:
        return level
    else:
        return CalculateLevel(correct, level+1)

print CalculateLevel(2000)
