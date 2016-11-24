import unittest

class TestDrone:

	def test_id(self,id):
		if self.id in id:
			print("ID already exists");

		else:
			print("ID successfully added");

	def test_simulation(self,simulation,grounded):
		if self.simulation == True:
			print("")

		elif (self.grounded == True):
				print("")

		else:
			print("")

	def check_connection_list(connection_list):
		for i in connection_list:
			