def qsort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]
        less = [x for x in arr[1:] if x < pivot]
        greater = [x for x in arr[1:] if x >= pivot]
        return qsort(less) + [pivot] + qsort(greater)

if __name__ == '__main__':
    a =qsort([2,1,43,7])
    print(a)