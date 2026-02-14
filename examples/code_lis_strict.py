def lengthOfLIS(nums):
    """
    Returns the length of the longest strictly increasing subsequence.
    Time Complexity: O(n log n)
    """
    if not nums:
        return 0
    tails = []
    for num in nums:
        import bisect
        idx = bisect.bisect_left(tails, num)
        if idx < len(tails):
            tails[idx] = num
        else:
            tails.append(num)
    return len(tails)
