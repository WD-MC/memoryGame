import os
import random

from pygame import *
import pygame.mixer

#initialisation de pygame
pygame.init()

#initialisation de pygame mixer
pygame.mixer.init()

# définition de la taille de l'ecran
width = 900
height = 700
screen = display.set_mode((width, height), RESIZABLE)

#ajout du titre à la fenêtre
display.set_caption('Memory Game')

#changer l'icône de la fenêtre
icon = pygame.image.load('images/caysti.JPG')
pygame.display.set_icon(icon)

#chargement du son du jeu
accueil_son = pygame.mixer.music.load("sons/bensound-clearday.mp3")

# chargment image de fond de l'écran d'accueil
fondaccueil = image.load('images/fond.png')
fondaccueil = fondaccueil.convert()
Fondaccueil = pygame.transform.scale(fondaccueil, (width, height))

# chargment image de fond barnière
entete = image.load('images/banière2.png')
entete = entete.convert()
Entete = pygame.transform.scale(entete, (width, 100))

# chargment image de fond nom du jeu
nomJeu = image.load('images/nomJeu1.png')
nomJeu = nomJeu.convert()
NomJeu = pygame.transform.scale(nomJeu, (width, 100))

# chargment image des étoiles
etoile = image.load('images/etoile.png')
etoile = etoile.convert_alpha()
Etoile = pygame.transform.scale(etoile, (50, 40))

etoilev = image.load('images/etoileOr.png')
etoilev = etoilev.convert_alpha()
Etoilev = pygame.transform.scale(etoilev, (50, 40))

# chargment image de fond de l'écran Win
fondvictoire = image.load('images/Victory.png')
fondvictoire = fondvictoire.convert()
Fondvictoire = pygame.transform.scale(fondvictoire, (width, height))

# caractéristique des cartes et de la grille de jeu
taille_carte = 110
nbreColone = 5
nbreligne = 4

padding =10
leftMargin = (width - ((taille_carte + padding) * nbreColone))//2
rigthMargin = leftMargin
topMargin = (height -((taille_carte + padding) * nbreligne))//2
bottomMargin = topMargin

#chargement des noms des images
memoryName=[]
for image in os.listdir('images/cartes1'):
    memoryName.append(image.split('.')[0])

#creer la copie pour avoir des cartes identiques
memoryNameCopy = memoryName.copy()
memoryName.extend(memoryNameCopy)
memoryNameCopy.clear()

# Mélange des cartes
random.shuffle(memoryName)

# chargement des images, des rectangles des images
memoryPicture = []
memoryPictureRect = []
visiblePicture = []
for item in memoryName:
    picture = pygame.image.load(f'images/cartes1/{item}.png')
    picture = pygame.transform.scale(picture,(taille_carte,taille_carte))
    memoryPicture.append(picture)
    pictureRect = picture.get_rect()
    memoryPictureRect.append(pictureRect)

# définir la position de chaque image et statut de chaque image
for i in range(len(memoryPictureRect)):
    memoryPictureRect[i][0] = leftMargin + ((taille_carte + padding) * (i % nbreColone))
    memoryPictureRect[i][1] = topMargin + ((taille_carte + padding) * (i % nbreligne))
    visiblePicture.append(False)

# Variables de jeu
carte_selectionnee = None
selection = None
cartes_trouvees = 0
nbreEssai = 0

# États de jeu
STATE_HOME = 0
STATE_GAME = 1
STATE_GAME_OVER = 2

# État de jeu initial
current_state = STATE_HOME

# boucle principale du jeu
game = True

#lecture du son
pygame.mixer.music.play(loops=-1)

nbreEtoileBlanche = 6
nbreEtoileOr = 0

