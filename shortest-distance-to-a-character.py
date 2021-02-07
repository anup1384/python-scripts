#Given a string s and a character c that occurs in s, return an array of integers answer where answer.length == s.length and answer[i] is the shortest distance from s[i] to the character c in s

def shortestToChar(s, c):
    import math
    ans = []
    for i in range(len(s)):
        if s[i] == c:
            ans.append(i)
    res = []
    for j in range(len(s)):
        temp = math.inf
        for x in ans:
            temp = min(temp, abs(j-x))
        res.append(temp)
    print(res)

#         ans = []
#         for i in range(len(s)):
#             if s[i] == c:
#                 ans.append(i)
#         res = []
#         for j in range(len(s)):
#             res.append(min(abs(j-x) for x in ans))
            
#         return res




s = "loveleetcode"
c = "e"
shortestToChar(s, c)
