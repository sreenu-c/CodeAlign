def lengthOfLIS(nums):
    # Edge Case: Strictly Decreasing
    # Input: [5, 4, 3, 2, 1]
    # Expected Output: 1 (Any single element is an LIS of length 1)
    if not nums:
        return 0
    
    # This naive logic might fail if not careful, 
    # but let's see how the AI evaluates it.
    # Correct O(n^2) approach for demo:
    dp = [1] * len(nums)
    for i in range(len(nums)):
        for j in range(i):
            if nums[i] > nums[j]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)
