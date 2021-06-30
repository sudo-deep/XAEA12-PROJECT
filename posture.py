class CheckPosture:
    def __init__(self, scale=1, key_points={}):
        self.key_points = key_points
        self.scale = scale
        self.message = ""

    def set_key_points(self, key_points):
        self.key_points = key_points

    def get_key_points(self):
        return self.key_points

    def set_message(self, message):
        self.message = message

    def get_message(self):
        return self.message

    def set_scale(self, scale):
        self.scale = scale

    def get_scale(self):
        return self.scale

    def check_lean_forward(self):
        if self.key_points['Left Shoulder'].x != -1 and self.key_points['Left Ear'].x != -1 \
            and self.key_points['Left Shoulder'].x >= (self.key_points['Left Ear'].x +
                                                       (self.scale * 150)):
            return False
        if self.key_points['Right Shoulder'].x != -1 and self.key_points['Right Ear'].x != -1 \
            and self.key_points['Right Shoulder'].x >= (self.key_points['Right Ear'].x +
                                                        (self.scale * 160)):
            return False
        return True

    def check_slump(self):
        if self.key_points['Neck'].y != -1 and self.key_points['Nose'].y != -1 and (self.key_points['Nose'].y >= self.key_points['Neck'].y - (self.scale * 150)):
            return False
        return True

    def check_head_drop(self):
        if self.key_points['Left Eye'].y != -1 and self.key_points['Left Ear'].y != -1 and self.key_points['Left Eye'].y > (self.key_points['Left Ear'].y + (self.scale * 15)):
            return False
        if self.key_points['Right Eye'].y != -1 and self.key_points['Right Ear'].y != -1 and self.key_points['Right Eye'].y > (self.key_points['Right Ear'].y + (self.scale * 15)):
            return False
        return True

    def correct_posture(self):
        return all([self.check_slump(), self.check_head_drop(), self.check_lean_forward()])

    def build_message(self):
        current_message = ""
        if not self.check_head_drop():
            current_message += "Lift up your head!\n"
        if not self.check_lean_forward():
            current_message += "Lean back!\n"
        if not self.check_slump():
            current_message += "Sit up in your chair, you're slumping!\n"
        self.message = current_message
        return current_message
