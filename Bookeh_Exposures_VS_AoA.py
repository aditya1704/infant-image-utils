# -*- coding: utf-8 -*-
"""Bookeh_Exposures_VS_AoA.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1iJ0imm77GucHmUcv40cwCZZQObNbx1PY
"""

import pandas as pd

# Load the Excel file
file_path = './MCDI_word_counts_for_each_age.xlsx'
xls = pd.ExcelFile(file_path)

# Age groups represented by their upper limits
age_groups = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17, 18,19,20,21,22,23,24,25,26,27,28,29,30]

# Initialize empty dataframes
mcdi_df = pd.DataFrame()
non_mcdi_df = pd.DataFrame()

# Loop through each age group and process the data
for age in age_groups:
    if f'{age}_MCDI_Words' not in xls.sheet_names:
        continue
    # Load MCDI and All_Words data for the current age group
    mcdi_words = pd.read_excel(xls, sheet_name=f'{age}_MCDI_Words')
    all_words = pd.read_excel(xls, sheet_name=f'{age}_All_Words')

    # Add an Age_group column to both dataframes
    mcdi_words['Age_group'] = age
    all_words['Age_group'] = age

    # Append MCDI words to mcdi_df
    mcdi_df = pd.concat([mcdi_df, mcdi_words], ignore_index=True)

    # Filter out MCDI words from All_Words to get non-MCDI words
    non_mcdi_words = all_words[~all_words['Word'].isin(mcdi_words['Word'])]
    non_mcdi_df = pd.concat([non_mcdi_df, non_mcdi_words], ignore_index=True)

# Add a 'Category' column to distinguish MCDI and NON-MCDI data
mcdi_df['Category'] = 'MCDI'
non_mcdi_df['Category'] = 'NON-MCDI'

age_group_data = {
        'Age_group': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28],
        'Total Duration (min)': [421.82, 534.93, 640.78, 524.87, 628.65, 759.16, 752.04, 742.43, 589.14, 563.55,
                             243.03, 705.29, 370.49, 556.52, 198.81, 175.67, 353.96, 717.56, 710.56, 0.03,
                             246.82, 275.23, 154.99, 356.73, 520.95, 217.95, 244.35],
        'wake_time': [8,8,8, 8,8,8, 12,12,12, 12,12,12, 14,14,14,14,14,14, 14,14,14,14,14,14, 14,14,14]
    }

df_age_group = pd.DataFrame(age_group_data)

mcdi_df = pd.merge(df_age_group, mcdi_df, on='Age_group')
non_mcdi_df = pd.merge(df_age_group, non_mcdi_df, on='Age_group')

mcdi_df['Count'] = pd.to_numeric(mcdi_df['Count'], errors='coerce')
mcdi_df['wake_time'] = pd.to_numeric(mcdi_df['wake_time'], errors='coerce')
non_mcdi_df['Count'] = pd.to_numeric(non_mcdi_df['Count'], errors='coerce')
non_mcdi_df['wake_time'] = pd.to_numeric(non_mcdi_df['wake_time'], errors='coerce')


# Calculate the extended count
mcdi_df['extended count'] = (mcdi_df['wake_time'] * mcdi_df['Count']) / (mcdi_df['Total Duration (min)'] / 60)
non_mcdi_df['extended count'] = (non_mcdi_df['wake_time'] * non_mcdi_df['Count']) / (non_mcdi_df['Total Duration (min)'] / 60)

# Sort data by Word and Age_group to ensure cumulative calculation across age progression
mcdi_df = mcdi_df.sort_values(['Word', 'Age_group'])
non_mcdi_df = non_mcdi_df.sort_values(['Word', 'Age_group'])

# Calculate the cumulative count across age progression for each word in MCDI and NON-MCDI data
mcdi_df['Cumulative_count'] = mcdi_df.groupby('Word')['Count'].cumsum()
mcdi_df['Extended Cumulative_count'] = mcdi_df.groupby('Word')['extended count'].cumsum()

non_mcdi_df['Cumulative_count'] = non_mcdi_df.groupby('Word')['Count'].cumsum()
non_mcdi_df['Extended Cumulative_count'] = non_mcdi_df.groupby('Word')['extended count'].cumsum()

