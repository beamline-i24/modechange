#!/bin/usr/python
import pv
import sys
from ca import caput, caget 
import setup_beamline as sup

def get_mode():
    current_mode = 'Unknown'
    ttabx = caget(pv.ttab_x + '.RBV')
    ptaby = caget(pv.ptab_y + '.RBV')
    cstrmt = caget(pv.cstrm_trans + '.RBV')
    fluoutlim = caget(pv.fluo_out_limit)
    print 'ptaby', ptaby, ptaby<-89
    print 'fluoutlim', fluoutlim, fluoutlim=='ON' 
    print 'cstrmt', cstrmt, cstrmt<-279
    print 'ttabx', ttabx, ttabx<3.0 
    print 'ptaby', ptaby, ptaby>-2
    if ptaby < -89 and fluoutlim == 'ON' and cstrmt < -220:
        current_mode = 'Tray'
    elif ttabx < 3.0 and ptaby > -2:
        current_mode = 'Pin'
    return current_mode

def requestor(req_mode, action):
    print 80*'-'
    print 'Requested mode:', req_mode
    print 'Requested action:', action
    print 'Getting Current mode'
    current_mode = get_mode()
    print 'Current Mode', current_mode
    if action == 'switch':
        print 10*'switch'
        if req_mode == 'Pin':
            if current_mode == 'Tray':
                sup.modechange('Tray_switch2pin')
            else:
                print 'In Pin Mode, doing nothing'
        elif req_mode == 'Tray':
            if current_mode == 'Pin':
                sup.modechange('Pin_switch2tray')
            else:
                print 'In Tray Mode, doing nothing'
        else:
            print 'Unknown Requested Mode (req_mode)'
    elif req_mode == current_mode:
        print 10*'move'
        sup.modechange(current_mode + '_' + action)
    else:
        print 'Unknown Requested Position (action)'
    print 80*'-'
    
if __name__ == '__main__':
    requestor(sys.argv[1], sys.argv[2])
