def lengthOfLongestSubstring(s: str) -> int:
    """
    Naïve O(n^2) or O(n^3) approach to check all substrings.
    Used to test 'constraint' alignment (time complexity).
    """
    n = len(s)
    res = 0
    for i in range(n):
        seen = set()
        for j in range(i, n):
            if s[j] in seen:
                break
            seen.add(s[j])
            res = max(res, j - i + 1)
    return res
