# coding:gbk

import numpy as np

G = {
	'A':{'a':1,'b':1,'d':1},
	'B':{'a':1,'c':1},
	'C':{'b':1,'e':1},
	'D':{'c':1,'d':1,'e':1},
	'a':{'A':1,'B':1},
	'b':{'A':1,'C':1},
	'c':{'B':1,'D':1},
	'd':{'A':1,'D':1},
	'e':{'C':1,'D':1}
	}

def PrintRank(rank):
	for i, ri in rank.items():
		print '%s:%.3f\t' % (i,ri) ,
	print
	
	
def PersonalRankRandomWalk(G, alpha, root):
	rank = dict()
	rank = {x:0 for x in G.keys()}
	rank[root] = 1
	PrintRank(rank)
	for k in range(20):
		tmp = {x:0 for x in G.keys()}
		for i, ri in G.items():
			for j, wij in ri.items():
				
				tmp[j] += alpha*rank[i] / len(ri)
				
				
				
		tmp[root] += 1 - alpha
		rank = tmp
		
		PrintRank(rank)
		
	return rank


def PersonalRankMatrixInverse(G, alpha, root):
	n = len(G)
	M = np.zeros((n,n))
	keys = G.keys()
	keysMap = dict()
	
	for i in range(n):
		keysMap[keys[i]] = i
	
	for i,items in G.items():
		for j, rij in items.items():
			u = keysMap[i]
			v = keysMap[j]
			M[u][v] = 1.0/len(items)
	
	
	r = np.zeros(n)
	r[keysMap[root]] = 1
	
	# print np.matrix(M )
	M = np.matrix(1 - alpha*M)
	r = np.matrix(r).T
	r = (1-alpha)*M.I*r
	
	rank = dict()
	for i in range(n):
		rank[keys[i]] = r[i]
		
	return rank
			
rank1 = PersonalRankRandomWalk(G, 0.6, 'A')
rank2 = PersonalRankMatrixInverse(G, 0.6, 'A')

print 'Random Walk'
PrintRank(rank1)
print 'Matrix Inverse'
PrintRank(rank2)