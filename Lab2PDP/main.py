# This is a sample Python script.
import random
import time
from threading import Thread, Lock, Condition

queue = []
condition = Condition()
size=0
finished=False

class Producer(Thread):

    def generateVector(self, size):
        vect = []
        for i in range(size):
            vect.append(random.randint(1, 20))
        return vect
        #i=random.randint(0,20)
        #j=random.randint(0,20)
        #return [i,j]

    def run(self):

        vector1 = self.generateVector(size)
        vector2 = self.generateVector(size)

        #vector1=self.generateVector()
        #vector2=self.generateVector()

        print(vector1, vector2)
        global queue

        for i in range(len(vector1)):
            prod = vector1[i] * vector2[i]
            condition.acquire()

            queue.append(prod)
            print("Product added:", prod)
            condition.notify()
            condition.release()

            time.sleep(random.random())
        global finished
        #finished=True

class Consumer(Thread):
    def run(self):
        sum = 0
        global queue
        i=0
        while i<size:
            condition.acquire()

            if not queue:
                print("Queue empty, waiting for product")
                condition.wait()
                print("Something was added to queue")
            prod = queue.pop()

            sum = sum + prod

            condition.release()
            print("Sum=", sum)
            i+=1

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    size = int(input("Size="))
    consumer = Consumer()
    producer = Producer()
    consumer.start()
    producer.start()
