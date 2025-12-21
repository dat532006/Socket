"original code provided for context"
# class VideoStream:
# 	def __init__(self, filename):
# 		self.filename = filename
# 		try:
# 			self.file = open(filename, 'rb')
# 		except:
# 			raise IOError
# 		self.frameNum = 0
		
# 	def nextFrame(self):
# 		"""Get next frame."""
# 		data = self.file.read(5) # Get the framelength from the first 5 bits
# 		if data: 
# 			framelength = int(data)
							
# 			# Read the current frame
# 			data = self.file.read(framelength)
# 			self.frameNum += 1
# 		return data
		
# 	def frameNbr(self):
# 		"""Get frame number."""
# 		return self.frameNum
	
"Videostream class to read frames from a video file"
import sys

class VideoStream:
    def __init__(self, filename):
        self.filename = filename
        try:
            self.file = open(filename, 'rb')
        except:
            raise IOError(f"Could not open file {filename}")
        self.frameNum = 0
        self.data = self.file.read()
        self.frames = []
        
        start = 0
        while True:
            # find start of JPEG frame (Magic bytes: FF D8)
            start_pos = self.data.find(b'\xff\xd8', start)
            if start_pos == -1:
                break
            
            # find end of JPEG frame (Magic bytes: FF D9)
            end_pos = self.data.find(b'\xff\xd9', start_pos)
            if end_pos == -1:
                break
            
            # cut out the frame
            frame = self.data[start_pos : end_pos + 2]
            self.frames.append(frame)
            
            # find next frame
            start = end_pos + 2

    def nextFrame(self):
        """Get next frame."""
        if self.frameNum < len(self.frames):
            frame = self.frames[self.frameNum]
            self.frameNum += 1
            return frame
        else:
            return None # No more frames available
        
    def frameNbr(self):
        """Get frame number."""
        return self.frameNum