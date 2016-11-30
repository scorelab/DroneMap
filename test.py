#Created by Imal thiunuwan using Intellij Idea

import unittest

class TestDrone:

    def test_id(self,id):
        if self.id in id:
            print("ID already exists")

        else:
            print("ID successfully added")

    def test_simulation(self,simulation,grounded):
        if self.simulation == True:
            print("simulation is OK")

        elif (self.grounded == True):
                print("")

        else:
            print("")

    def check_connection_list(connection_list):
        for i in connection_list:
            print i


    def main(self):
        print self.testid
        print self.test_simulation
        print self.check_connection_list