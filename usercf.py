# coding:gbk
import math
import numpy as np
import matplotlib.pyplot as plt
from moviedata import *
from similarity import *

def Recall(train, test, N):
	hit = 0
	all = 0
	
	for user in train.keys():
		if user not in test:
			tu = dict()
		else:
			tu = test[user]
		rank = GetRecommendation(user,N)
		for item, pui in rank.items():
			if item in tu:
				hit += 1
			
		all += len(tu)
		
	return hit / (all*1.0)

def Precision(train, test, N):
	hit = 0
	all = 0
	
	for user in train.keys():
		if user not in test:
			tu = dict()
		else:
			tu = test[user]
		rank = GetRecommendation(user,N)
		for item, pui in rank.items():
			if item in tu:
				hit += 1
			
		all += N
		
	return hit / (all*1.0)
	
def Coverage(train, test, N):
	recommend_items = set()
	all_items = set()
	
	for user in train.keys():
		for item in train[user].keys():
			all_items.add(item)
		rank = GetRecommendation(user,N)
		for item in rank.keys():
			recommend_items.add(item)
		
	return len(recommend_items) * 1.0 / len(all_items)
	
def Popularity(train, test, N):
	item_popularity = dict()
	for user, items in train.items():
		for item in items.keys():
			if item not in item_popularity:
				item_popularity[item] = 0
			
			item_popularity[item] += 1
		
	ret = 0
	n = 0
	for user in train.keys():
		rank = GetRecommendation(user, N)
		for item in rank.keys():
			ret += math.log(1+item_popularity[item])
			n += 1
		
	ret /= n * 1.0
	return ret
	
def Recommend(user, train, W, K=3):
	rank = dict()
	
	if user not in train:
		return rank
	interacted_items = train[user]
	
	for v, wuv in sorted(W[user].items(), key=itemgetter(1), reverse=True)[0:K]:
		for i, rvi in train[v].items():
			if i in interacted_items:
				continue
			if i not in rank:
				rank[i] = 0
			rank[i] += wuv*rvi
		
	return rank

def GetRecommendation(user, N):
	rank = Recommend(user,train,W,N)
	movies = []
	for m, p in rank.items():
		movies.append([m,p])
	movies.sort(key=itemgetter(1),reverse=True)
	
	ret = dict()
	for m, p in movies[0:N]:
		ret[m] = p
		
	return ret 

	
movieInfo = ReadMovieInfo('../data/u.item')
data = ReadData('../data/u.data','\t')
train, test = SplitData(data,4,0,0)
del data
print 'read data finished!'
	
W = UserSimilarity(train)
print 'caculate similarity finished!'

n = 6
pr = np.zeros(n)
re = np.zeros(n)
co = np.zeros(n)
po = np.zeros(n)
for i in range(n):
	N = 5*2**i
	pr[i] = Precision(train,test,N)
	re[i] = Recall(train,test,N)
	co[i] = Coverage(train,test,N)
	po[i] = Popularity(train,test,N)
	
	print 'precision',pr[i]
	print 'recall',re[i]
	print 'coverage',co[i]
	print 'popularity',po[i]
	
x = 5*2**np.arange(n)
plt.figure()
plt.plot(x,pr,'r.-',x,re,'b.-',x,co,'g.-')
plt.show()