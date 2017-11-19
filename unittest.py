# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 14:34:06 2017

@author: joseph.chen
"""
import unittest

from reel_strip import ReelStrip_MG_001A, ReelStrip_MG_001B, ReelStrip_FG_A, ReelStrip_FG_B, ReelStrip_FG_C
from lines import Lines

class WangTheDogTest(unittest.TestCase):
    
    def test_reel_strip(self):
        reel_lengths = [len(r) for r in ReelStrip_MG_001A]
        self.assertEqual(reel_lengths, [47,56,55,57,51])
        reel_lengths = [len(r) for r in ReelStrip_MG_001B]
        self.assertEqual(reel_lengths, [36,44,42,43,38])
        reel_lengths = [len(r) for r in ReelStrip_FG_A]
        self.assertEqual(reel_lengths, [47,60,60,62,51])
        reel_lengths = [len(r) for r in ReelStrip_FG_B]
        self.assertEqual(reel_lengths, [36,45,43,44,39])
        reel_lengths = [len(r) for r in ReelStrip_FG_C]
        self.assertEqual(reel_lengths, [38,43,42,44,39])
        
    def test_lines(self):
        self.assertEqual(Lines[0], [0,0,0,0,0])
        self.assertEqual(Lines[1], [0,1,1,1,0])
        self.assertEqual(Lines[2], [1,1,1,1,1])
        self.assertEqual(Lines[3], [1,2,2,2,1])
        self.assertEqual(Lines[4], [2,2,2,2,2])
        
        self.assertEqual(Lines[5], [2,3,3,3,2])
        self.assertEqual(Lines[6], [0,0,1,0,0])
        self.assertEqual(Lines[7], [0,1,0,1,0])
        self.assertEqual(Lines[8], [1,1,2,1,1])
        self.assertEqual(Lines[9], [1,2,1,2,1])
        
        self.assertEqual(Lines[10], [2,2,3,2,2])
        self.assertEqual(Lines[11], [2,3,2,3,2])
        self.assertEqual(Lines[12], [0,0,0,1,0])
        self.assertEqual(Lines[13], [0,1,1,0,0])
        self.assertEqual(Lines[14], [1,1,1,2,1])
        
        self.assertEqual(Lines[15], [1,2,2,1,1])
        self.assertEqual(Lines[16], [2,2,2,3,2])
        self.assertEqual(Lines[17], [2,3,3,2,2])
        self.assertEqual(Lines[18], [0,0,1,1,0])
        self.assertEqual(Lines[19], [0,1,0,0,0])
        
        self.assertEqual(Lines[20], [1,0,2,2,1])
        self.assertEqual(Lines[21], [1,2,1,1,1])
        self.assertEqual(Lines[22], [2,2,3,3,2])
        self.assertEqual(Lines[23], [2,3,2,2,2])
        self.assertEqual(Lines[24], [0,1,2,1,0])
        
        self.assertEqual(Lines[25], [1,2,3,2,1])
        self.assertEqual(Lines[26], [1,1,0,1,1])
        self.assertEqual(Lines[27], [2,2,1,2,2])
        self.assertEqual(Lines[28], [0,1,2,2,1])
        self.assertEqual(Lines[29], [1,2,3,3,2])
        
        self.assertEqual(Lines[30], [1,1,0,0,0])
        self.assertEqual(Lines[31], [2,2,1,1,1])
        self.assertEqual(Lines[32], [0,2,1,2,1])
        self.assertEqual(Lines[33], [1,3,2,3,2])
        self.assertEqual(Lines[34], [1,0,1,0,0])
        
        self.assertEqual(Lines[35], [2,1,2,1,1])
        self.assertEqual(Lines[36], [2,1,0,1,2])
        self.assertEqual(Lines[37], [0,2,3,2,0])
        self.assertEqual(Lines[38], [1,0,0,0,1])
        self.assertEqual(Lines[39], [1,3,3,3,1])
        
if __name__=="__main__":
    print("Unittest of SB50")
    unittest.main()