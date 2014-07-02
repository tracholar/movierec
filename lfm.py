# coding:gbk

import math
import numpy as np
import matplotlib.pyplot as plt
from moviedata import *


def RandomSelectNagativeSample(items, items_pool):
	ret = dict()
	for i in items.keys():
		ret[i] = 1
	
	n = 0
	for i in range(0,len(items) * 3):
		item = items_pool[ np.random.randint(0, len(items_pool) ) ]
		if item in ret:
			continue
		ret[item] = 0
		n += 1
		if n>len(items):
			break
		
	return ret 
	
		
def GetRatings(train):
	R = dict()
	items_pool = []
	for u in train:
		for i in train[u]:
			if i not in items_pool:
				items_pool.append(i)
				
#	f = open('items_pool.txt','w')
#	for i in items_pool:
#		f.write(i + '\n')
#	f.close()
	
#	f = open('ratings.txt','w')
	for u in train:
		R[u] = RandomSelectNagativeSample(train[u], items_pool)
		
#		for v, r in R[u].items():
#			f.write('%s\t%s\t%d\n' % (u, v, r))
#	
#	f.close()
	
	return R
		
def InitModel(train, F):
	p = dict()
	q = dict()
	for u, items in train.items():
		for i, rui in items.items():
			if u not in p:
				p[u] = np.random.random(F)/np.sqrt(F)
			
			if i not in q:
				q[i] = np.random.random(F)/np.sqrt(F)
		
	return p,q

def Predict(u,i,P,Q):
	return np.dot(P[u],Q[i])
	
def LatentFactorModel(user_items, F, N, alpha, lam):
	P, Q = InitModel(user_items, F)
	for step in range(0,N):
		print step
		for u, items in user_items.items():
			for i, rui in items.items():
				eui = rui - Predict(u,i,P,Q)
				
				P[u] += alpha*(eui*Q[i] - lam*P[u])
				Q[i] += alpha*(eui*P[u] - lam*Q[i])
		
		alpha *= 0.9
		
		
	return P,Q

def Recommend(user,P,Q):
	rank = dict()
	for i in Q:
		if i not in rank:
			rank[i] = Predict(user,i,P,Q)
		
	return rank
	
def WritePQ(P,Q):
	f = open('P.txt','w')
	for u,pu in P.items():
		f.write(u + '\t')
		for p in pu:
			f.write('%f\t' % p)
		f.write('\n')
	f.close()
	f = open('Q.txt','w')
	for u,pu in P.items():
		f.write(u + '\t')
		for p in pu:
			f.write('%f\t' % p)
		f.write('\n')
	f.close()

movieInfo = ReadMovieInfo('../data/u.item')
data = ReadData('../data/u.data','\t')
train, test = SplitData(data,4,0,0)
del data
print 'read data finished!'

R = GetRatings(train)
print 'get ratings from train finished!'

P,Q = LatentFactorModel(R, 4, 100, 0.03, 0.01)
WritePQ(P,Q)
print 'P,Q caculated!'

rec = sorted(Recommend(1,P,Q).items(), key=itemgetter(1), reverse=True)[0:20]
for i,r in rec:
	print i,r
