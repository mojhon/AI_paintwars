# Projet "robotique" IA&Jeux 2021
#
# Binome:
#  Prénom Nom: Ryane Mehdi Djari
#  Prénom Nom: Sunny Liu
import math
import random

count=0

def get_team_name():
    return "VROUM VROUM HASBULLA"
    
def suivre(robotId, sensors):

    translation = 1
    rotation = 0

    # blocage si suivi par ennemie 
    if sensors["sensor_back"]["isRobot"] == True and sensors["sensor_back"]["isSameTeam"] == False:
        return 0, 0
    
	#on fuit dans le cas où on est bloqué ou ralenti par un ennemi
    if (sensors["sensor_front"]["distance_to_robot"] < 1 or sensors["sensor_front_left"]["distance_to_robot"] < 1 or sensors["sensor_front_right"]["distance_to_robot"] < 1) and sensors["sensor_front"]["isSameTeam"] == False:
        return braitenberg_flee(robotId, sensors)

    # on fuit si on croise un allié
    
    # on prend une direction aleatoire pour couvrir le + de surface possible et eviter comportement repetee/cyclique
    if sensors["sensor_front"]["isRobot"] == True and sensors["sensor_front"]["isSameTeam"] == True:  # if allié devant
    	while rotation == 0:  #pour etre sur que le robot ne suit pas son camarade
    		rotation = random.uniform(-1, 1) 
    	return translation, rotation

    # if allié devant à gauche
    if sensors["sensor_front_left"]["isRobot"] == True and sensors["sensor_front_left"]["isSameTeam"] == True:
    	while rotation == 0:  # pour etre sur que le robot ne suit pas son camarade
    		rotation = random.uniform(-1, 1)
    	return translation, rotation

    # if allié devant à droite
    if sensors["sensor_front_right"]["isRobot"] == True and sensors["sensor_front_right"]["isSameTeam"] == True:
    	while rotation == 0:  # pour etre sur que le robot ne suit pas son camarade
    		rotation = random.uniform(-1, 1)
    	return translation, rotation

    # if allié est à gauche
    if sensors["sensor_left"]["isRobot"] == True and sensors["sensor_left"]["isSameTeam"] == True:
    	while rotation == 0:  # pour etre sur que le robot ne suit pas son camarade
    		rotation = random.uniform(-1, 1)
    	return translation, rotation

    # if allié est à droite
    if sensors["sensor_right"]["isRobot"] == True and sensors["sensor_right"]["isSameTeam"] == True:
    	while rotation == 0:  # pour etre sur que le robot ne suit pas son camarade
    		rotation = random.uniform(-1, 1)
    	return translation, rotation

    # on suit un ennemi si on le croise
    if sensors["sensor_front"]["isRobot"] or sensors["sensor_front_left"]["isRobot"] or sensors["sensor_front_right"]["isRobot"] or sensors["sensor_left"]["isRobot"] or sensors["sensor_right"]["isRobot"]:
        return braitenberg_loveBot(robotId, sensors)

    if sensors["sensor_front"]["distance"] < 0.5 or sensors["sensor_front_left"]["distance"] < 0.5 or sensors["sensor_front_right"]["distance"] < 0.5:
        if sensors["sensor_front"]["distance"] < 0.5 and sensors["sensor_front_left"]["distance"] < 1 and sensors["sensor_front_right"]["distance"] < 1:  # Bloqué devant
            rotation = 1
            return translation, rotation

        if sensors["sensor_front"]["distance"] < 0.5 and sensors["sensor_left"]["distance"]:
            rotation = 0.5
            return translation, rotation
        if sensors["sensor_front"]["distance"] < 0.5 and sensors["sensor_right"]["distance"]: 
            rotation = -0.5
            return translation, rotation

        if sensors["sensor_front"]["distance"] < 0.5 and sensors["sensor_left"]["distance"] == 1: 
            rotation = -0.5
            return translation, rotation
        if sensors["sensor_front"]["distance"] < 0.5 and sensors["sensor_right"]["distance"] == 1: 
            rotation = -0.5
            return translation, rotation

    return braitenberg_avoider(robotId, sensors)