# les fonctions du jeu
while game:
    #quitter le jeu
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            game = False

        #vérifie si une touche du clavier a été enfoncée
        if events.type == pygame.KEYDOWN:
            #Vérifie l'état
            if current_state == STATE_HOME:
                #vérifie si la touche enfoncée est enter
                if events.key == pygame.K_RETURN:
                    current_state = STATE_GAME
            elif current_state == STATE_GAME_OVER:
                #verifie si la touche enfoncée est R
                if events.key == pygame.K_r:
                    current_state = STATE_GAME
                    random.shuffle(memoryPicture)

        # vérifie si l'état du jeu est à STATE_HOME
        if current_state == STATE_HOME:
            #affiche l'image de l'écran d'accueil
            screen.blit(Fondaccueil, (0, 0))

        # vérifie si l'état du jeu est à STATE_GAME
        elif current_state == STATE_GAME:
            # ajouter une couleur a l'écran de fond
            screen.fill((255, 255, 255))
            #affiche l'image de la banière
            screen.blit(Entete, (0, 0))

            j = 500
            # affiche les étoiles Or
            for i in range(nbreEtoileOr):
                screen.blit(Etoilev, (j, 25))
                j += 60
            # affiche les étoiles blanches
            for i in range(nbreEtoileBlanche):
                screen.blit(Etoile, (j, 25))
                j += 60

            #affiche le nbre d'essai
            fonte = pygame.font.Font(None, 45)
            text = fonte.render(f'{nbreEssai}', True, (255, 255, 255))
            screen.blit(text, (290, 32))

            #affiche le nom du jeu
            screen.blit(NomJeu, (0, 600))

            # affiche les cartes et logique du jeu
            for i in range(len(memoryName)):
                #vérifie l'etat de visibilité de la carte
                if visiblePicture[i] == True:
                    #affiche la carte
                    screen.blit(memoryPicture[i], memoryPictureRect[i])
                else:
                    #affiche des rectangles
                    pygame.draw.rect(screen, (246, 205, 85),(memoryPictureRect[i][0], memoryPictureRect[i][1], taille_carte, taille_carte), border_radius=10)
                    # Calcul des coordonnées pour le rectangle de bordure
                    border_rect = pygame.Rect(memoryPictureRect[i])
                    border_rect.inflate_ip(-2, -2)  # Réduire la taille de 2 pixels de chaque côté
                    # Dessin du rectangle de bordure
                    pygame.draw.rect(screen, (255, 255, 255), border_rect, border_radius=10)

                # ajouter l'évènement clic et vérifie si toutes les cartes n'ont pas été découvert
                if events.type == pygame.MOUSEBUTTONDOWN and events.button == 1 and cartes_trouvees < len(memoryName):
                    # recupère chaque rectangle
                    for item in memoryPictureRect:
                        # vérifie si le clic est dans le rectangle de l'image
                        if item.collidepoint(events.pos):
                            #vérifie si la valeur de l'index de l'image est différent de true
                            if visiblePicture[memoryPictureRect.index(item)] != True:
                                #vérifie s'il n'ya pas de carte sélectionnee
                                if carte_selectionnee != None:
                                    #recupère l'index de la carte sélectionnée
                                    selection = memoryPictureRect.index(item)
                                    visiblePicture[selection] = True
                                else:
                                    #conserve l'index de la carte sélectionnée
                                    carte_selectionnee = memoryPictureRect.index(item)
                                    visiblePicture[carte_selectionnee] = True

            #met à jour l'etat du jeu
            for i in range(len(memoryName)):
                if visiblePicture[i] == True:
                    screen.blit(memoryPicture[i], memoryPictureRect[i])
                else:
                    pygame.draw.rect(screen, (246, 205, 85),(memoryPictureRect[i][0], memoryPictureRect[i][1], taille_carte, taille_carte), border_radius=10)
                    # Calcul des coordonnées pour le rectangle de bordure
                    border_rect = pygame.Rect(memoryPictureRect[i])
                    border_rect.inflate_ip(-2, -2)  # Réduire la taille de 2 pixels de chaque côté
                    # Dessin du rectangle de bordure
                    pygame.draw.rect(screen, (255, 255, 255), border_rect, border_radius=10)
            pygame.display.update()

            # vérifie si les variables de jeu sont vides
            if carte_selectionnee != None and selection != None:
                if memoryName[carte_selectionnee] == memoryName[selection]:
                    #compte le nombre de carte trouvée
                    cartes_trouvees +=2
                    #compte le nombre d'essai
                    nbreEssai +=2
                    #vide les variables de jeu
                    carte_selectionnee, selection = None, None
                else:
                    nbreEssai +=2
                    #après 5s
                    pygame.time.wait(500)
                    #retourne les cartes
                    visiblePicture[carte_selectionnee] = False
                    visiblePicture[selection] = False
                    carte_selectionnee, selection = None, None

            # Vérification si toutes les cartes ont été trouvées
            if cartes_trouvees == 20:
                pos_etoile = 500
                #réinitialise toutes les variables
                cartes_trouvees = 0
                carte_selectionnee, selection = None, None
                for i in range (len(memoryName)):
                    visiblePicture[i] = False
                #vérifie le nbre de coups
                if nbreEssai <= 30:
                    #ajoute toutes les étoiles
                    nbreEssai = 0
                    current_state = STATE_GAME_OVER
                elif nbreEssai >= 31 and nbreEssai <=50:
                    nbreEssai = 0
                    # ajoute 4 les étoiles
                    nbreEtoileOr = 4
                    nbreEtoileBlanche = 2
                    current_state = STATE_GAME
                elif nbreEssai >= 51 and nbreEssai <=70:
                    nbreEssai = 0
                    # ajoute 3 les étoiles
                    nbreEtoileOr = 3
                    nbreEtoileBlanche = 3
                elif nbreEssai >= 71 and nbreEssai <=90:
                    nbreEssai = 0
                    # ajoute 2 les étoiles
                    nbreEtoileOr = 2
                    nbreEtoileBlanche = 4
                    current_state = STATE_GAME
                elif nbreEssai >= 91 and nbreEssai <=120:
                    nbreEssai = 0
                    # ajoute 1 les étoiles
                    nbreEtoileOr = 1
                    nbreEtoileBlanche = 5
                    current_state = STATE_GAME
                else:
                    nbreEssai = 0
                    nbreEtoileOr = 0
                    nbreEtoileBlanche = 6
                    current_state = STATE_GAME


        elif current_state == STATE_GAME_OVER:
            # Afficher l'écran de fin de jeu
            screen.blit(Fondvictoire, (0, 0))
            nbreEssai = 0
            nbreEtoileOr = 0
            nbreEtoileBlanche = 6

    display.flip()

pygame.quit()

