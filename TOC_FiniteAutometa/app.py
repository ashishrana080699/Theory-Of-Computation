#import required packages
from flask import *
import json
import os
import pandas as pd
from pandas.io.json import json_normalize
import numpy as np

app = Flask(__name__)
NO_OF_CHARS = 256
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/run',methods=["post"])
def run():
    formvalues = request.form
    path1 = "static/json/"
    with open(os.path.join(os.getcwd()+"/"+path1,'file.json'), 'w') as f:
        json.dump(formvalues, f)
    with open(os.path.join(os.getcwd()+"/"+path1,'file.json'), 'r') as f:
        values = json.load(f)
        txt=values["text"]
        pat=values["pattern"]
    #text_box_value = request.form['text']
    #pattern_box_value = request.form['pattern']
     
    return render_template("index.html", txt_disp=txt, pat_disp=pat, ans=search(pat, txt), **request.args)

def search(pat, txt): 
    ''' 
    Prints all occurrences of pat in txt 
    '''
    global NO_OF_CHARS 
    M = len(pat) 
    N = len(txt) 
    TF = computeTF(pat, M)     
  
    # Process txt over FA. 
    state=0
    result=[]
    for i in range(N): 
       
        state = TF[state][ord(txt[i])] 
        if state == M: 
            result.append(format(i-M+1)) 
    return result       

def computeTF(pat, M): 
    ''' 
    This function builds the TF table which  
    represents Finite Automata for a given pattern 
    '''
    global NO_OF_CHARS 
  
    TF = [[0 for i in range(NO_OF_CHARS)]
          for _ in range(M+1)] 
  
    for state in range(M+1): 
        for x in range(NO_OF_CHARS): 
            z = getNextState(pat, M, state, x) 
            TF[state][x] = z 
  
    return TF 

def getNextState(pat, M, state, x): 
    ''' 
    calculate the next state  
    '''
  
    # If the character c is same as next character  
      # in pattern, then simply increment state 
  
    if state < M and x == ord(pat[state]): 
        return state+1
  
    i=0
    # ns stores the result which is next state 
  
    # ns finally contains the longest prefix  
     # which is also suffix in "pat[0..state-1]c" 
  
     # Start from the largest possible value and  
      # stop when you find a prefix which is also suffix 
    for ns in range(state,0,-1): 
        if ord(pat[ns-1]) == x: 
            while(i<ns-1): 
                if pat[i] != pat[state-ns+1+i]: 
                    break
                i+=1
            if i == ns-1: 
                return ns  
    return 0

    


if __name__ == '__main__':
    app.run()