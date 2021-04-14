
ENUM_FID_NAMES = {
	0: "bottom_right",
	1: "top_left",
	2: "BLOCK",
	3: "bottom_left"
}

CONS_R1 = 0 # MegArm distance off-screen to lower X bound

class Fiducial:
	def __init__(self, fid: int, x=-1, y=-1):
		""" Fiducial class. """
		self.fid, self.x, self.y = fid, x, y
		self.ftype = ""

class FiducialList:
	def __init__(self):
		""" List of active Fiducials. """
		self.fiducials = []

	def addFid(self, fd: Fiducial) -> bool:
		""" Add Fiducial to list.
		# RETURN: bool (Fiducial added successfully)
		"""
		if fd not in self.fiducials:
			self.fiducials.append(fd)
			return True
		return False

	def removeFid(self, fd: Fiducial) -> bool:
		""" Remove Fiducial from list.
		RETURN: bool (Fiducial removed successfully)
		"""
		if fd in self.fiducials:
			self.fiducials.remove(fd)
			return True
		return False

	def ascTypes(self):
		""" Associate Fudicual ID with type. """
		for f in self.fiducials:
			if not f.ftype:
				f.ftype = ENUM_FID_NAMES[f.fid]

class MegArm:
	def __init__(self, fidlist: FiducialList):
		""" MegArm class. Refer to CONS_R1 for position. """
		self.fidlist, self.x, self.y = fidlist, 0, 0
