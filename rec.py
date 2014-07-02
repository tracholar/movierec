# coding:gbk
import random
import math
from operator import *
import SimpleHTTPServer
import SocketServer
import re
import json

def ReadData(fname,split='::'):
	data = []
	
	for line in open(fname,'r'):
		uid, mid, r, t = line.split(split)
		t = int(t.replace('\n',''))
		data.append([uid,mid,int(r),t])
		
	return data

def ReadMovieInfo(fname):
	minfo = dict()
	for line in open(fname,'r'):
		line = line.replace('\n','')
		info = line.split('|')
		minfo[info[0]] = info
	
	return minfo
	
def SplitData(data,M,k,seed):
	test = dict()
	train = dict()
	random.seed(seed)
	for uid, mid, r, t in data:
		if random.randint(0,M)==k:
			if uid not in test:
				test[uid] = dict()
			test[uid][mid] = r
		else:
			if uid not in train:
				train[uid] = dict()
			train[uid][mid] = r
		
	return train,test
	
movieInfo = ReadMovieInfo('../data/u.item')
data = ReadData('../data/u.data','\t')
train, test = SplitData(data,4,0,0)
del data

print 'read data finished!'

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
	

def Recommend(user, train, W, K=3):
	rank = dict()
	interacted_items = train[user]
	
	for v, wuv in sorted(W[user].items(), key=itemgetter(1), reverse=True)[0:K]:
		for i, rvi in train[v].items():
			if i in interacted_items:
				continue
			if i not in rank:
				rank[i] = 0
			rank[i] += wuv*rvi
		
	return rank


W = UserSimilarity(train)

print 'caculate similarity finished!'




## 前端显示部分 

# request handler
class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def do_GET(self):
		m = re.match(r'/rec/([^/]+)',self.path)
		if m:
			print self.path
			uid = m.group(1)
			res = Recommend(uid,train,W)
			print res
			data = dict()
			data['movie'] = res
			mInfo = dict()
			for mid in res.keys():
				mInfo[mid] = movieInfo[mid]
				
			data['info'] = mInfo
			# print data
			html = json.dumps(data)
			
			self.protocol_version = 'HTTP/1.1'
			self.send_response(200,'OK')
			self.send_header('Content-Type','text/json')
			self.end_headers()
			self.wfile.write(html)
		else:
			return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
	
		
		
		
		
PORT = 8000
Handler = MyRequestHandler
server = SocketServer.TCPServer(('0.0.0.0',PORT),Handler)

print 'server at port ', PORT
server.serve_forever()


