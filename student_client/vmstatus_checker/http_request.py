# -*- coding:utf-8 -*-

import argparse

import demjson
import requests


def get(url, data=None):
	respone = requests.get(url, params=data)
	return respone.json()


def post(url, data=None):
	data = demjson.decode(data)
	respone = requests.post(url=url, json=data)
	return respone.json()


def put(url, data=None):
	data = demjson.decode(data)
	respone = requests.put(url, json=data)
	return respone.json()


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--get')
	parser.add_argument('--post')
	parser.add_argument('--put')
	parser.add_argument('--data')
	args = parser.parse_args()
	if args.get:
		respone = get(args.get, args.data)
	if args.post:
		respone = post(args.post, args.data)
	if args.put:
		respone = put(args.put, args.data)
	print respone['message'].decode("utf-8")