################################################################################
def braitenberg_avoider(robotId, sensors):

    translation = 1 * sensors["sensor_front"]["distance"]
    rotation = (-1) * sensors["sensor_front_left"]["distance"] + (1) * sensors["sensor_front_right"]["distance"] + (-1) * sensors["sensor_left"]["distance"] + sensors["sensor_right"]["distance"]

    translation = max(-1,min(translation,1))
    rotation = max(-1, min(rotation, 1))

    return translation, rotation
################################################################################
def mateAvoider(robotId, sensors):

    translation = 1
    rotation = 0
    
    # on prend une direction aleatoire pour couvrir le + de surface possible et eviter comportement repetee/cyclique
    if sensors["sensor_front"]["isRobot"] == True and sensors["sensor_front"]["isSameTeam"] == True:  # Si un allié est devant
        while(rotation==0):
        	rotation = random.uniform(-0.5, 0.5)
        return translation, rotation

    # if allié devant à gauche
    if sensors["sensor_front_left"]["isRobot"] == True and sensors["sensor_front_left"]["isSameTeam"] == True:
        while(rotation==0):
        	rotation = random.uniform(0, 1)
        return translation, rotation

    # if allié devant à droite
    if sensors["sensor_front_right"]["isRobot"] == True and sensors["sensor_front_right"]["isSameTeam"] == True:
        while(rotation==0):
        	rotation = random.uniform(-1, 0)
        return translation, rotation

    # if allié est à gauche
    if sensors["sensor_left"]["isRobot"] == True and sensors["sensor_left"]["isSameTeam"] == True:
        while(rotation==0):
        	rotation = random.uniform(0, 1)
        return translation, rotation

    # if allié est à droite
    if sensors["sensor_right"]["isRobot"] == True and sensors["sensor_right"]["isSameTeam"] == True:
        while(rotation==0):
        	rotation = random.uniform(-1, 0)
        return translation, rotation
    return braitenberg_flee(robotId, sensors)
################################################################################
def braitenberg_flee(robotId, sensors):

    translation = 1 * sensors["sensor_front"]["distance"]
    rotation = 0

    # Calcul de la rotation 
    rotation+= (1 - sensors["sensor_front"]["distance"])+ (1 - sensors["sensor_front_left"]["distance"])- (1 - sensors["sensor_front_right"]["distance"])

    # Rotation rapide si obstacle detecte
    if abs(rotation) > 0:
        translation = 0.5
        
    # limite les valeurs de sortie entre -1 et +1
    translation = max(-1, min(translation, 1))
    rotation= max(-1, min(rotation, 1))

    return translation, rotation
################################################################################
def braitenberg_loveBot(robotId, sensors):

    translation = 1
    rotation = 0

    if sensors["sensor_front"]["isRobot"] == True:  # if un ennemi devant
        return translation, rotation

    if sensors["sensor_front_left"]["isRobot"] == True:  # if ennemi devant à gauche
        rotation = -0.5
        return translation, rotation

    if sensors["sensor_front_right"]["isRobot"] == True:  # if ennemi devant à droite
        rotation = 0.5
        return translation, rotation

    if sensors["sensor_left"]["isRobot"] == True:  # if ennemi à gauche
        rotation = -1
        return translation, rotation

    if sensors["sensor_right"]["isRobot"] == True:  # if ennemi à droite
        rotation = 1
        return translation, rotation
