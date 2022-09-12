import time

def elapsed(func):
	start_at = time.time()
	func()
	end_at = time.time()
	duration = end_at - start_at
	print(f"duration: {duration*1000}ms")
