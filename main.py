# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 14:16:53 2017

@author: joseph.chen
"""

from slot import Slot
from settings import Num_Sim, Bet, Weight_For_MainGame, Weight_For_FreeGame

def main():
    print("This program is used to verify model SB50")
    total_placement = 0
    total_payment = 0
    total_MG_payment = 0
    total_MG_Dog_Respin_payment = 0
    total_FG_payment = 0
    total_FG_Dog_Respin_payment = 0
    
    slot = Slot()
    for n in range(Num_Sim):
        slot.set_reel(slot.main_game_reels, Weight_For_MainGame)
        slot.spin()
        #print(slot.window)
        game_type1, payment1, game_type2, payment2 = slot.check_results()
        payment = payment1 + payment2
        total_placement += Bet
        total_payment += payment*(Bet/slot.num_lines)
        if game_type1=="MG" and game_type2=="MG_Dog_Respin":
            total_MG_payment += payment1*(Bet/slot.num_lines)
            total_MG_Dog_Respin_payment += payment2*(Bet/slot.num_lines)
        elif game_type1=="FG" and game_type2=="FG_Dog_Respin":
            total_FG_payment += payment1*(Bet/slot.num_lines)
            total_FG_Dog_Respin_payment += payment2*(Bet/slot.num_lines)
        else:
            print("Error!")
        
    print("Total placement: {:.2f}".format(total_placement))
    print("Total payment: {:.2f}+{:.2f}+{:.2f}+{:.2f} = {:.2f}".format(total_MG_payment,
                                                   total_MG_Dog_Respin_payment,
                                                   total_FG_payment,
                                                   total_FG_Dog_Respin_payment,
                                                   total_payment))
    print("Total RTP: {:.4f}".format(total_payment*1.0/total_placement))
    print("Total MG RTP: {:.4f}".format(total_MG_payment*1.0/total_placement))
    print("Total MG Dog Respin RTP: {:.4f}".format(total_MG_Dog_Respin_payment*1.0/total_placement))
    print("Total FG RTP: {:.4f}".format(total_FG_payment*1.0/total_placement))
    print("Total FG Dog Respin RTP: {:.4f}".format(total_FG_Dog_Respin_payment*1.0/total_placement))
    
    
if __name__=="__main__":
    main()