# coding:gbk
import random
from operator import *


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

