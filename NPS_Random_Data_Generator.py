import numpy as np
import pandas as pd


# Params    
years = 5
n= 100
attribute_count = 4

def GenerateDataSet(n, years):
    
    df = {} # Create empty data frame
    
    df=pd.DataFrame(np.zeros([0,0])) # Zero matrix
    
    #Create empty structure with client name and LTR
    for i in range(n * years):
        df = df.append({'Client Name': np.nan, 'Likelihood to recommend': np.nan},ignore_index=True)
    return df     


def GenerateAttributes(d, n):

    df = d
    
    for i in range(n):
        df["Attribute" + str(i + 1)] = np.nan
    return df         
    
def CreateClients(d, shape , n):
    
    df = d
    count = 0 
    for i in range(shape):
        if(count < n):
            df.loc[i,"Client Name"] = "Client " + str(count)
            count += 1
            print(count)
        else:
            df.loc[i,"Client Name"] = "Client " + str(count)
            count = 0
            
    return df    
    
def GenerateYearColumn(d, n, years):
    
    df = d
    year = 2017
    count = 0
    
    for i in range(n * years):
        
        if (count < n):
            df.loc[i,"Year"] = str(year)
            count += 1
        else:
            df.loc[i,"Year"] = str(year)
            count = 0
            year = year - 1
    return df
    
def GenerateLHTR(d, prom_pct, det_pct):
 
    if((prom_pct + det_pct) > 1): raise ValueError, "error"
    else:
        promoters, passive, detractors = np.split(d.sample(frac=1), [  int(prom_pct*len(d)), int(det_pct*len(d))])
        
        colname = d.columns[1]
        
        promoter_df = d.loc[promoters.index,colname]
        passive_df = d.loc[passive.index,colname]
        detractors_df = d.loc[detractors.index,colname]
        
        d.loc[promoters.index,colname] = np.random.choice(np.arange(9, 11), len(promoter_df))
        d.loc[passive.index,colname] = np.random.choice(np.arange(7,8), len(passive_df))
        d.loc[detractors.index,colname] = np.random.choice(np.arange(0,6), len(detractors_df))

    return(d)
    
def GenerateAttributeScore(d,attribute_count):

    for j in range(d.shape[1]):

        promoter_scores_proba = [0.02, 0.02, 0.02, 0.02, 0.02, 0.05, .05, .1, .3, .4]
        passive_scores_proba= [0.02, 0.02, 0.02, 0.02, 0.02, 0.1, .1, .3, .2, .2]
        detractor_scores_proba = [.05, .05, .05, .10, .30, 0.2, 0.1, 0.05, 0.09, 0.01]
        
        possible_scores = [1,2,3,4,5,6,7,8,9,10]
        
        detractor_scores = possible_scores
        passive_scores = possible_scores 
        promoter_scores = possible_scores
        
        colname = d.columns[j]
        LHTR = d.columns[1]
        
        promoter_dataset = (d[LHTR] > 8)
        passive_dataset = (d[LHTR] <9 ) & (d[LHTR] > 5 )
        detractor_dataset = (d[LHTR] <=5 )

        if(j > 2 & j < (2 + attribute_count)):
            d.loc[promoter_dataset, colname] = np.random.choice(promoter_scores, d.loc[d[LHTR] > 8, colname].shape[0], p=promoter_scores_proba)
            d.loc[passive_dataset, colname] = np.random.choice(passive_scores, d.loc[passive_dataset, colname].shape[0], p=passive_scores_proba)
            d.loc[detractor_dataset, colname] = np.random.choice(passive_scores, d.loc[detractor_dataset, colname].shape[0], p=passive_scores_proba)
            
    return(d)


d = GenerateDataSet(n,years)

d = GenerateYearColumn(d,n,years)

d = GenerateAttributes(d, attribute_count)

d = CreateClients(d,d.shape[0],n)

d = GenerateLHTR(d, .8, .1)

d = GenerateAttributeScore(d,attribute_count)

d.to_csv("NPS_DATA.csv")
