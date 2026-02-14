def lengthOfLIS(nums):
    # Edge Case: All Duplicates
    # Input: [7, 7, 7, 7]
    # Expected Output: 1 (Strictly increasing means 7 !< 7)
    
    if not nums:
        return 0
        
    tails = []
    for num in nums:
        import bisect
        # bisect_left handles duplicates by inserting to the left
        # rewriting the existing value, which maintains 'strictly' increasing property logic
        idx = bisect.bisect_left(tails, num)
        if idx < len(tails):
            tails[idx] = num
        else:
            tails.append(num)
    return len(tails)
