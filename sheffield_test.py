from sheffield import compare
import unittest
import random

class TestSheffield(unittest.TestCase):
    def pathbuilder(self,m,n):
        v = 0
        t = 0
        path = []
        for i in range(m+n):
            r = randint(0,1)
            if(r==0):
                path.append(chr(v+97))
                v+=1
            else:
                path.append(chr(t+65))
                t+=1
            if(v==m or v==26):
                while t<n:
                    path.append(chr(t+65))
                    t+=1
                break
            elif(t==n or t==26):
                while v<m:
                    path.append(chr(v+97))
                    v+=1
                break
        return path

    def test_compare(self,p1,p2):
        pass
        
