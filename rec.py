# coding:utf-8
import random
import math
from operator import *
import SimpleHTTPServer
import SocketServer
import re
import json
from moviedata import *
from similarity import *
	
movieInfo = ReadMovieInfo('../data/u.item')
data = ReadData('../data/u.data','\t')
train, test = SplitData(data,4,0,0)
del data
print 'read data finished!'
	
W = UserSimilarity(train)
print 'caculate similarity finished!'


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






## 前端显示部分 

# request handler
class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def do_GET(self):
		m = re.match(r'/rec/([^/]+)',self.path)
		if m:
			# print self.path
			uid = m.group(1)
			res = Recommend(uid,train,W)
			# print res
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


