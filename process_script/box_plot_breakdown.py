import matplotlib.pyplot as plt
import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import warnings
from process_data import *
import seaborn as sns



def plot_box_breakdown(data, labels, save_file_name, title, use_color=False, with_llm=False):
     plt.figure(figsize=(12, 7))
     box = plt.boxplot(data, vert=False, patch_artist=True)

     plt.yticks(range(1, len(labels) + 1), labels,fontsize=13)
     plt.xticks(fontsize=15)

     plt.title(title, fontsize=15)
     plt.xlabel("Time (us)", fontsize=15)
     plt.ylabel("Segment Name", fontsize=15)
     if with_llm:
          plt.xscale('log')
     if use_color:
          palette = sns.color_palette("tab10", len(data))
          for patch, color in zip(box['boxes'], palette):
               patch.set_facecolor(color)
     plt.tight_layout()
     plt.savefig(save_file_name)
     plt.show()
     



if __name__ == "__main__":
     arguments = sys.argv
     if len(sys.argv) < 3:
          print("Usage: python3 dot_plot_data.py <data_dir> <save_dir> ")
          exit()
     local_dir = sys.argv[1]
     save_dir = sys.argv[2]
     print("drop_warmup number:")
     drop_warmup_num = int(input())
     print("color box plot(T/F):")
     use_color = False
     if input() == "T":
          use_color = True
     else:
          use_color = False
     with_llm = False
     print("with_llm(T/F):")
     if input() == "T":
          with_llm = True
     


     
     log_files = get_log_files(local_dir, suffix)
     log_data = get_log_files_dataframe(log_files)
     df = clean_log_dataframe(log_data,drop_warmup=drop_warmup_num)

     from_back_client_dict = process_from_back_client(df.copy()) 
     bt_udls_dict = process_btw_udls(df.copy())    
     start_to_udl1_df = from_back_client_dict['from_client_time']
     start_to_udl1_times = start_to_udl1_df['from_client_time']
     
     udl1_df = process_udl1_dataframe(df)['udl1_time']
     udl1_times = udl1_df['udl1_time']
     
     udl1_2_df = bt_udls_dict['udl1_udl2_time']
     udl1_2_times = udl1_2_df['udl1_udl2_time']

     # udl2_df = process_udl2_dataframe(df)['udl2_time']
     # udl2_times = udl2_df['udl2_time']
     udl2_df = process_udl2_dataframe(df)[0]['batch_search_time']
     udl2_times = udl2_df['batch_search_time']
     
     udl2_3_df = bt_udls_dict['udl2_udl3_time']
     udl2_3_times = udl2_3_df['udl2_udl3_time']
     
     udl3_df = process_udl3_dataframe(df)['udl3_time']
     udl3_times = udl3_df['udl3_time']

     udl3_end_df = from_back_client_dict['back_client_time']
     udl3_end_times = udl3_end_df['back_client_time']    

     end_to_end_latency = process_end_to_end_latency_dataframe(df)["e2e_latency"]
     
     if with_llm:
          labels = [
               "Vortex RAG End-to-End Latency",
               "UDL3-Aggregator",
               "UDL3:resultAgg+LLM",
               "UDL2-3",
               "UDL2:batchSearch",#"UDL2:objectmatch",
               "UDL1-2",
               "UDL1:encoder+clustermatch",
               "Aggregator-UDL1"
          ]
          title = "Vortex RAG Latency Breakdown by query processing segments (log scale)"
     else:
          labels = [
               "Vortex Vector Search End-to-End Latency",
               "UDL3-Aggregator",
               "UDL3:resultAgg",
               "UDL2-3",
               "UDL2:batchSearch",#"UDL2:objectmatch",
               "UDL1-2",
               "UDL1:clustermatch",
               "Aggregator-UDL1"
          ]
          title = "Vortex VectorSearch Latency Breakdown by query processing segments"

     data = [
          end_to_end_latency,
          udl3_end_times,
          udl3_times,
          udl2_3_times,
          udl2_times,
          udl1_2_times,
          udl1_times,
          start_to_udl1_times
     ]
     
     if use_color:
          plot_name = "box_plot_color" + local_dir.split("/")[-1] +".pdf"
     else:
          plot_name = "box_plot" + local_dir.split("/")[-1] +".pdf"
     save_file_dir = os.path.join(save_dir, plot_name)
     plot_box_breakdown(data, labels,  save_file_name=save_file_dir,title = title, use_color=use_color, with_llm=with_llm)