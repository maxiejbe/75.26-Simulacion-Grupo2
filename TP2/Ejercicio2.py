import numpy as np
import matplotlib.pyplot as plt
import math
import enum


class RequestStatus(enum.Enum):
    New = 1
    Processing = 2
    Finalized = 3


class Request:
    def __init__(self):
        self.request_status = RequestStatus.New

    def start_processing(self):
        self.request_status = RequestStatus.Processing

    def end_processing(self):
        self.request_status = RequestStatus.Finalized


class Server:
    def __init__(self):
        self.state = []

    def resolve_request(self):
        next_start_procesing = False
        for request in reversed(self.state):
            if(next_start_procesing):
                request.start_processing()
                break
            if(request.request_status == RequestStatus.Processing):
                request.end_processing()
                next_start_procesing = True

    def addNewRequest(self):
        request = Request()
        if (len([request for request in self.state if request.request_status == RequestStatus.Processing]) == 0):
            request.start_processing()
        self.state.insert(0, request)

    def getNewRequest(self):
        return [request for request in self.state if request.request_status == RequestStatus.New]

    def get_processing_request(self):
        return [request for request in self.state if request.request_status == RequestStatus.Processing]

    def getFinalizedRequest(self):
        return [request for request in self.state if request.request_status == RequestStatus.Finalized]

    def printState(self):
        print('New ', str(self.getNewRequest()), ' | Processing ', str(
            self.get_processing_request()), ' | Finalized ',  str(self.getFinalizedRequest()))


def plot_number_request(n, number_of_request):
    plt.close()
    x_axis = list(range(0, n))
    plt.plot(x_axis, number_of_request, color='blue', label='Requests')
    plt.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1)
    plt.show()


def run_simulation(seconds, p_new_request, p_resolve_request):
    server = Server()
    number_of_request = []
    n = seconds*1000/100
    i = 0
    while i < n:
        is_new_request = np.random.uniform(0, 1) < p_new_request
        is_resolve_request = np.random.uniform(0, 1) < p_resolve_request
        if (is_resolve_request):
            server.resolve_request()
        if (is_new_request):
            server.addNewRequest()
        i += 1
        number_of_request.append(
            str(len(server.getNewRequest()) + len(server.get_processing_request())))

    plot_number_request(int(n), number_of_request)


def main():
    seconds = 1000
    p_new_request = 1/40
    p_resolve_request = 1/30
    run_simulation(seconds, p_new_request, p_resolve_request)


if __name__ == "__main__":
    main()
