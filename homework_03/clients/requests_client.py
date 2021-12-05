import requests
import time
import statistics



URL = "http://127.0.0.1:8090/post"

def run_requests_client(counter = 1, pings = 100, returned_value = None):
    URL = "http://127.0.0.1:8090/post"
    results = []

    for n in range(counter):
        now = time.time()
        for num in range(pings):
            post = requests.post(URL, json={"num": str(num)})
            if post.ok:
                # print('response', post.json())
                continue
        
        delta = time.time() - now

        results.append(pings/delta)
        print('Client prosses is killed')
        
        if returned_value.value  == 0.0:
            returned_value.value = statistics.mean(results)
        pings *= 2
        print(results)
    return statistics.mean(results)

 
def main():
    print(run_requests_client())
    

if __name__ == '__main__':
   main()

