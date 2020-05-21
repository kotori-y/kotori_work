# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 16:46:49 2019

@Author: Zhi-Jiang Yang, Dong-Sheng Cao
@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com; oriental-cds@163.com
@Blog: https://blog.moyule.me

♥I love Princess Zelda forever♥
"""

import sys
import getopt
from roc import drawroc
from pr import drawpr
from logauc import draw_logauc
from enrich import Enrichment

def draw(argv):
    """
    """
    try:
        opts, args = getopt.getopt(argv, "ht:i:l:s:a:o:", ['help','type=','folder_path=','label_field=',
                                               'score_field=','ascending=','save_dir='])
#        print(opts)
    except:
        pass
    
    
    kwargs = {}
    
    
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('python draw.py --type <type of fig> --folder_path <folder_path>')
            sys.exit()
        
        elif opt in ('--type'):
            _type = arg
        
        elif opt in ('-i','--folder_path'):
            kwargs['folder_path'] = arg
#            print(arg)
            
        elif opt in ('--label_field'):
            kwargs['label_field'] = arg
            
        elif opt in ('--score_idx'):
            kwargs['score_field'] = arg
            
        elif opt in ('--ascending'):
            kwargs['ascending'] = arg
            
        elif opt in ('-o','--save_dir'):
            kwargs['savedir'] = arg
    
    if _type == 'roc':
        drawroc(**kwargs)
    elif _type == 'pr':
        drawpr(**kwargs)
    elif _type == 'logauc':
        draw_logauc(**kwargs)
    elif _type == 'enrich':
        en = Enrichment(**kwargs)
        en.show_enrichment_roc()
    
        
            
if __name__ == "__main__":
    draw(sys.argv[1:])