################################################################################
def explorer(robotId, sensors): 

    translation = 1
    rotation = 0
    if robotId == 0:
    	rotation = -0.5
    elif robotId == 7:
    	rotation = 0.5
    # on bloque l'ennemi qui nous suit
    if sensors["sensor_back"]["isRobot"] == True and sensors["sensor_back"]["isSameTeam"] == False:
        return 0, 0

    # on fuit l'allié 
    if (sensors["sensor_front"]["isSameTeam"] and sensors["sensor_front"]["isRobot"]) or (sensors["sensor_front_left"]["isSameTeam"] and sensors["sensor_front_left"]["isRobot"]) or (sensors["sensor_front_right"]["isSameTeam"] and sensors["sensor_front_right"]["isRobot"]) or (sensors["sensor_left"]["isSameTeam"] and sensors["sensor_left"]["isRobot"]) or (sensors["sensor_right"]["isSameTeam"] and sensors["sensor_right"]["isRobot"]):
        return mateAvoider(robotId, sensors)

    # on suit l'ennemi qu'on croise
    if sensors["sensor_front"]["isRobot"] or sensors["sensor_front_left"]["isRobot"] or sensors["sensor_front_right"]["isRobot"] or sensors["sensor_left"]["isRobot"] or sensors["sensor_right"]["isRobot"]:
        return braitenberg_loveBot(robotId, sensors)

    #  on essaie d'entrer sur les chemins/couloirs libres

    if (not sensors["sensor_right"]["isRobot"]) and (sensors["sensor_right"]["distance"] != 1) and (sensors["sensor_front_right"]["distance"] > 0.8) and (not sensors["sensor_left"]["isRobot"]) and (sensors["sensor_left"]["distance"] != 1) and (sensors["sensor_front_left"]["distance"] > 0.8):
        #si on est sur un chemin fermé à droite et à gauche
        if sensors["sensor_front"]["distance"] == 1:
            if random.random() < 0.4:
                rotation = -0.4
            elif random.random() <= 0.3:
                rotation = 0
            else:
                rotation = 0.4
        if random.random() < 0.6:
            rotation = -0.4
        else:
            rotation = 0.4

        return translation, rotation
    # Chemin de gauche
    if (not sensors["sensor_left"]["isRobot"]) and (sensors["sensor_left"]["distance"] != 1) and (sensors["sensor_front_left"]["distance"] == 1):
        # Si un chemin est à gauche, on a 80% de chance de l'emprunter, sinon on se retourne aléatoirement.

        if random.random() < 0.8:
            rotation = -0.4
        else:
            rotation = random.uniform(0, 1)

        return translation, rotation

    # Chemin de droite
    if (not sensors["sensor_right"]["isRobot"]) and (sensors["sensor_right"]["distance"] != 1) and (sensors["sensor_front_right"]["distance"] == 1):

        if random.random() < 0.8:
            rotation = 0.4
        else:
            rotation = random.uniform(-1, 0)

        return translation, rotation

    # Si on est bloqué au mur on tourne

    if sensors["sensor_front"]["distance"] < 0.3 or sensors["sensor_front_left"]["distance"] < 0.3 or sensors["sensor_front_right"]["distance"] < 0.3:
        if sensors["sensor_front"]["distance"] < 0.5 and sensors["sensor_left"]["distance"] < 1 and sensors["sensor_right"]["distance"] < 1:  # Bloqué devant
            rotation = random.uniform(-1, 1)
            return translation, rotation
        if sensors["sensor_front_left"]["distance"] < sensors["sensor_front_right"]["distance"]:  # Bloqué à  gauche
            rotation = 1

        else:  # Bloqué à droite
            rotation = -1

        return translation, rotation

    return braitenberg_avoider(robotId, sensors)

def get_extended_sensors(sensors):
    for key in sensors:
        sensors[key]["distance_to_robot"] = 1.0
        sensors[key]["distance_to_wall"] = 1.0
        if sensors[key]["isRobot"] == True:
            sensors[key]["distance_to_robot"] = sensors[key]["distance"]
        else:
            sensors[key]["distance_to_wall"] = sensors[key]["distance"]
    return sensors

################################################################################
def step(robotId, sensors):
	global count
	#les robots 1 et 8 changent de comportement chaque 100 iterations
	#les robots 2 et 7 changent de comportement apres 50 puis 150 puis 50 et ainsi de suite
	#les robots 3 à 6 executent uniquement le randomizer
	sensors = get_extended_sensors(sensors)
	if robotId%8 == 1 or robotId%8 == 6 and (count % 100) < 50: #chaque 50 iterations
		return suivre(robotId,sensors)
	if robotId%8 >= 2 and robotId%8 <= 5 :
		return explorer(robotId,sensors)
	if(robotId%8 == 0):
		count += 1	
	if count % 200 < 100:#chaque 100 
		return explorer(robotId,sensors)
	else:
		return suivre(robotId,sensors)

