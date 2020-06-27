import numpy as np
import matplotlib.pyplot as plt
import math


class Request:
    def __init__(self):
        self.request_status = 'New'

    def startProcessing(self):
        self.request_status = 'Processing'

    def endProcessing(self):
        self.request_status = 'Finalized'


class Server:
    def __init__(self):
        self.state = []

    def resolveRequest(self):
        next_start_procesing = False
        for request in reversed(self.state):
            if(next_start_procesing):
                request.startProcessing()
                break
            if(request.request_status == 'Processing'):
                request.endProcessing()
                next_start_procesing = True

    def addNewRequest(self):
        request = Request()
        if (len([request for request in self.state if request.request_status == 'Processing']) == 0):
            request.startProcessing()
        self.state.insert(0, request)

    def printState(self):
        news = len(
            [request for request in self.state if request.request_status == 'New'])
        processing = len(
            [request for request in self.state if request.request_status == 'Processing'])
        finalized = len(
            [request for request in self.state if request.request_status == 'Finalized'])

        print('New ', str(news), ' | Processing ', str(
            processing), ' | Finalized ',  str(finalized))


def run_simulation(seconds, p_new_request, p_resolve_request):
    server = Server()
    n = seconds*1000/100
    i = 0
    while i < n:
        is_new_request = np.random.uniform(0, 1) < p_new_request
        is_resolve_request = np.random.uniform(0, 1) < p_resolve_request
        if (is_resolve_request):
            server.resolveRequest()
        if (is_new_request):
            server.addNewRequest()
        i += 1
        server.printState()


def main():
    seconds = 1000
    p_new_request = 1/40
    p_resolve_request = 1/30
    run_simulation(seconds, p_new_request, p_resolve_request)


if __name__ == "__main__":
    main()
