import numpy as np
import matplotlib.pyplot as plt
import pandas as pd




def main():

  df = pd.read_csv("dataset/dataset.csv")
  print (df.to_markdown)

  alt = df[0,"elev_01":0,"elev_100"]



  return 0




# INICIO    
if __name__ == '__main__':
    main()



