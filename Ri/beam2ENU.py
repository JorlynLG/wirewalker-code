import numpy as np

def beam2ENU(beams,heading,pitch,roll,beam1,beam2,beam3):
# % Transform.m is a Matlab script that shows how velocity data can be 
# % transformed between beam coordinates and ENU coordinates. Beam 
# % coordinates are defined as the velocity measured along the three 
# % beams of the instrument.
# % ENU coordinates are defined in an earth coordinate system, where
# % E represents the East-West component, N represents the North-South
# % component and U represents the Up-Down component.

# % Note that the transformation matrix must be recalculated every time
# % the orientation, heading, pitch or roll changes.

# % Transformation matrix for beam to xyz coordinates,
# % the values can be found from the header file that is generated in the
# % conversion of data to ASCII format
# % This example shows the transformation matrix for a standard Aquadopp head

# % AquadoppII - beams 1234
  T_beam2xyz1234 = np.matrix([[0.6782,0,-0.6782,0],
    [0,-1.1831,0,1.1831],
    [0.2644,0.3546,0.2644,0.3546]])


#% AquadoppII - beams 234
  T_beam2xyz234 = np.matrix([[0.5055,-1.3563,0.5055],
    [-1.1831,0,1.1831],
    [0.5517,0,0.5517]])

#% AquadoppII - beams 124
  T_beam2xyz124 = np.matrix([[1.3563,-0.5055,-0.5055],
    [0,-1.1831,1.1831],
    [0,0.5517,0.5517]])

#%T = T/4096;   % Scale the transformation matrix correctly to floating point numbers


#%Which transformation will it be?
  if beams == [1,2,3,4]:
    T_beam2xyz = T_beam2xyz1234
  elif beams == [2,3,4,0]:
    T_beam2xyz = T_beam2xyz234
  elif beams == [1,2,4,0]:
   T_beam2xyz = T_beam2xyz124
  else:
    print('Beam configuration not supported.')
    T_beam2xyz = NaN
  T_beam2xyz = T_beam2xyz.tolist()
  ReorientedT_beam2xyz = np.matrix([T_beam2xyz[2],[-x for x in T_beam2xyz[1]],T_beam2xyz[0]])
  T_org = ReorientedT_beam2xyz
#T_org = T_beam2xyz;
#%Not sure if the MMP is oriented in the same direction as this is assuming
#%but I will check to make sure that it is
 
  Vx = []
  Vy = []
  Vz = []
  east = []
  north = []
  up = []
#% heading, pitch and roll are the angles output in the data in degrees
  for i in range(len(heading)):
    xyz = T_org*np.matrix([[beam1[i]],[beam2[i]],[beam3[i]]])
    
    hh = np.pi*(heading[i]-90)/180
    pp = np.pi*pitch[i]/180

    rr = np.pi*roll[i]/180
#    % Make heading matrix
    H = np.matrix([[np.cos(hh),np.sin(hh), 0],
      [-np.sin(hh),np.cos(hh), 0],
      [0, 0, 1]])
    
#    % Make tilt matrix
    P = np.matrix([[np.cos(pp), -np.sin(pp)*np.sin(rr), -np.cos(rr)*np.sin(pp)],
      [0,np.cos(rr),-np.sin(rr)],
      [np.sin(pp), np.sin(rr)*np.cos(pp), np.cos(pp)*np.cos(rr)]])
#    %Create ENU
    xyz2enu = H*P
    ENU = xyz2enu * xyz
    east.append(ENU.item(0))
    north.append(ENU.item(1))
    up.append(ENU.item(2))

  return [east,north,up]