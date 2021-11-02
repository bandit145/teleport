from dataclasses import dataclass

@dataclass
class Connection:
	remote_address: str
	remote_port: int
	local_address: str
	local_port: int
	time: int


	def __eq__(self, other):
		return hash(self) == hash(other)

	def __hash__(self):
		return hash(f'{self.remote_address}:{self.remote_port},{self.local_address}:{self.local_port}')
