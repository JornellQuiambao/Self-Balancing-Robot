import event_checker

class HSM_TopLevel():

	def __init__(self):
		# Set initial state
		self.current_state = 'POWER_OFF'
		self.event = [None]
		# Initialize event checker
		Event_Checker = event_checker.Event_Checker(self.event)
		# Initialize SubHSMs here
		self.PowerOff = SubHSM_PowerOff()
		self.PowerOn = SubHSM_PowerOn()

	def run_HSM(self):
		# Following variable declarations are not practical but helpful for interfacing
		#states------------------------------------------
		POWER_OFF = 'POWER_OFF'
		POWER_ON = 'POWER_ON'
		
		#transitions-------------------------------------
		poweredOn = 'powered_on'
		poweredOff = 'powered_off'
		print(self.event)
		# State Machine
		if self.current_state == POWER_OFF:
			print('POWER_OFF')
			self.PowerOff.run_HSM(self.event)
			
			if (self.event[0] == poweredOn):
				self.current_state = POWER_ON
		# ------------------------------------------------
		elif self.current_state == POWER_ON:
			self.PowerOn.run_HSM(self.event)

			if (self.event[0] == poweredOff):
				self.current_state = POWER_OFF
		# -------------------------------------------------
		else:
			pass
		# Reset event to None
		self.event[0] = None

class SubHSM_PowerOff():

	def __init__(self):
		# Set initial state
		self.current_state = 'IDLE'
		# Init subHSMs here
		self.Charging = SubHSM_Charging()

	def run_HSM(self, event):
		# Following variable declarations are not practical but helpful for interfacing
		#states------------------------------------------
		IDLE = 'IDLE'
		CHARGING = 'CHARGING'
		
		#transitions-------------------------------------
		plugged_in = 'plugged_in'
		plugged_out = 'plugged_out'

		# State Machine
		if self.current_state == IDLE:
			print('IDLE')
			if (event[0] == plugged_in):
				self.current_state = CHARGING
		# ------------------------------------------------
		elif self.current_state == CHARGING:
			print('Charging')
			self.Charging.run_HSM(self.event)
			
			if (event[0] == plugged_out):
				self.current_state = IDLE
		# -------------------------------------------------
		else:
			pass
		# Reset event to None
		event[0] = None

class SubHSM_PowerOn():

	def __init__(self):
		# Set initial state
		self.current_state = 'FIND_TARGET'
		# Init subHSMs here
		self.FollowTarget = SubHSM_FollowTarget()

	def run_HSM(self, event):
		# Following variable declarations are not practical but helpful for interfacing
		#states------------------------------------------
		FIND_TARGET = 'FIND_TARGET'
		FOLLOW_TARGET = 'FOLLOW_TARGET'
		LEFT_BUMP_COLLISION = 'LEFT_BUMP_COLLISION'
		RIGHT_BUMP_COLLISION = 'RIGHT_BUMP_COLLISION'
		IDLE = 'IDLE'
		
		#transitions-------------------------------------
		target_found = 'target_found'
		target_lost = 'target_lost'
		left_bump = 'left_bump'
		right_bump = 'right_bump'
		correction = 'correction'
		proximity_close = 'proximity_close'
		proximity_far = 'proximity_far'

		# State Machine
		if self.current_state == FIND_TARGET:
			#print('IDLE')
			if (event[0] == target_found):
				self.current_state = FOLLOW_TARGET
		# ------------------------------------------------
		elif self.current_state == FOLLOW_TARGET:
			#print('Charging')
			self.FollowTarget.run_HSM(self.event)
			
			if (event[0] == target_lost):
				self.current_state = FIND_TARGET
			elif (event[0] == proximity_close):
				self.current_state = IDLE
			elif (event[0] == left_bump):
				self.current_state = LEFT_BUMP_COLLISION
			elif (event[0] == right_bump):
				self.current_state = RIGHT_BUMP_COLLISION			
		# -------------------------------------------------
		elif self.current_state == LEFT_BUMP_COLLISION:
			
			if (event[0] == correction):
				self.current_state = FIND_TARGET			
		# -------------------------------------------------
		elif self.current_state == RIGHT_BUMP_COLLISION:
			
			if (event[0] == correction):
				self.current_state = FIND_TARGET
		# -------------------------------------------------
		elif self.current_state == IDLE:
			if (event[0] == proximity_far):
				self.current_state = FOLLOW_TARGET
		# -------------------------------------------------
		else:
			pass
		# Reset event to None
		event[0] = None

