"""
Object to calculate entropy
"""

import pandas as pd
import numpy as np
import math
import threading

import multiprocessing as mp

class wordleEntropy:
    def __init__(self) -> None:
        """
        Object that can calculate the entropy of each Wordle guess given the
        remaining valid words.
        wordsLeft -> DataFrame
        """
        self.genPossibleCombinations()

    def genPossibleCombinations(self):
        """
        Creates matrix detailing each possible combination of outcomes,
        will be used as a set of instructions for calc entropy 
        """
        self.comMatrix = pd.DataFrame(columns=[0,1,2,3,4])
        colors = ['grey', 'green', 'yellow']

        for i in colors:
            for j in colors:
                for k in colors:
                    for l in colors:
                        for m in colors:
                            tempList = [i, j, k, l, m]
                            self.comMatrix.loc[len(self.comMatrix.index)] = tempList

    def parallelEntropy(self, wordsLeft, numProcess=11):
        try:
            mp.set_start_method('fork')
        except RuntimeError as e:
            pass
            
        self.df = wordsLeft
        self.df["E"] = np.nan
        self.dfLength = len(self.df)
        
        if len(wordsLeft) <= numProcess:
            numProcess = len(wordsLeft)
            
        # Multi-process approach
        chunk_size = math.floor(len(wordsLeft) / numProcess)
        manager = mp.Manager()
        results = manager.list()
        pool = mp.Pool(processes=numProcess)
        
        # Map the chunks to different processes
        chunk_args = []
        for i, chunk_df in enumerate(np.array_split(self.df, numProcess)):
            start = i * chunk_size
            end = start + chunk_size if i < numProcess - 1 else len(wordsLeft)
            chunk_args.append((chunk_df, start, end, results))
            
        pool.starmap(self.calcEntropy, chunk_args)
        pool.close()
        pool.join()

        # Append the calculated entropy results to self.df
        for index, E in results:
            self.df.at[index, 'E'] = E
                
    def calcEntropy(self, thread_df, indexStart, indexEnd, results=None):
        print("Process starting, with start/end: %s/%s" % (indexStart, indexEnd))
        
        for index, row in thread_df.iterrows():
            E = 0 # entropy sum
            p = 0
            
            for idx, possibility in self.comMatrix.iterrows():
                temp = self.df.copy()
                
                for lt in range(0,5):
                    if len(temp) != 0:
                        if possibility[lt] == 'grey':
                            # grey means that the letter does not exist in the soln
                            temp = temp[~temp['0'].isin([row[str(lt)]])]
                            temp = temp[~temp['1'].isin([row[str(lt)]])]
                            temp = temp[~temp['2'].isin([row[str(lt)]])]
                            temp = temp[~temp['3'].isin([row[str(lt)]])]
                            temp = temp[~temp['4'].isin([row[str(lt)]])]
                            
                        elif possibility[lt] == 'green':
                            # that means that the letter is in the right column
                            temp = temp[temp[str(lt)].isin([row[str(lt)]])]
                            
                        elif possibility[lt] == 'yellow':
                            columns_to_check = []
                            temp = temp[~temp[str(lt)].isin([row[str(lt)]])]
                            
                            for ii in range(0,5):
                                if ii != lt:
                                    columns_to_check.append(str(ii))
                                    
                            filtered_rows = []
                            for _, row_temp in temp[columns_to_check].iterrows():
                                letter_found = False
                                for cell_value in row_temp:
                                    if cell_value == row[str(lt)]:
                                        letter_found = True
                                        break
                                filtered_rows.append(letter_found)
                            
                            temp = temp[filtered_rows]
                
                p = len(temp) / self.dfLength
                if p > 0:
                    E = E + (p * math.log2(1 / p))
            
            # If results list is provided, append the calculated entropy to the results list
            if results is not None:
                results.append((index, E))
            else:
                # If no results list provided, directly update self.df with the calculated entropy
                self.df.at[index, 'E'] = E 