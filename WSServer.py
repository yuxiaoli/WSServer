#!/usr/bin/env python

# WS server example
import asyncio
import websockets

counter = 0

def consumer(message):
	# On receive
	print("client write:", message)
	global counter
	
	# Decompose data
	value = int(message)
	global counter
	counter = value
	
	
async def consumer_handler(websocket, path):
	async for message in websocket:
		consumer(message)

def producer():
	global counter
	counter = counter + 1
	return str(counter)
	
		
async def producer_handler(websocket, path):
	while True:
		message = producer()
		await websocket.send(message)
		await asyncio.sleep(0.1)

async def handler(websocket, path):
	consumer_task = asyncio.ensure_future(consumer_handler(websocket,path))
	producer_task = asyncio.ensure_future(producer_handler(websocket, path))
	
	done, pending = await asyncio.wait(
		[consumer_task, producer_task],
		return_when = asyncio.FIRST_COMPLETED
	)
	for task in pending:
		task.cancel()
		
async def server(websocket, path):
	while True:
		handler(websocket, path)
	
if __name__ == "__main__":
	start_server = websockets.serve(handler, "localhost", 8765)

	asyncio.get_event_loop().run_until_complete(start_server)
	asyncio.get_event_loop().run_forever()