class SubHSM_Charging():
	def __init__(self):
		# Set initial state
		self.current_state = 'BATTERY_CHARGING'
		# Init subHSMs here
	
	def run_HSM(self, event):
		#states------------------------------------------
		BATTERY_CHARGING = 'BATTERY_CHARGING'
		BATTERY_FULL = 'BATTERY_FULL'
		
		#transitions-------------------------------------
		power_full = 'power_full'
		
		#State Machine
		if self.current_state == BATTERY_CHARGING:
			if (event[0] == power_full):
				self.current_state = BATTERY_FULL
		# -------------------------------------------------
		else:
			pass
		# Reset event to None
		event[0] = None
		

class SubHSM_FollowTarget():
	def __init__(self):
		# Set initial state
		self.current_state = 'STANDARD_FOLLOW'
		# Init subHSMs here
	
	def run_HSM(self, event):
		#states------------------------------------------
		STANDARD_FOLLOW = 'STANDARD_FOLLOW'
		BEYOND_RIGHT = 'BEYOND_RIGHT'
		BEYOND_LEFT = 'BEYOND_LEFT'
		PING_DETECTION = 'PING_DETECTION'
		
		#transitions-------------------------------------
		too_far_left = 'too_far_left'
		return_from_left = 'return_from_left'
		too_far_right = 'too_far_right'
		return_from_right = 'too_far_right'
		sensor_detect = 'sensor_detect'
		path_correction = 'path_correction'
		
		#State Machine
		if self.current_state == STANDARD_FOLLOW:
			if (event[0] == too_far_left):
				self.current_state = BEYOND_LEFT
			elif (event[0] == too_far_right):
				self.current_state = BEYOND_RIGHT
			elif (event[0] == sensor_detect):
				self.current_state = PING_DETECTION
		# -------------------------------------------------
		elif self.current_state == BEYOND_LEFT:
			if (event[0] == return_from_left):
				self.current_state = STANDARD_FOLLOW
		# -------------------------------------------------
		elif self.current_state == BEYOND_RIGHT:
			if (event[0] == return_from_right):
				self.current_state = STANDARD_FOLLOW
		# -------------------------------------------------
		elif self.current_state == PING_DETECTION:
			if (event[0] == path_correction):
				self.current_state = STANDARD_FOLLOW
		# -------------------------------------------------
		else:
			pass
		# Reset event to None
		event[0] = None

# ##########################################################

# class PowerOnMachine(StateMachine):
# 	#states------------------------------------------
# 	findTarget = State('Find_Target', initial = True)
# 	followTarget = State('Follow_Target')
# 	idle = State('Idle')
# 	bumpCollision = State('Bump_Collision')
	
# 	#transitions-------------------------------------
# 	targetFound = findTarget.to(followTarget)
# 	targetLost = followTarget.to(findTarget)
# 	bump = followTarget.to(bumpCollision)
# 	correction = bumpCollision.to(findTarget)
# 	proximityClose = followTarget.to(idle)
# 	proximityFar = idle.to(followTarget)

# 	def run_HSM:

# ##########################################################
	
# class PowerOffMachine(StateMachine):
# 	#states------------------------------------------
# 	charging = State('Charging', initial = True)
# 	idle = State('Idle')

# 	#transitions-------------------------------------
# 	pluggedOut = charging.to(idle)
# 	pluggedIn = idle.to(charging)
# ##########################################################

# class FollowTargetMachine(StateMachine):
# 	#states------------------------------------------
# 	standardFollow = State('Standard_Follow', initial = True)
# 	beyondRight = State('Beyond_Right')
# 	beyondLeft = State('Beyond_Left')
# 	pingDetection = State('Ping_Detection')
	
# 	#transitions-------------------------------------
# 	tooFarLeft = standardFollow.to(beyondLeft)
# 	returnFromLeft = beyondLeft.to(standardFollow)
# 	tooFarRight = standardFollow.to(beyondRight)
# 	returnFromRight = beyondRight.to(standardFollow)
# 	sensorDetect = standardFollow.to(pingDetection)
# 	correction = pingDetection.to(standardFollow)
# ##########################################################

# class ChargingMachine(StateMachine):
# 	#states------------------------------------------
# 	batteryCharging = State('Battery_Charging', initial = True)
# 	batteryFull = State('Battery_Full')
	
# 	#transitions-------------------------------------
# 	powerFull = batteryCharging.to(batteryFull)
# ##########################################################

# #The BumpingMachine will be based on Diego's bumping algorithms from Mechatronics
# class BumpingMachine(StateMachine):
# 	#states------------------------------------------
	
# 	#transitions-------------------------------------
	
# ##########################################################


if __name__ == "__main__":
	HSM = HSM_TopLevel()
	while True:
		HSM.run_HSM()