# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 15:48:06 2017

@author: joseph.chen
"""
import random
from reel_strip import ReelStrip_MG_001A, ReelStrip_MG_001B, ReelStrip_FG_A, ReelStrip_FG_B, ReelStrip_FG_C
from lines import Lines
from odds import Odds
from symbols import Symbols
from settings import Rows, Weight_For_Mystery, Weight_For_MainGame, Weight_For_FreeGame
from settings import Num_Respin_In_Dog_Mode, Num_Scatter_To_Trigger_Free, Num_Free_Spins

def random_pick(some_list, probabilities):
    """
    Source:　https://www.safaribooksonline.com/library/view/python-cookbook-2nd/0596007973/ch04s22.html
    """
    x = random.uniform(0, 1)
    cumulative_probability = 0.0
    for item, item_probability in zip(some_list, probabilities):
        cumulative_probability += item_probability
        if x < cumulative_probability: break
    return item

class Slot(object):
    
    def __init__(self):
        self.main_game_reels = [ReelStrip_MG_001A, ReelStrip_MG_001B]
        self.free_game_reels = [ReelStrip_FG_A, ReelStrip_FG_B, ReelStrip_FG_C]
        self.window = [[0]*r for r in Rows]
        self.set_reel(self.main_game_reels, Weight_For_MainGame)
        self.N_reel = len(self.window)
        self.num_lines = len(Lines)
    
    def set_reel(self, reel_strips, weights):
        # The server randomly picks a reel according to their choice weights
        self.reel = random_pick(reel_strips, weights) 
        self.extended_reel = [r+r for r in self.reel]
    
    def spin(self):
        # If the MainGameA strip is chosen, then server will pick one randomly using this 
        # weight, and replace all mystery symbol with this symbol for this round only.
        symbol_replace_mystery = random_pick(list(range(len(Weight_For_Mystery))), 
                                             Weight_For_Mystery)        
        stop_index = [random.choice(range(len(rl))) for rl in self.reel]
        for n, win in enumerate(self.window):
            stop = stop_index[n]
            self.window[n] = self.extended_reel[n][stop:stop+len(win)]
            # Now we replace the `Mystery` symbol (if any) with the symbol we just picked.
            self.window[n] = [symbol_replace_mystery if x==Symbols.index("Mystery") else x for x in self.window[n]]           
            
    def check_results(self):
        # TODO: the trigger priority: dog_respin --> free game?      
        # check whether Dog Respin Mode was triggered
        if self.trigger_dog_respin():
            return "MG", 0.0, "MG_Dog_Respin", self.check_MG_Dog_Respin_payment()
        elif self.trigger_free_game():
            FG_payment, FG_Dog_Respin_payment = self.check_FG_payment()
            return "FG", FG_payment, "FG_Dog_Respin", FG_Dog_Respin_payment
        else:
            return "MG", self.check_MG_payment(), "MG_Dog_Respin", 0.0
        
    def check_MG_payment(self):
        return self._check_total_payment()
    
    def check_MG_Dog_Respin_payment(self):
        # Wild symbols can also be treated as Dog
        fixed_positions = self.get_fixed_symbols(["Dog", "Wild"], self.window)
        for n in range(Num_Respin_In_Dog_Mode):
            self.set_reel(self.main_game_reels, Weight_For_MainGame)
            self.spin()
            self.window = self.apply_fixed_symbols(fixed_positions, self.window)
            fixed_positions = self.get_fixed_symbols(["Dog", "Wild"], self.window)
        return self._check_total_payment()
                
    def check_FG_payment(self):
        num_free_spins = Num_Free_Spins
        FG_payment = 0
        FG_Dog_Respin_payment = 0
        while num_free_spins>0:
            self.set_reel(self.free_game_reels, Weight_For_FreeGame)
            self.spin()
            if self.trigger_dog_respin(mode="FG"):
                self.mirror_full_stack_symbols()
                FG_Dog_Respin_payment += self.check_FG_Dog_Respin_payment()
            elif self.trigger_free_game():
                num_free_spins += Num_Free_Spins
            else:
                FG_payment += self._check_total_payment(two_ways=True)
            num_free_spins -= 1
        return FG_payment, FG_Dog_Respin_payment
        
    def check_FG_Dog_Respin_payment(self):
        # Wild symbols can also be treated as Dog
        fixed_positions = self.get_fixed_symbols(["Dog", "Wild"], self.window)
        for n in range(Num_Respin_In_Dog_Mode):
            self.set_reel(self.free_game_reels, Weight_For_FreeGame)
            self.spin()
            self.window = self.apply_fixed_symbols(fixed_positions, self.window)
            fixed_positions = self.get_fixed_symbols(["Dog", "Wild"], self.window)
        return self._check_total_payment(two_ways=True)
    
    def mirror_full_stack_symbols(self):
        # TODO: Only mirror the first and last columns?
        if len(set(self.window[0]))==1 and self.window[0][0]==Symbols.index("Dog"):
            self.window[-1] = self.window[0]
        elif len(set(self.window[-1]))==1 and self.window[-1][0]==Symbols.index("Dog"):
            self.window[0] = self.window[-1]
    
    def _check_total_payment(self, two_ways=False):        
        total_payment = 0
        for n,line in enumerate(Lines):
            symbols_on_line = [self.window[m][line[m]] for m in range(len(line))]
            if two_ways:
                count, line_payment = self.check_two_ways_line_payment(symbols_on_line, Odds) 
            else:
                count, line_payment = self.check_line_payment(symbols_on_line, Odds)
            total_payment += line_payment
        return total_payment # in unit of per line bet
            
    def check_two_ways_line_payment(self, symbols_on_line, odds):
        count, payment = self.check_line_payment(symbols_on_line, odds)
        reversed_symbols_on_line = list(reversed(symbols_on_line))
        r_count, r_payment = self.check_line_payment(reversed_symbols_on_line, odds)
        if payment>=r_payment:
            return count, payment
        else:
            return r_count, r_payment
    
    def check_line_payment(self, symbols_on_line, odds):
        symbol = symbols_on_line[0]
        count = 1
        for n in range(1,len(symbols_on_line)):
            next_symbol = symbols_on_line[n]
            if symbol==next_symbol:
                count += 1
            elif (next_symbol==Symbols.index("Wild") and symbol!=Symbols.index("Scatter")):
                count += 1
            else:
                break
        payment = Odds[symbol][self.N_reel-count] 
        return count, payment
    
    def trigger_dog_respin(self, mode="MG"):
        # TODO: can Wild be count as Dog symbol in this case?
        if mode=="MG":
            return len(set(self.window[0]))==1 and self.window[0][0]==Symbols.index("Dog")
        elif mode=="FG":
            return ((len(set(self.window[-1]))==1 and self.window[-1][0]==Symbols.index("Dog")) or
                    (len(set(self.window[0]))==1 and self.window[0][0]==Symbols.index("Dog"))
            )
    
    def get_fixed_symbols(self, fixed_symbols, window):
        fixed_symbol_positions = []
        fixed_symbol_codes = [Symbols.index(fixed_symbol) for fixed_symbol in fixed_symbols]
        for n, col in enumerate(window):
            for m, sym in enumerate(col):
                if sym in fixed_symbol_codes:
                    fixed_symbol_positions.append((n,m,sym))
        return fixed_symbol_positions
            
    def apply_fixed_symbols(self, fixed_symbol_positions, window):
        for (n,m,sym) in fixed_symbol_positions:
            window[n][m] = sym
        return window
    
    def trigger_free_game(self):
        scatter_code = Symbols.index("Scatter")
        num_scatter = (self.window[1].count(scatter_code) +
                       self.window[2].count(scatter_code) +
                       self.window[3].count(scatter_code)
        )
        return num_scatter>=Num_Scatter_To_Trigger_Free
    
# temporally use    
def check_payment(symbols_on_line, odds):
    symbol = symbols_on_line[0]
    count = 1
    for n in range(1,len(symbols_on_line)):
        next_symbol = symbols_on_line[n]
        if symbol==next_symbol:
            count += 1
        elif (next_symbol==Symbols.index("Wild") and symbol!=Symbols.index("Scatter")):
            count += 1
        else:
            break
    payment = Odds[symbol][5-count] 
    return count, payment

def check_results(window):
    total_payment = 0
    for n,line in enumerate(Lines):
        symbols_on_line = [window[m][line[m]] for m in range(len(line))]
        count, line_payment = check_payment(symbols_on_line, Odds)
        #print("{}. {} {} {} {}".format(n,line, symbols_on_line, count, line_payment))
        if line_payment>0:
            print(symbols_on_line, line, count, line_payment)
        total_payment += line_payment
    return total_payment # in unit of per line bet