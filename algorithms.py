
class Sorter:
    def __init__(self):
        pass

    @staticmethod
    def binary_search(ar, target):
        left = 0
        right = len(ar) - 1
        while left <= right:
            mid = (left + right) // 2
            if ar[mid] == target:
                return mid
            elif ar[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1
    
    @staticmethod
    def merge(left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result += left[i:]
        result += right[j:]
        return result

    @staticmethod
    def merge_sort(ar):
        if len(ar) <= 1:
            return ar
        mid = len(ar) // 2
        left = Sorter.merge_sort(ar[:mid])
        right = Sorter.merge_sort(ar[mid:])
        return Sorter.merge(left, right)