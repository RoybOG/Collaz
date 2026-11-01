
def binStrFunc(func):
    def wrapper(*args, **kwargs):
        altArgs = list(args)
        
        altArgs[0] = int(args[0],0) if type(altArgs[0]) is str else args[0]
        result = func(*altArgs, **kwargs)
        if result is not None:
            print(toBitStr(result))
        return result
    return wrapper




toBitStr = lambda b: format(b, 'b')

reduce2s = lambda n: int(toBitStr(n).rstrip('0'),2)

@binStrFunc
def nextNum(n):

    return reduce2s(n) if n%2==0 else 3 * n + 1


@binStrFunc
def prevNum(n):
    if n % 3 == 0: 
        return n

    n = n * (4 if n % 3 == 1 else 2) # multiplying by the power of 2 thats mod 3 multplicitive inverse of n to get reminder 1
    
    return (n-1) // 3


@binStrFunc
def collatzPath(n):
    
    maxNum = n
    i = 1
    print(toBitStr(n))
    while n > 5:
        n = nextNum(n)
        maxNum = max(n,maxNum)
        i = i + 1

    print(f"length: {i}, max: {toBitStr(maxNum)}")

