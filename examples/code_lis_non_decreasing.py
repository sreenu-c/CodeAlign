def lengthOfLIS(nums):
    """
    Returns the length of the longest non-decreasing subsequence (variant).
    Note: This is technically different from strictly increasing, used to test 'partial' alignment.
    """
    if not nums:
        return 0
    tails = []
    for num in nums:
        import bisect
        # bisect_right for non-decreasing
        idx = bisect.bisect_right(tails, num)
        if idx < len(tails):
            tails[idx] = num
        else:
            tails.append(num)
    return len(tails)
