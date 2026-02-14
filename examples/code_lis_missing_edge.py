
def lengthOfLIS(nums):
    # Missing empty check
    tails = []
    for num in nums:
        if not tails or num > tails[-1]:
            tails.append(num)
        else:
            # Simple replacement strategy (not fully correct for all cases or just different logic)
            for i in range(len(tails)):
                if tails[i] >= num:
                    tails[i] = num
                    break
    return len(tails)