import pandas as pd
import numpy as np
from bokeh.palettes import Category10
from bokeh.plotting import figure, show
from bokeh.models import Paragraph, Panel, Tabs,Span
from bokeh.layouts import row,column

data = {
    'Age_group': [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
    'animal': [0.03, 0.06, 0.10, 0.20, 0.21, 0.30, 0.32, 0.46, 0.49, 0.54, 0.57, 0.59, 0.67, 0.71, 0.79],
    'bug': [0.10, 0.14, 0.22, 0.41, 0.40, 0.43, 0.52, 0.60, 0.65, 0.69, 0.73, 0.74, 0.78, 0.78, 0.83],
    'bird': [0.32, 0.43, 0.50, 0.66, 0.66, 0.74, 0.72, 0.80, 0.85, 0.88, 0.90, 0.89, 0.90, 0.90, 0.95],
    'butterfly': [0.06, 0.09, 0.14, 0.24, 0.27, 0.35, 0.42, 0.55, 0.61, 0.64, 0.64, 0.68, 0.74, 0.82, 0.86],
    'cat': [0.35, 0.44, 0.46, 0.62, 0.66, 0.70, 0.77, 0.83, 0.84, 0.87, 0.87, 0.93, 0.87, 0.93, 0.96],
    'dog': [0.62, 0.68, 0.75, 0.79, 0.82, 0.84, 0.84, 0.91, 0.91, 0.93, 0.92, 0.94, 0.94, 0.95, 0.96],
    'elephant': [0.06, 0.11, 0.17, 0.29, 0.31, 0.35, 0.50, 0.58, 0.66, 0.65, 0.69, 0.75, 0.77, 0.81, 0.88],
    'fish': [0.21, 0.32, 0.38, 0.53, 0.56, 0.57, 0.70, 0.74, 0.80, 0.84, 0.83, 0.86, 0.90, 0.91, 0.93]
}
animal_Data = pd.DataFrame(data)
animal_Data = animal_Data.melt(id_vars=['Age_group'], var_name='Word', value_name='AoA')

animals = ["animal", "bird", "bug", "butterfly", "cat", "dog", "elephant", "fish"]
df = mcdi_df[mcdi_df['Word'].isin(animals)]

# Merge df1_long and df2 on Age_group and Word
merged_df = pd.merge(df, animal_Data, on=['Age_group', 'Word'], how='left')

# Set up the figure
p1 = figure(width=800, height=550)
p1.title.text = 'Animals'
#p11.x_range = Range1d(12, 30)
p1.xaxis.axis_label = 'Exposure (No. of times the word is heard by infant)'
p1.yaxis.axis_label = 'Age of Acquisition'
#xticks = np.array([12,13,14,15,16, 18, 20, 22, 24, 26, 28, 30])
#p11.xaxis.ticker = FixedTicker(ticks=xticks)
unique_words = merged_df['Word'].unique()

for word, color in zip(unique_words, Category10[len(unique_words)]):
    df = merged_df[merged_df['Word'] == word]
    p1.line(df['Extended Cumulative_count'], df['AoA'], line_width=2, color=color, alpha=0.8,
           muted_color=color, muted_alpha=0.2, legend_label=word)

# Configure legend
p1.legend.location = "bottom_right"
p1.legend.click_policy = "mute"

# Display the plot
#show(p1)

# Add the layout to a tab
tab1 = Panel(child=p1, title="Animals")

# Define the data
data = {
    'Age_group': [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
    'airplane': [0.13, 0.20, 0.30, 0.44, 0.48, 0.55, 0.61, 0.70, 0.77, 0.81, 0.82, 0.85, 0.88, 0.90, 0.93],
    'bicycle': [0.09, 0.15, 0.21, 0.32, 0.36, 0.42, 0.52, 0.61, 0.67, 0.71, 0.73, 0.75, 0.81, 0.84, 0.90],
    'boat': [0.17, 0.21, 0.29, 0.45, 0.44, 0.51, 0.58, 0.72, 0.74, 0.75, 0.80, 0.79, 0.86, 0.87, 0.91],
    'bus': [0.15, 0.20, 0.25, 0.39, 0.41, 0.47, 0.60, 0.71, 0.76, 0.76, 0.76, 0.82, 0.84, 0.89, 0.92],
    'car': [0.35, 0.47, 0.55, 0.70, 0.76, 0.77, 0.77, 0.88, 0.92, 0.90, 0.92, 0.93, 0.94, 0.95, 0.97],
    'train': [0.11, 0.17, 0.24, 0.37, 0.47, 0.48, 0.56, 0.69, 0.77, 0.77, 0.82, 0.81, 0.87, 0.88, 0.93],
    'truck': [0.27, 0.31, 0.40, 0.55, 0.56, 0.62, 0.68, 0.78, 0.81, 0.83, 0.85, 0.86, 0.88, 0.92, 0.93]
}

vehicle_Data = pd.DataFrame(data)
vehicle_Data = vehicle_Data.melt(id_vars=['Age_group'], var_name='Word', value_name='AoA')

vehicles = ["airplane", "bicycle", "boat", "bus", "car", "train", "truck"]
df = mcdi_df[mcdi_df['Word'].isin(vehicles)]

# Merge df1_long and df2 on Age_group and Word
merged_df = pd.merge(df, vehicle_Data, on=['Age_group', 'Word'], how='left')

# Set up the figure
p2 = figure(width=800, height=550)
p2.title.text = 'Animals'
#p21.x_range = Range1d(12, 30)
p2.xaxis.axis_label = 'Exposure (No. of times the word is heard by infant)'
p2.yaxis.axis_label = 'Age of Acquisition'
#xticks = np.array([12,13,14,15,16, 18, 20, 22, 24, 26, 28, 30])
#p21.xaxis.ticker = FixedTicker(ticks=xticks)
unique_words = merged_df['Word'].unique()

for word, color in zip(unique_words, Category10[len(unique_words)]):
    df = merged_df[merged_df['Word'] == word]
    p2.line(df['Extended Cumulative_count'], df['AoA'], line_width=2, color=color, alpha=0.8,
           muted_color=color, muted_alpha=0.2, legend_label=word)

# Configure legend
p2.legend.location = "bottom_right"
p2.legend.click_policy = "mute"

# Display the plot
#show(p2)

# Add the layout to a tab
tab2 = Panel(child=p2, title="Vehicles")

# Define the data
data = {
    'Age_group': [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
    'ball': [0.73, 0.80, 0.85, 0.91, 0.93, 0.93, 0.95, 0.96, 0.96, 0.97, 0.95, 0.97, 0.96, 0.96, 0.98],
    'balloon': [0.29, 0.39, 0.46, 0.61, 0.65, 0.67, 0.68, 0.79, 0.84, 0.86, 0.87, 0.88, 0.90, 0.92, 0.94],
    'bat': [0.05, 0.05, 0.10, 0.14, 0.18, 0.20, 0.24, 0.29, 0.36, 0.39, 0.44, 0.42, 0.54, 0.55, 0.55],
    'book': [0.44, 0.57, 0.63, 0.74, 0.77, 0.79, 0.82, 0.85, 0.91, 0.89, 0.89, 0.92, 0.92, 0.93, 0.97],
    'crayon': [0.03, 0.08, 0.13, 0.28, 0.25, 0.36, 0.46, 0.51, 0.57, 0.67, 0.65, 0.70, 0.74, 0.79, 0.83],
    'game': [0.01, 0.02, 0.05, 0.09, 0.10, 0.15, 0.24, 0.27, 0.32, 0.43, 0.43, 0.48, 0.62, 0.63, 0.74],
    'pencil': [0.01, 0.04, 0.06, 0.16, 0.16, 0.24, 0.24, 0.34, 0.34, 0.43, 0.48, 0.50, 0.58, 0.61, 0.69],
    'toy (object)': [0.13, 0.16, 0.24, 0.36, 0.43, 0.48, 0.52, 0.64, 0.68, 0.75, 0.76, 0.79, 0.82, 0.87, 0.93]
}

toys_Data = pd.DataFrame(data)
toys_Data = toys_Data.melt(id_vars=['Age_group'], var_name='Word', value_name='AoA')

toys = ["ball", "balloon", "bat", "book", "crayon", "game", "pencil", "toy"]
df = mcdi_df[mcdi_df['Word'].isin(toys)]

# Merge df1_long and df2 on Age_group and Word
merged_df = pd.merge(df, toys_Data, on=['Age_group', 'Word'], how='left')

# Set up the figure
p3 = figure(width=800, height=550)
p3.title.text = 'Toys'
#p31.x_range = Range1d(12, 30)
p3.xaxis.axis_label = 'Exposure (No. of times the word is heard by infant)'
p3.yaxis.axis_label = 'Age of Acquisition'
#xticks = np.array([12,13,14,15,16, 18, 20, 22, 24, 26, 28, 30])
#p31.xaxis.ticker = FixedTicker(ticks=xticks)
unique_words = merged_df['Word'].unique()

for word, color in zip(unique_words, Category10[len(unique_words)]):
    df = merged_df[merged_df['Word'] == word]
    p3.line(df['Extended Cumulative_count'], df['AoA'], line_width=2, color=color, alpha=0.8,
           muted_color=color, muted_alpha=0.2, legend_label=word)

# Configure legend
p3.legend.location = "bottom_right"
p3.legend.click_policy = "mute"

# Display the plot
#show(p3)

# Add the layout to a tab
tab3 = Panel(child=p3, title="Toys")

# Define the data
data = {
    'Age_group': [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
    'apple': [0.29, 0.37, 0.48, 0.64, 0.60, 0.68, 0.78, 0.86, 0.87, 0.89, 0.88, 0.91, 0.92, 0.93, 0.95],
    'banana': [0.45, 0.53, 0.63, 0.69, 0.71, 0.75, 0.80, 0.89, 0.90, 0.91, 0.90, 0.92, 0.91, 0.94, 0.98],
    'bread': [0.09, 0.15, 0.20, 0.36, 0.37, 0.42, 0.51, 0.61, 0.67, 0.70, 0.74, 0.74, 0.82, 0.86, 0.91],
    'butter': [0.02, 0.04, 0.09, 0.14, 0.18, 0.25, 0.28, 0.41, 0.43, 0.49, 0.54, 0.59, 0.62, 0.68, 0.75],
    'chocolate': [0.02, 0.04, 0.07, 0.11, 0.16, 0.23, 0.29, 0.43, 0.47, 0.52, 0.54, 0.63, 0.71, 0.72, 0.81],
    'coffee': [0.04, 0.06, 0.10, 0.20, 0.21, 0.26, 0.33, 0.46, 0.51, 0.52, 0.56, 0.58, 0.63, 0.71, 0.77],
    'egg': [0.09, 0.17, 0.19, 0.35, 0.35, 0.46, 0.52, 0.65, 0.69, 0.70, 0.74, 0.78, 0.80, 0.86, 0.90],
    'fish (food)': [0.09, 0.13, 0.18, 0.32, 0.34, 0.35, 0.40, 0.48, 0.52, 0.58, 0.56, 0.57, 0.65, 0.71, 0.74],
    'milk': [0.35, 0.38, 0.49, 0.65, 0.64, 0.71, 0.73, 0.80, 0.85, 0.86, 0.86, 0.90, 0.90, 0.93, 0.96],
    'water (beverage)': [0.23, 0.32, 0.44, 0.55, 0.59, 0.66, 0.69, 0.82, 0.84, 0.84, 0.84, 0.89, 0.89, 0.90, 0.94]
}
food_drink_Data = pd.DataFrame(data)
food_drink_Data = food_drink_Data.melt(id_vars=['Age_group'], var_name='Word', value_name='AoA')

food_and_drink = [ "banana", "bread", "butter", "chocolate", "coffee", "egg", "fish","milk", "water"]
df = mcdi_df[mcdi_df['Word'].isin(food_and_drink)]

# Merge df1_long and df2 on Age_group and Word
merged_df = pd.merge(df, food_drink_Data, on=['Age_group', 'Word'], how='left')

# Set up the figure
p4 = figure(width=800, height=550)
p4.title.text = 'Food & Drinks'
#p41.x_range = Range1d(12, 30)
p4.xaxis.axis_label = 'Exposure (No. of times the word is heard by infant)'
p4.yaxis.axis_label = 'Age of Acquisition'
#xticks = np.array([12,13,14,15,16, 18, 20, 22, 24, 26, 28, 30])
#p41.xaxis.ticker = FixedTicker(ticks=xticks)
unique_words = merged_df['Word'].unique()

for word, color in zip(unique_words, Category10[len(unique_words)]):
    df = merged_df[merged_df['Word'] == word]
    p4.line(df['Extended Cumulative_count'], df['AoA'], line_width=2, color=color, alpha=0.8,
           muted_color=color, muted_alpha=0.2, legend_label=word)

# Configure legend
p4.legend.location = "bottom_right"
p4.legend.click_policy = "mute"

# Display the plot
#show(p4)

# Add the layout to a tab
tab4 = Panel(child=p4, title="Food & Drinks")

data = {
    "Age_group": [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
    "diaper": [0.21, 0.30, 0.41, 0.52, 0.53, 0.58, 0.65, 0.76, 0.77, 0.85, 0.84, 0.85, 0.88, 0.91, 0.93],
    "dress (object)": [0.03, 0.05, 0.09, 0.14, 0.18, 0.23, 0.30, 0.39, 0.42, 0.47, 0.52, 0.57, 0.55, 0.66, 0.70],
    "gloves": [0.00, 0.03, 0.05, 0.09, 0.13, 0.13, 0.21, 0.31, 0.35, 0.37, 0.47, 0.43, 0.51, 0.64, 0.68],
    "hat": [0.23, 0.34, 0.46, 0.58, 0.61, 0.67, 0.72, 0.82, 0.82, 0.84, 0.84, 0.85, 0.85, 0.89, 0.95],
    "pants": [0.07, 0.11, 0.20, 0.31, 0.35, 0.45, 0.54, 0.66, 0.71, 0.71, 0.76, 0.81, 0.86, 0.88, 0.92],
    "scarf": [0.00, 0.01, 0.01, 0.05, 0.04, 0.08, 0.08, 0.16, 0.16, 0.18, 0.18, 0.22, 0.26, 0.35, 0.43],
    "shirt": [0.08, 0.12, 0.23, 0.35, 0.39, 0.48, 0.56, 0.67, 0.69, 0.73, 0.75, 0.82, 0.84, 0.86, 0.90],
    "shorts": [0.03, 0.03, 0.08, 0.13, 0.16, 0.25, 0.28, 0.37, 0.44, 0.48, 0.55, 0.58, 0.68, 0.74, 0.75],
    "sock": [0.22, 0.26, 0.41, 0.55, 0.55, 0.60, 0.66, 0.72, 0.78, 0.76, 0.83, 0.84, 0.87, 0.87, 0.91],
}
clothing_Data = pd.DataFrame(data)
clothing_Data = clothing_Data.melt(id_vars=['Age_group'], var_name='Word', value_name='AoA')

clothing = ["diaper", "dress", "gloves", "hat", "pants", "scarf", "shirt", "shorts", "sock" ]
df = mcdi_df[mcdi_df['Word'].isin(clothing)]

# Merge df1_long and df2 on Age_group and Word
merged_df = pd.merge(df, clothing_Data, on=['Age_group', 'Word'], how='left')

# Set up the figure
p5 = figure(width=800, height=550)
p5.title.text = 'Clothing'
#p51.x_range = Range1d(12, 30)
p5.xaxis.axis_label = 'Exposure (No. of times the word is heard by infant)'
p5.yaxis.axis_label = 'Age of Acquisition'
#xticks = np.array([12,13,14,15,16, 18, 20, 22, 24, 26, 28, 30])
#p51.xaxis.ticker = FixedTicker(ticks=xticks)
unique_words = merged_df['Word'].unique()

for word, color in zip(unique_words, Category10[len(unique_words)]):
    df = merged_df[merged_df['Word'] == word]
    p5.line(df['Extended Cumulative_count'], df['AoA'], line_width=2, color=color, alpha=0.8,
           muted_color=color, muted_alpha=0.2, legend_label=word)

# Configure legend
p5.legend.location = "bottom_right"
p5.legend.click_policy = "mute"

# Display the plot
#show(p5)


# Add the layout to a tab
tab5 = Panel(child=p5, title="Clothing")

data = {
    "Age_group": [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
    "ear": [0.28, 0.38, 0.49, 0.61, 0.64, 0.69, 0.76, 0.82, 0.86, 0.86, 0.89, 0.90, 0.90, 0.92, 0.95],
    "eye": [0.31, 0.44, 0.58, 0.72, 0.75, 0.79, 0.84, 0.87, 0.92, 0.92, 0.89, 0.94, 0.93, 0.95, 0.96],
    "face": [0.03, 0.08, 0.11, 0.22, 0.23, 0.29, 0.42, 0.48, 0.56, 0.63, 0.64, 0.72, 0.78, 0.80, 0.86],
    "hair": [0.15, 0.28, 0.34, 0.50, 0.53, 0.62, 0.69, 0.78, 0.81, 0.82, 0.82, 0.87, 0.92, 0.91, 0.95],
    "hand": [0.07, 0.13, 0.24, 0.36, 0.42, 0.56, 0.58, 0.73, 0.76, 0.78, 0.81, 0.84, 0.89, 0.92, 0.93],
    "leg": [0.03, 0.08, 0.12, 0.25, 0.29, 0.34, 0.47, 0.58, 0.64, 0.68, 0.68, 0.77, 0.81, 0.83, 0.88],
    "mouth": [0.17, 0.24, 0.34, 0.50, 0.52, 0.58, 0.65, 0.74, 0.77, 0.79, 0.81, 0.86, 0.88, 0.90, 0.91],
    "nose": [0.33, 0.46, 0.54, 0.68, 0.71, 0.76, 0.81, 0.85, 0.89, 0.90, 0.88, 0.92, 0.91, 0.93, 0.96],
    "tooth": [0.08, 0.15, 0.24, 0.41, 0.37, 0.46, 0.53, 0.61, 0.67, 0.76, 0.73, 0.77, 0.79, 0.84, 0.88],
}
body_parts_Data = pd.DataFrame(data)
body_parts_Data = body_parts_Data.melt(id_vars=['Age_group'], var_name='Word', value_name='AoA')

body_parts = ["ear", "eye", "face", "hair", "hand", "leg", "mouth", "nose", "tooth" ]
df = mcdi_df[mcdi_df['Word'].isin(body_parts)]

# Merge df1_long and df2 on Age_group and Word
merged_df = pd.merge(df, body_parts_Data, on=['Age_group', 'Word'], how='left')

# Set up the figure
p6 = figure(width=800, height=550)
p6.title.text = 'Body Parts'
#p61.x_range = Range1d(12, 30)
p6.xaxis.axis_label = 'Exposure (No. of times the word is heard by infant)'
p6.yaxis.axis_label = 'Age of Acquisition'
#xticks = np.array([12,13,14,15,16, 18, 20, 22, 24, 26, 28, 30])
#p61.xaxis.ticker = FixedTicker(ticks=xticks)
unique_words = merged_df['Word'].unique()

for word, color in zip(unique_words, Category10[len(unique_words)]):
    df = merged_df[merged_df['Word'] == word]
    p6.line(df['Extended Cumulative_count'], df['AoA'], line_width=2, color=color, alpha=0.8,
           muted_color=color, muted_alpha=0.2, legend_label=word)

# Configure legend
p6.legend.location = "bottom_right"
p6.legend.click_policy = "mute"

# Display the plot
#show(p6)


# Add the layout to a tab
tab6 = Panel(child=p6, title="Body Parts")

# Data for the DataFrame
data = {
    'Age_group': [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
    'bottle': [0.32, 0.35, 0.40, 0.49, 0.57, 0.61, 0.62, 0.68, 0.69, 0.76, 0.77, 0.80, 0.84, 0.86, 0.91],
    'clock': [0.09, 0.10, 0.19, 0.30, 0.31, 0.36, 0.38, 0.49, 0.48, 0.56, 0.58, 0.60, 0.64, 0.67, 0.79],
    'comb': [0.05, 0.08, 0.11, 0.21, 0.24, 0.28, 0.30, 0.35, 0.41, 0.46, 0.51, 0.55, 0.60, 0.60, 0.69],
    'cup': [0.22, 0.26, 0.40, 0.50, 0.56, 0.61, 0.71, 0.77, 0.78, 0.86, 0.87, 0.91, 0.90, 0.91, 0.94],
    'dish': [0.01, 0.03, 0.06, 0.13, 0.15, 0.21, 0.21, 0.28, 0.30, 0.36, 0.36, 0.48, 0.52, 0.52, 0.61],
    'medicine': [0.03, 0.05, 0.09, 0.20, 0.19, 0.23, 0.30, 0.38, 0.45, 0.54, 0.59, 0.62, 0.64, 0.70, 0.77],
    'money': [0.02, 0.06, 0.10, 0.22, 0.25, 0.30, 0.33, 0.37, 0.45, 0.53, 0.58, 0.61, 0.69, 0.70, 0.72],
    'pillow': [0.05, 0.10, 0.14, 0.29, 0.31, 0.40, 0.43, 0.58, 0.62, 0.66, 0.72, 0.74, 0.82, 0.84, 0.89],
    'spoon': [0.17, 0.20, 0.32, 0.48, 0.51, 0.56, 0.63, 0.73, 0.76, 0.79, 0.80, 0.81, 0.86, 0.87, 0.92],
    'toothbrush': [0.11, 0.13, 0.22, 0.38, 0.38, 0.43, 0.55, 0.68, 0.68, 0.74, 0.75, 0.77, 0.84, 0.86, 0.92]
}
small_household_items_Data = pd.DataFrame(data)
small_household_items_Data = small_household_items_Data.melt(id_vars=['Age_group'], var_name='Word', value_name='AoA')

small_household_items = ["bottle", "clock", "comb", "cup", "dish" , "medicine", "money", "pillow", "spoon", "toothbrush"]
df = mcdi_df[mcdi_df['Word'].isin(small_household_items)]

# Merge df1_long and df2 on Age_group and Word
merged_df = pd.merge(df, small_household_items_Data, on=['Age_group', 'Word'], how='left')

# Set up the figure
p7 = figure(width=800, height=550)
p7.title.text = 'Small Household Items'
#p71.x_range = Range1d(12, 30)
p7.xaxis.axis_label = 'Exposure (No. of times the word is heard by infant)'
p7.yaxis.axis_label = 'Age of Acquisition'
#xticks = np.array([12,13,14,15,16, 18, 20, 22, 24, 26, 28, 30])
#p71.xaxis.ticker = FixedTicker(ticks=xticks)
unique_words = merged_df['Word'].unique()

for word, color in zip(unique_words, Category10[len(unique_words)]):
    df = merged_df[merged_df['Word'] == word]
    p7.line(df['Extended Cumulative_count'], df['AoA'], line_width=2, color=color, alpha=0.8,
           muted_color=color, muted_alpha=0.2, legend_label=word)

# Add horizontal line at AoA = 0.5 to indicate acquisition threshold
threshold_line = Span(location=0.5, dimension='width', line_color='red', line_width=2, line_dash='dashed')
p7.add_layout(threshold_line)

# Configure legend
p7.legend.location = "bottom_right"
p7.legend.click_policy = "mute"

# Display the plot
#show(p7)

tab7 = Panel(child=p7, title="Small Household Items")

tabs = Tabs(tabs=[tab1, tab2, tab3, tab4, tab5,tab6,tab7])
#show(tabs)

from bokeh.io import output_file, save

# Specify the output HTML file
output_file("Bookeh_Exposures_VS_AoA.html")

# Save the entire layout to HTML
save(tabs)

