import serial, struct

class DTAFrame:
    def __init__(self, mapping, values):
        self.values = values
        self.mapping = mapping
        self.keys = [i[0] for i in mapping]
    
    def getValues(self):
        return self.values
    
    def getValue(self, key):
        idx = self.keys.index(key)
        return self.values[idx]
    
    def getMapping(self):
        return self.mapping
    
    def __str__(self):
        res = ""
        for i in range(len(self.values)):
            res += "{0:>18s}: {1:5d}\t".format(self.mapping[i][1], self.values[i])
        return res

class DTAFrameParser:
    def __init__(self):
        self.mapping = {
             0x2000: [("rpm","RPM"),                 ("tps", "TPS %"),            ("wt", "Water Temp C"),       ("at", "Air Temperature C")],
             0x2001: [("map","MAP Kpa"),             ("lambda", "Lambda x 1000"), ("kph", "KPH x100"),          ("op", "Oil Pressure Kpa")],
             0x2002: [("fuelp","Fuel Pressure Kpa"), ("ot", "Oil Temperature C"), ("volts", "Volts x10"),       ("fclh", "Fuel Con. L/h x10")],
             0x2003: [("gear","Gear"),               ("adeg", "Advance Deg x10"), ("inj", "Injection ms x100"), ("fcl100", "Fuel Con. L/100km x10")],
             0x2004: [("ana1","Analog1 mV"),         ("ana2", "Analog2 mV"),      ("ana3", "Analog3 mV"),       ("ca", "Cam Advance x10")],
             0x2005: [("camtarg","Cam Target x10"),  ("cpwm", "Cam PWM x10"),     ("cre", "Crank Errors"),      ("cae", "Cam Errors")]}
    def parse(self, frame):
        id = frame.getMsgId()
        if id not in self.mapping:
            raise "Unknown id for DTA frame parser 0x{0:x}".format(id)
        map = self.mapping[id]
        values = struct.unpack("hhhh", frame.getBody());
        return DTAFrame(map, values)
        

class Frame:
    def __init__(self, head):
        self.head = head
        self.body = ""
        (tmp, self.msgId, self.bodyLength) = struct.unpack("IIB", self.head[1:])
        
    def setBody(self, body):
        self.body = body
        
    def getBody(self):
        return self.body
        
    def getBodyLength(self):
        return self.bodyLength
    
    def getMsgId(self):
        return self.msgId
    
    def __str__(self):
        return "0x{0:x} ".format(self.msgId) + "".join(map(lambda x: "{0:02x}".format(ord(x)), self.body))
    
class CanClient:
    def __init__(self, serial):
        self.serial = serial
        self.started = False
        
    def _nextMessage(self):
        b=""
        while b != "\xAA":
            b = self._readByte() 
        return b
           
    def _readByte(self):
        return self.serial.read()
    
    def readMessage(self):
        message = []
        if not self.started:
            message = self._nextMessage()
        message += self.serial.read(9)
        fr = Frame(message)
        bodyLength = fr.getBodyLength()
        body = self.serial.read(bodyLength)
        fr.setBody(body)
        return fr
        
"""   
ser = serial.Serial('/dev/ttyUSB0', 1228800)
try:
    client = CanClient(ser)
    p = DTAFrameParser()
    i = 0;
    while True:
        frame = client.readMessage()
        dtaFrame = p.parse(frame)
        print dtaFrame
        if frame.getMsgId() == 0x2000:
            print ""
        i = i+1
finally:
    ser.close()
    
    """
    
    