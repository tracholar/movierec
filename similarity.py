# coding:gbk
import math

def UserSimilarity(train):
	item_users = dict()
	for u, items in train.items():
		for i in items.keys():
			if i not in item_users:
				item_users[i] = set()
			item_users[i].add(u)
			
	C = dict()
	N = dict()
	for i, users in item_users.items():
		for u in users:
			if u not in N:
				N[u] = 0
			N[u] += 1
			
			if u not in C:
				C[u] = dict()
				
			for v in users:
				if u==v:
					continue
				if v not in C[u]:
					C[u][v] = 0
					
				C[u][v] += 1
				
	W = dict()
	for u, related_users in C.items():
		for v, cuv in related_users.items():
			if u not in W:
				W[u] = dict()
			W[u][v] = cuv / math.sqrt(N[u] * N[v])

	return W 
