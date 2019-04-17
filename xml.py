#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 16:55:16 2019

@author: dingwenna
"""
import operator
import pandas as pd
import numpy as np


################################################
#The first part: aim to generate the templete.xml file
#You should replace  [] with {} before applying this templete.xml to do the next part in this python script.
#also, you need to add f'''\ at the begining and  ''' at last. (see template.xml)
################################################

xml_template = 'xml_template.xml'
data = pd.read_csv('xml_data.csv', sep=',')
group = data['family']
length = len(np.unique(group))

tempelete_lines = []
l=0
for l in range(length-1):
#    print(l)
    tempelete_lines.extend([f'''[''.join(prior_distribution_lines_{l})]\n\t\t\t\t[''.join(prior_taxaset_lines_{l})]\n\t\t\t\t\t[','.join(prior_taxa_lines_{l})]\n\t\t\t\t</taxonset>\n\t\t\t\t[''.join(prior_uniform_lines_{l})]\n\t\t\t</distribution>'''])

tempelete_lines = '\n\t\t\t'.join(tempelete_lines)

with open(xml_template, 'w') as outf:
    outf.write(eval(open('preTemplate.xml').read()))

####################################################
#The second part: aim to generate the Caryophyllales._prior.xml
###################################################
## 'tree' file should be the same name with the **.nex file by defalt, but you can check the name on the original file generated from BEAUTi

tree="@Tree.t:Caryophyllales_COM"
xml_output = 'Caryophyllales_prior.xml'
data = pd.read_csv('xml_data.csv', sep=',')
group = data['family']
taxa = data['taxa']
uniform = data['uniform']
min = data['min']
max = data['max']
length = len(np.unique(group))
#creat empty list for storing strings later
for j in range(length+1):
    globals()['prior_distribution_lines_'+str(j)] = []
for j in range(length+1):
    globals()['prior_taxaset_lines_'+str(j)] = []
for j in range(length+1):
    globals()['prior_taxa_lines_'+str(j)] = []
for j in range(length+1):
    globals()['prior_uniform_lines_'+str(j)] = []
prior_idref_lines =[]

#prior_distribution_lines = []
#prior_taxaset_lines = []
#prior_taxa_lines = []
#prior_uniform_lines_j = []
#prior_idref_lines =[]

# n starts from 7, because the prior of unform ends at 6 in the original xml file
n = 7
i=0
j=0
for i in range(len(taxa)-1):
    if group.iloc[i] == group.iloc[i+1]:
#        print(i)
         globals()['prior_taxa_lines_'+str(j)].extend([f'<taxon id="{taxa[i]}" spec="Taxon"/>'])
    else :
#        continue
        globals()['prior_taxa_lines_'+str(j)].extend([f'<taxon id="{taxa[i]}" spec="Taxon"/>'])
        globals()['prior_taxaset_lines_'+str(j)].extend([f'<taxonset id="{group[i]}" spec="TaxonSet">'])
        prior_idref_lines .extend([f'<log idref="{group[i]}.prior"/>'])
        if uniform[i] == 'crown':
            globals()['prior_distribution_lines_'+str(j)].extend([f'<distribution id="{group[i]}.prior" spec="beast.math.distributions.MRCAPrior" monophyletic="true" tree="{tree}">'])
            globals()['prior_uniform_lines_'+str(j)].extend([f'<Uniform id="Uniform.{n}" lower="{min[i]}" name="distr" upper="{max[i]}"/>'])
        elif uniform[i] == 'stem':
            globals()['prior_distribution_lines_'+str(j)].extend([f'<distribution id="{group[i]}.prior" spec="beast.math.distributions.MRCAPrior" monophyletic="true" tree="{tree}" useOriginate="true">'])
            globals()['prior_uniform_lines_'+str(j)].extend([f'<Uniform id="Uniform.{n}" lower="{min[i]}" name="distr" upper="{max[i]}"/>'])
        else :
            globals()['prior_distribution_lines_'+str(j)].extend([f'<distribution id="{group[i]}.prior" spec="beast.math.distributions.MRCAPrior" monophyletic="true" tree="{tree}">'])
        i=i+1
        n=n+1
        j=j+1

globals()['prior_distribution_lines_'+str(j)]= '\n'.join(globals()['prior_distribution_lines_'+str(j)])
globals()['prior_taxaset_lines_'+str(j)] = '\n'.join(globals()['prior_taxaset_lines_'+str(j)])
globals()['prior_taxa_lines_'+str(j)] = '\n'.join(globals()['prior_taxa_lines_'+str(j)])
globals()['prior_uniform_lines_'+str(j)] = '\n'.join(globals()['prior_uniform_lines_'+str(j)])
prior_idref_lines  = '\n\t\t'.join(prior_idref_lines)

with open(xml_output, 'w') as outf:
    outf.write(eval(open('xlm_template.xml').read()))
