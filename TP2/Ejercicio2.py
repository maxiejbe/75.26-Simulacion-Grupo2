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
    def __init__(self, seconds,  p_new_request, p_resolve_request):
        self.state = []
        self.iterations = int(seconds * 1000/100)
        self.p_new_request = p_new_request
        self.p_resolve_request = p_resolve_request
        self.number_of_request = []

    def resolve_request(self):
        if(np.random.uniform(0, 1) < self.p_resolve_request):
            next_start_procesing = False
            for request in reversed(self.state):
                if(next_start_procesing):
                    request.start_processing()
                    break
                if(request.request_status == RequestStatus.Processing):
                    request.end_processing()
                    next_start_procesing = True

    def addNewRequest(self):
        if (np.random.uniform(0, 1) < self.p_new_request):
            request = Request()
            if (len([request for request in self.state if request.request_status == RequestStatus.Processing]) == 0):
                request.start_processing()
            self.state.insert(0, request)

    def get_new_request(self):
        return [request for request in self.state if request.request_status == RequestStatus.New]

    def get_processing_request(self):
        return [request for request in self.state if request.request_status == RequestStatus.Processing]

    def get_finalized_request(self):
        return [request for request in self.state if request.request_status == RequestStatus.Finalized]

    def printState(self):
        print('New ', str(self.get_new_request()), ' | Processing ', str(
            self.get_processing_request()), ' | Finalized ',  str(self.get_finalized_request()))

    def run_server(self):
        i = 0
        while i < self.iterations:
            self.resolve_request()
            self.addNewRequest()
            self.number_of_request.append(
                str(len(self.get_new_request()) + len(self.get_processing_request())))
            i += 1

    def plot_number_request(self):
        plt.close()
        x_axis = list(range(0, self.iterations))
        plt.plot(x_axis, self.number_of_request, color='blue')
        plt.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1)
        plt.show()


def main():
    seconds = 1000
    p_new_request = 1/40
    p_resolve_request = 1/30
    server = Server(seconds, p_new_request, p_resolve_request)
    server.run_server()
    server.plot_number_request()


if __name__ == "__main__":
    main()
