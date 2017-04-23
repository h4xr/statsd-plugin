'''
File: StatsdPlugin.py
Description: Provides an interface for writing StatsD Plugins, collecting their
             data and reporting it to the StatsD Server
Author: Saurabh Badhwar <sbadhwar@redhat.com>
Date: 23/04/2017
'''
import inspect
import statsd
import threading
import time

class StatsdPlugin(object):
    '''
    StatsdPlugin provides a wrapper to the plugins through which they can
    register to a common interface to run and provide data.
    '''

    def __init__(self, host='127.0.0.1', port=8125, application_name='Satellite6',run_interval=1):
        '''
        Initialize the object and set the host and port where the statsd server
        is running. If no argument is provided, the client tries to connect to
        the statsd server running on localhost port 8125 by default.
        Params:
         - host: The host address of statsd server (Default:127.0.0.1)
         - port: The port on which the statsd server is listening (Default:8125)
         - application_name: The name of the application which will be appended
                             to the results before sending statistics
         - run_interval: The time interval in seconds which the registered
                         methods should run to collectd data (Default:1s)
        Returns: None
        '''

        self.host = host
        self.port = port
        self.application_name = application_name
        self.run_interval = run_interval

        #Maintain a flag to check if thread execution should take place or not
        self.run_threads = True

        #Initialize the metric method collection list
        self.registered_collectors = []

        #Initialize the result dictionary
        self.collected_metrics = {}

        #Initialize the runtime threads list
        self.runtime_thread = []

        #Connect to the Statsd Server
        self.statsd_client = statsd.StatsClient(self.host, self.port)

    def __get_collectors(self):
        '''
        Get the list of all the methods that are their in the derived class and
        which needs to be run.
        Params: None
        Returns: None
        '''

        print "Get collectors"
        for base_class in self.__class__.__bases__:
            for subclass in base_class.__subclasses__():
                for method in subclass.__dict__.values():
                    if callable(method):
                        self.registered_collectors.append(method)

    def __execute_collectors(self):
        '''
        Execute the collectors to collect the metrics
        Params: None
        Returns: None
        '''

        collector_threads = []
        for method in self.registered_collectors:
            self.runtime_thread.append(threading.Thread(
                target=method,
                args=(self,)
            ))

        #Run the threads
        for thread in self.runtime_thread:
            thread.start()

        #Wait for threads to exit
        for thread in self.runtime_thread:
            thread.join()

        self.send_metrics()

        self.runtime_thread[:] = [] #Clear the threads

    def send_metrics(self):
        '''
        Report the collected metrics to the StatsD server
        Params: None
        Returns: None
        '''

        for key in self.collected_metrics:
            metric_name = self.application_name + '.' + key
            self.statsd_client.gauge(metric_name, self.collected_metrics[key])

    def start(self):
        '''
        Start the Collector execution
        Params: None
        Returns: None
        '''

        self.__get_collectors()
        while self.run_threads:
            self.__execute_collectors()
            time.sleep(self.run_interval)

    def store_results(self, metric_name, metric_value):
        '''
        Stores the results in the result dictionary
        Params:
         - metric_name: The name of the metric to store
         - metric_value: The value of the metric
        Returns: None
        '''

        self.collected_metrics[metric_name] = metric_value

    def stop(self):
        '''
        Stops the collector execution by setting the run thread flag to False
        Params: None
        Returns: None
        '''

        self.run_threads = False
