import pygame, math, random, sys, copy
from pygame.locals import *


pygame.init()
#------------------- universal setup ---------------------------
#------------ color setup ---------------
BLACK = (0,0,0)
GRAY = (128,128,128)
WHITE = (255,255,255)
RED = (255,0,0)
DARKRED = (150,0,0)
GREEN = (0,255,0)
DARKGREEN = (0,150,0)
BLUE = (0,0,255)
DARKBLUE = (0,0,150)
YELLOW = (255,255,0)
DARKYELLOW = (150,150,0)
ROCKCOLOR = (139,125,107)
HOUSECOLOR = (219,111,111)
RIVERCOLOR = (0,255,255)
LANDMINECOLOR = (165,42,42)
INFOCOLOR = (182,82,235)

#------------ window setup ---------------
windowSize = [1120,700] # size of the window
screen = pygame.display.set_mode(windowSize)
FPS = 100
clock = pygame.time.Clock()

#---------- minimap configuration ------------
cornerpos = [0,0]
minimapWidth = 250
minimapHeight = 250
bigmapWidth = 1500
bigmapHeight = 1500
scrollstepx = scrollstepy = 4
margin = 30 # for text drawing

#---------- set up names and size of all the images that I will use ------------
imageSize = 200 # size of the tank body and turret images
HT_body = "C:\Users\EPZY\Desktop\\15-112 term project\
\World of Tanks_main file\\HT_body_1.png"
HT_turret = "C:\Users\EPZY\Desktop\\15-112 term project\
\World of Tanks_main file\\HT_turret_1.png"
HT_turret_recoil = "C:\Users\EPZY\Desktop\\15-112 term project\
\World of Tanks_main file\\HT_turret_2.png"
wallpaper_1="C:\Users\EPZY\Desktop\\15-112 term project\
\World of Tanks_main file\\wallpaper_tiger.png"
wallpaper_2="C:\Users\EPZY\Desktop\\15-112 term project\
\World of Tanks_main file\\wallpaper_tiger_2.png"
wallpaper_3="C:\Users\EPZY\Desktop\\15-112 term project\
\World of Tanks_main file\\wallpaper_tiger_3.png"
wallpaper_4="C:\Users\EPZY\Desktop\\15-112 term project\
\World of Tanks_main file\\wallpaper_4.png"
help_1="C:\Users\EPZY\Desktop\\15-112 term project\
\World of Tanks_main file\\help_1.png"
help_2="C:\Users\EPZY\Desktop\\15-112 term project\
\World of Tanks_main file\\help_2.png"
pause="C:\Users\EPZY\Desktop\\15-112 term project\
\World of Tanks_main file\\pause_2.png"
battlemap_1 = "C:\Users\EPZY\Desktop\\15-112 term project\
\World of Tanks_main file\\Malinovka.png"
battlemap_2 = "C:\Users\EPZY\Desktop\\15-112 term project\
\World of Tanks_main file\\Erlenberg.png"
battlemap_3 = "C:\Users\EPZY\Desktop\\15-112 term project\
\World of Tanks_main file\\Himmelsdorf.png"
battlemap_4 = "C:\Users\EPZY\Desktop\\15-112 term project\
\World of Tanks_main file\\Prohorovka.png"

#------------------- BGM and sound effects setup -----------------------------
pygame.mixer.init(44100, -16, 2, 2048)
BGM1 = "C:\Users\EPZY\Desktop\\15-112 term project\World of Tanks_main file\
\sound\World of Tanks OST - 36 - The Legend is Born.ogg"
BGM2 = "C:\Users\EPZY\Desktop\\15-112 term project\World of Tanks_main file\
\sound\World of Tanks OST - 23 - The Urge to Win.ogg"
BGM3 = "C:\Users\EPZY\Desktop\\15-112 term project\World of Tanks_main file\
\sound\World of Tanks OST - 35 - New Victories Await.ogg"
fireSound = pygame.mixer.Sound(
"C:\Users\EPZY\Desktop\\15-112 term project\World of Tanks_main file\sound\
\\fire sound.ogg")
buttonHoverSound = pygame.mixer.Sound(
"C:\Users\EPZY\Desktop\\15-112 term project\World of Tanks_main file\sound\
\\button_hover.ogg")
buttonClickSound = pygame.mixer.Sound(
"C:\Users\EPZY\Desktop\\15-112 term project\World of Tanks_main file\sound\
\\button_click.ogg")
enemyHitSound = pygame.mixer.Sound(
"C:\Users\EPZY\Desktop\\15-112 term project\World of Tanks_main file\sound\
\enemy-is-hit.ogg")
enemyDestroyedSound = pygame.mixer.Sound(
"C:\Users\EPZY\Desktop\\15-112 term project\World of Tanks_main file\sound\
\enemy-vehicle-destroyed.ogg")
playerHitSound = pygame.mixer.Sound(
"C:\Users\EPZY\Desktop\\15-112 term project\World of Tanks_main file\sound\
\critical-chime.ogg")
playerDestroyedSound = pygame.mixer.Sound(
"C:\Users\EPZY\Desktop\\15-112 term project\World of Tanks_main file\sound\
\\bail-out.ogg")

#------------------------------------------------------------------------------
#--------------------------- main game and maps -------------------------------
#------------------------------------------------------------------------------

def game_map_1():
    # start
    screen = pygame.display.set_mode(windowSize)
    pygame.display.set_caption("World of Tanks")
    clock = pygame.time.Clock()
    
    #--------------------- game intro screen --------------------------
    #global pause
    pause = False
    over = False
    # note that "map" is an pygame function and can not be used as a name for a variable
    bigmap = pygame.Surface((bigmapWidth,bigmapHeight))
    # ----------------- create bigmap -------------------
    battlemap = pygame.image.load(battlemap_1).convert()
    bigmap.blit(battlemap,[0,0])
    # ------- background is a subsurface of bigmap ----------
    background = pygame.Surface((screen.get_size()))
    backgroundrect = background.get_rect()
    background = bigmap.subsurface((Config.cornerpos[0],
                                    Config.cornerpos[1],
                                    windowSize[0],
                                    windowSize[1])) # take snapshot of bigmap
    # -----------------------------------
    background = background.convert()
    screen.blit(background, (0,0)) # delete all
    
    
    #------------- play background music --------------
    pygame.mixer.music.load(BGM2)
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1,0.0)
    
    done = False
    
    #------------  deal with all sprite groups before main loop  -------------
    allgroup = pygame.sprite.Group()
    shellgroup = pygame.sprite.Group()
    housegroup = pygame.sprite.Group()
    rockgroup = pygame.sprite.Group()
    landminegroup = pygame.sprite.Group()
    rivergroup = pygame.sprite.Group()
    infogroup = pygame.sprite.Group()
    enemyturretgroup = pygame.sprite.Group()
    enemyshellgroup = pygame.sprite.Group()
    reticlegroup = pygame.sprite.Group()
    
    Shell.groups = shellgroup, allgroup
    House.groups = housegroup, allgroup
    Rock.groups = rockgroup, allgroup
    Landmine.groups = landminegroup, allgroup
    River.groups = rivergroup, allgroup
    Info.groups = infogroup, allgroup
    EnemyTurret.groups = enemyturretgroup, allgroup
    EnemyShell.groups = enemyshellgroup, allgroup
    Reticle.groups = reticlegroup, allgroup
    Text.groups = allgroup
    Minimap.groups = allgroup
    
    player = Tank()
    turret = Turret()
    Minimap()
    Reticle()
    
    #------------ construct the map -----------------
    #----- house -----
    House([1000,250],50,50)
    House([1060,400],50,50)
    House([700,1150],50,50)
    House([560,1200],50,50)
    House([4800,1280],50,50)
    House([942,1392],50,50)
    #----- rock -----
    Rock([900,250],60,60)
    Rock([1050,400],60,60)
    Rock([1200,400],60,120)
    #----- river -----
    River([300,200],50,100)
    River([50,50],180,150)
    River([400,450],100,50)
    River([620,600],400,200)
    River([850,800],150,300)
    River([1050,1200],250,100)
    River([0,1100],120,250)
    River([100,1200],100,200)
    River([220,1300],100,230)
    #----- landmine -----
    Landmine([1148,690],50,50)
    Landmine([1266,804],50,50)
    Landmine([1252,1026],50,50)
    Landmine([1090,1104],50,50)
    #----- info -----
    Info([554,912],50,50)
    Info([22,1422],50,50)
    Info([22,1422],50,50)
    Info([326,1132],50,50)
    Info([1382,848],50,50)
    Info([1402,48],50,50)
    Info([470,1020],50,50)
    Info([656,856],50,50)
    #----- enemies -----
    EnemyTurret([162,644])
    EnemyTurret([200,500])
    EnemyTurret([794,1330])
    EnemyTurret([154,836])
    EnemyTurret([122,538])
    EnemyTurret([800,300])
    EnemyTurret([1252,238])
    
    while not done:
        milliseconds = clock.tick(FPS)  # milliseconds passed since last frame
        seconds = milliseconds / 1000.0 # seconds passed since last frame (float)
        pause = False
        over = False
        win = False
        
        if turret.cooldown > 0:
            turret.cooldown -= seconds
        else:
            turret.cooldown = 0 # avoid negative numbers
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        #------------- pause and repair ------------------
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = True
                    paused(pause)
                if event.key == pygame.K_r:
                    if player.repair > 0:
                        player.trackHit = False
                        if player.repair <= 0:
                            player.repair = 0
                        player.armor += 30
                        if player.armor >= player.maxarmor:
                            player.armor = player.maxarmor
                        player.repair -= 1
                    player.msg =  '''Armor: %i/%i  Track Status: %s  Repair Package Left: %i''' % (player.armor,player.maxarmor,"Operational",player.repair)
                    Text.book[player.number].changemsg(player.msg)
        #------------- tank stops when key is not pressed --------------
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    player.speed = 0
                if event.key == pygame.K_s:
                    player.speed = 0
        #------------- fire -------------
            if event.type == pygame.MOUSEBUTTONDOWN and turret.cooldown <= 0:
                mouseMotion_x, mouseMotion_y = pygame.mouse.get_pos()
                turret_cx,turret_cy=player.pos[0], player.pos[1]
                Shell([turret_cx,turret_cy],turret.angle)
                turret.cooldown = turret.cooldownTime # reset the cooldown time
                fireSound.play()
        # -------- scroll the big map ----------
        scrollx = 0
        scrolly = 0
        pressedkeys = pygame.key.get_pressed()
        # --- handle Cursor keys to scroll map ----
        if pressedkeys[pygame.K_LEFT]:
                scrollx -= scrollstepx
        if pressedkeys[pygame.K_RIGHT]:
                scrollx += scrollstepx
        if pressedkeys[pygame.K_UP]:
                scrolly -= scrollstepy
        if pressedkeys[pygame.K_DOWN]:
                scrolly += scrollstepy
        # -------- scroll the visible part of the map ------
        Config.cornerpos[0] += scrollx
        Config.cornerpos[1] += scrolly
        #--------- do not scroll out of bigmap edge -----
        if Config.cornerpos[0] < 0:
            Config.cornerpos[0] = 0
            scrollx = 0
        elif Config.cornerpos[0] > bigmapWidth - windowSize[0]:
            Config.cornerpos[0] = bigmapWidth - windowSize[0]
            scrollx = 0
        if Config.cornerpos[1] < 0:
            Config.cornerpos[1] = 0
            scrolly = 0
        elif Config.cornerpos[1] > bigmapHeight - windowSize[1]:
            Config.cornerpos[1] = bigmapHeight - windowSize[1]
            scrolly = 0
        #-----------------------------------------------
        #------------ check for collision --------------
        #-----------------------------------------------
        #------------ shell or enemyshell or player hit a house -----------
        for house in housegroup:
            crashedShell = pygame.sprite.spritecollide(
            house,shellgroup,False,pygame.sprite.collide_rect)
            crashedEnemyShell = pygame.sprite.spritecollide(
            house,enemyshellgroup,False,pygame.sprite.collide_rect)
            for shell in crashedShell:
                shell.kill()
            for enemyshell in crashedEnemyShell:
                enemyshell.kill()
            if crashedShell: # if crashedSHell is not an empty list, kill the house
                house.kill()
                del House.book[house.number]
            if crashedEnemyShell:
                house.kill()
                del House.book[house.number]
            if player.rectCollision.colliderect(house.rect):
                house.kill()
                del House.book[house.number]
        # ----------- shell or enemyshell or player hit a rock --------------
        for rock in rockgroup:
            crashedShell = pygame.sprite.spritecollide(
            rock,shellgroup,False,pygame.sprite.collide_rect)
            crashedEnemyShell = pygame.sprite.spritecollide(
            rock,enemyshellgroup,False,pygame.sprite.collide_rect)
            for shell in crashedShell:
                shell.kill()
            for enemyshell in crashedEnemyShell:
                enemyshell.kill()
            if player.rectCollision.colliderect(rock.rect):
                if abs(player.speed) <= player.maxspeed/4:
                    player.speed *= -1.5
                elif player.maxspeed/4 < abs(player.speed) <= player.maxspeed/2:
                    player.speed *= -0.1
                elif player.maxspeed/2 < abs(player.speed) <= player.maxspeed*3/4:
                    player.speed *= -0.5
                elif player.maxspeed*3/4 < abs(player.speed) <= player.maxspeed:
                    player.speed *= -0.3
        #--------------- player crossing river ---------------------
        for river in rivergroup:
            if player.rectCollision.colliderect(river.rect):
                if player.speed > 0:
                    player.speed = player.maxspeed/river.resistence
                elif player.speed < 0:
                    player.speed = player.maxspeed/river.resistence * (-1)
                else:
                    player.speed = 0
        #--------------- player collecting info ------------------
        for info in infogroup:
            if player.rectCollision.colliderect(info.rect):
                player.infoGet += 1
                info.kill()
                del Info.book[info.number]
        #--------------- player hit a landmine ---------------------
        for landmine in landminegroup:
            if player.rectCollision.colliderect(landmine.rect):
                player.trackHit = True
                player.speed = 0
                player.armor -= landmine.damage
                if player.armor <= 0:
                    player.armor = 0
                landmine.kill()
                player.msg =  '''Armor: %i/%i  Track Status: %s  Repair Package Left: %i''' % (player.armor,player.maxarmor,"Track hit! Need repair!",player.repair)
                Text.book[player.number].changemsg(player.msg)
        #--------------- shell hit an enemy --------------------
        for enemyturret in enemyturretgroup:
            crashedShell = pygame.sprite.spritecollide(
            enemyturret,shellgroup,False,pygame.sprite.collide_rect)
            for shell in crashedShell:
                shell.kill()
                enemyturret.armor -= shell.damage
                if enemyturret.armor > 0:
                    enemyHitSound.play()
                if enemyturret.armor <= 0:
                    enemyturret.kill()
                    del EnemyTurret.book[enemyturret.number]
                    enemyDestroyedSound.play()
        #--------------- enemy shell hit player or enemy -------------------
        for enemyshell in enemyshellgroup:
            if player.rectCollision.colliderect(enemyshell.rect):
                player.armor -= enemyshell.damage
                if player.armor <= 0:
                    player.armor = 0
                enemyshell.kill()
                if player.trackHit:
                    player.msg =  '''Armor: %i/%i  Track Status: %s  Repair Package Left: %i''' % (player.armor,player.maxarmor,"Track hit! Need repair!",player.repair)
                    Text.book[player.number].changemsg(player.msg)
                else:
                    player.msg =  '''Armor: %i/%i  Track Status: %s  Repair Package Left: %i''' % (player.armor,player.maxarmor,"Operational",player.repair)
                    Text.book[player.number].changemsg(player.msg)
                if player.armor > 0:
                    playerHitSound.play()
                else:
                    playerDestroyedSound.play()
                    player.alive = False
        #--------------- player and enemy collide with each other ------------
        for enemyturret in enemyturretgroup:
            if player.rectCollision.colliderect(enemyturret.rect):
                if abs(player.speed) <= player.maxspeed/4:
                    player.speed *= -1.5
                elif player.maxspeed/4 < abs(player.speed) <= player.maxspeed/2:
                    player.speed *= -1
                elif player.maxspeed/2 < abs(player.speed) <= player.maxspeed*3/4:
                    player.speed *= -0.5
                elif player.maxspeed*3/4 < abs(player.speed) <= player.maxspeed:
                    player.speed *= -0.3
                if abs(player.speed) >= player.maxspeed:
                    enemyturret.armor -= player.rammingDamage
                    player.armor -= player.rammingDamage
                    if player.armor <= 0:
                        player.armor = 0
                    if player.trackHit:
                        player.msg =  '''Armor: %i/%i  Track Status: %s  Repair Package Left: %i''' % (player.armor,player.maxarmor,"Track hit! Need repair!",player.repair)
                        Text.book[player.number].changemsg(player.msg)
                    else:
                        player.msg =  '''Armor: %i/%i  Track Status: %s  Repair Package Left: %i''' % (player.armor,player.maxarmor,"Operational",player.repair)
                        Text.book[player.number].changemsg(player.msg)
                    if player.armor > 0:
                        playerHitSound.play()
                    else:
                        playerDestroyedSound.play()
                        player.alive = False
                    if enemyturret.armor > 0:
                        enemyHitSound.play()
                    if enemyturret.armor <= 0:
                        enemyturret.kill()
                        del EnemyTurret.book[enemyturret.number]
                        enemyDestroyedSound.play()
                    
        #-------------- game over ------------------
        if not player.alive:
            over = True
            game_over(over)
        
        if (not Info.book) and (not EnemyTurret.book):
            win = True
            game_win(win)
            
        if scrollx == 0 and scrolly == 0:    # only necessery if there was no scrolling
            allgroup.clear(screen, background) # funny effect if you outcomment this line
        else:
            background = bigmap.subsurface((Config.cornerpos[0],
                                            Config.cornerpos[1],
                                            windowSize[0],
                                            windowSize[1])) # take snapshot of bigmap
            screen.blit(background, (0,0))
    #------------------ clear, draw, update, flip -----------------------
        screen.blit(background, (0,0))
        allgroup.clear(screen,background)
        allgroup.update(seconds)
        allgroup.draw(screen)
        
        
        player.update(seconds)
        turret.update(seconds)
        player.render(screen)
        turret.render(screen)
        pygame.display.flip()
        clock.tick(FPS)
        
def game_map_2():
    # start
    screen = pygame.display.set_mode(windowSize)
    pygame.display.set_caption("World of Tanks")
    clock = pygame.time.Clock()
    
    #--------------------- game intro screen --------------------------
    #global pause
    pause = False
    over = False
    # note that "map" is an pygame function and can not be used as a name for a variable
    bigmap = pygame.Surface((bigmapWidth,bigmapHeight))
    # ----------------- create bigmap -------------------
    battlemap = pygame.image.load(battlemap_2).convert()
    bigmap.blit(battlemap,[0,0])
    # ------- background is a subsurface of bigmap ----------
    background = pygame.Surface((screen.get_size()))
    backgroundrect = background.get_rect()
    background = bigmap.subsurface((Config.cornerpos[0],
                                    Config.cornerpos[1],
                                    windowSize[0],
                                    windowSize[1])) # take snapshot of bigmap
    # -----------------------------------
    background = background.convert()
    screen.blit(background, (0,0)) # delete all
    
    
    #------------- play background music --------------
    pygame.mixer.music.load(BGM2)
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1,0.0)
    
    done = False
    
    #------------  deal with all sprite groups before main loop  -------------
    allgroup = pygame.sprite.Group()
    shellgroup = pygame.sprite.Group()
    housegroup = pygame.sprite.Group()
    rockgroup = pygame.sprite.Group()
    landminegroup = pygame.sprite.Group()
    rivergroup = pygame.sprite.Group()
    infogroup = pygame.sprite.Group()
    enemyturretgroup = pygame.sprite.Group()
    enemyshellgroup = pygame.sprite.Group()
    reticlegroup = pygame.sprite.Group()
    
    Shell.groups = shellgroup, allgroup
    House.groups = housegroup, allgroup
    Rock.groups = rockgroup, allgroup
    Landmine.groups = landminegroup, allgroup
    River.groups = rivergroup, allgroup
    Info.groups = infogroup, allgroup
    EnemyTurret.groups = enemyturretgroup, allgroup
    EnemyShell.groups = enemyshellgroup, allgroup
    Reticle.groups = reticlegroup, allgroup
    Text.groups = allgroup
    Minimap.groups = allgroup
    
    player = Tank()
    turret = Turret()
    Minimap()
    Reticle()
    
    #------------ construct the map -----------------
    #----- house -----
    House([588,624],50,50)
    House([1060,400],50,50)
    House([700,1150],50,50)
    House([560,1200],50,50)
    House([4800,1280],50,50)
    House([942,1392],50,50)
    #----- rock -----
    Rock([900,250],60,60)
    Rock([1050,400],60,60)
    Rock([1200,400],60,120)
    #----- river -----
    River([618,4],240,1500)
    #----- landmine -----
    Landmine([1148,690],50,50)
    Landmine([1266,804],50,50)
    Landmine([1252,1026],50,50)
    Landmine([1090,1104],50,50)
    #----- info -----
    Info([66,92],50,50)
    Info([22,1422],50,50)
    Info([50,512],50,50)
    Info([80,1108],50,50)
    Info([1364,1364],50,50)
    Info([1308,990],50,50)
    Info([1292,634],50,50)
    Info([1368,104],50,50)
    #----- enemies -----
    EnemyTurret([1218,306])
    EnemyTurret([1210,638])
    EnemyTurret([1154,1074])
    EnemyTurret([1118,1302])
    EnemyTurret([296,1232])
    EnemyTurret([280,786])
    EnemyTurret([344,622])
    EnemyTurret([328,376])
    
    while not done:
        milliseconds = clock.tick(FPS)  # milliseconds passed since last frame
        seconds = milliseconds / 1000.0 # seconds passed since last frame (float)
        pause = False
        over = False
        win = False
        
        if turret.cooldown > 0:
            turret.cooldown -= seconds
        else:
            turret.cooldown = 0 # avoid negative numbers
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        #------------- pause and repair ------------------
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = True
                    paused(pause)
                if event.key == pygame.K_r:
                    if player.repair > 0:
                        player.trackHit = False
                        if player.repair <= 0:
                            player.repair = 0
                        player.armor += 30
                        if player.armor >= player.maxarmor:
                            player.armor = player.maxarmor
                        player.repair -= 1
                    player.msg =  '''Armor: %i/%i  Track Status: %s  Repair Package Left: %i''' % (player.armor,player.maxarmor,"Operational",player.repair)
                    Text.book[player.number].changemsg(player.msg)
        #------------- tank stops when key is not pressed --------------
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    player.speed = 0
                if event.key == pygame.K_s:
                    player.speed = 0
        #------------- fire -------------
            if event.type == pygame.MOUSEBUTTONDOWN and turret.cooldown <= 0:
                mouseMotion_x, mouseMotion_y = pygame.mouse.get_pos()
                turret_cx,turret_cy=player.pos[0], player.pos[1]
                Shell([turret_cx,turret_cy],turret.angle)
                turret.cooldown = turret.cooldownTime # reset the cooldown time
                fireSound.play()
        # -------- scroll the big map ----------
        scrollx = 0
        scrolly = 0
        pressedkeys = pygame.key.get_pressed()
        # --- handle Cursor keys to scroll map ----
        if pressedkeys[pygame.K_LEFT]:
                scrollx -= scrollstepx
        if pressedkeys[pygame.K_RIGHT]:
                scrollx += scrollstepx
        if pressedkeys[pygame.K_UP]:
                scrolly -= scrollstepy
        if pressedkeys[pygame.K_DOWN]:
                scrolly += scrollstepy
        # -------- scroll the visible part of the map ------
        Config.cornerpos[0] += scrollx
        Config.cornerpos[1] += scrolly
        #--------- do not scroll out of bigmap edge -----
        if Config.cornerpos[0] < 0:
            Config.cornerpos[0] = 0
            scrollx = 0
        elif Config.cornerpos[0] > bigmapWidth - windowSize[0]:
            Config.cornerpos[0] = bigmapWidth - windowSize[0]
            scrollx = 0
        if Config.cornerpos[1] < 0:
            Config.cornerpos[1] = 0
            scrolly = 0
        elif Config.cornerpos[1] > bigmapHeight - windowSize[1]:
            Config.cornerpos[1] = bigmapHeight - windowSize[1]
            scrolly = 0
        #-----------------------------------------------
        #------------ check for collision --------------
        #-----------------------------------------------
        #------------ shell or enemyshell or player hit a house -----------
        for house in housegroup:
            crashedShell = pygame.sprite.spritecollide(
            house,shellgroup,False,pygame.sprite.collide_rect)
            crashedEnemyShell = pygame.sprite.spritecollide(
            house,enemyshellgroup,False,pygame.sprite.collide_rect)
            for shell in crashedShell:
                shell.kill()
            for enemyshell in crashedEnemyShell:
                enemyshell.kill()
            if crashedShell: # if crashedSHell is not an empty list, kill the house
                house.kill()
                del House.book[house.number]
            if crashedEnemyShell:
                house.kill()
                del House.book[house.number]
            if player.rectCollision.colliderect(house.rect):
                house.kill()
                del House.book[house.number]
        # ----------- shell or enemyshell or player hit a rock --------------
        for rock in rockgroup:
            crashedShell = pygame.sprite.spritecollide(
            rock,shellgroup,False,pygame.sprite.collide_rect)
            crashedEnemyShell = pygame.sprite.spritecollide(
            rock,enemyshellgroup,False,pygame.sprite.collide_rect)
            for shell in crashedShell:
                shell.kill()
            for enemyshell in crashedEnemyShell:
                enemyshell.kill()
            if player.rectCollision.colliderect(rock.rect):
                if abs(player.speed) <= player.maxspeed/4:
                    player.speed *= -1.5
                elif player.maxspeed/4 < abs(player.speed) <= player.maxspeed/2:
                    player.speed *= -0.1
                elif player.maxspeed/2 < abs(player.speed) <= player.maxspeed*3/4:
                    player.speed *= -0.5
                elif player.maxspeed*3/4 < abs(player.speed) <= player.maxspeed:
                    player.speed *= -0.3
        #--------------- player crossing river ---------------------
        for river in rivergroup:
            if player.rectCollision.colliderect(river.rect):
                if player.speed > 0:
                    player.speed = player.maxspeed/river.resistence
                elif player.speed < 0:
                    player.speed = player.maxspeed/river.resistence * (-1)
                else:
                    player.speed = 0
        #--------------- player collecting info ------------------
        for info in infogroup:
            if player.rectCollision.colliderect(info.rect):
                player.infoGet += 1
                info.kill()
                del Info.book[info.number]
        #--------------- player hit a landmine ---------------------
        for landmine in landminegroup:
            if player.rectCollision.colliderect(landmine.rect):
                player.trackHit = True
                player.speed = 0
                player.armor -= landmine.damage
                if player.armor <= 0:
                    player.armor = 0
                landmine.kill()
                player.msg =  '''Armor: %i/%i  Track Status: %s  Repair Package Left: %i''' % (player.armor,player.maxarmor,"Track hit! Need repair!",player.repair)
                Text.book[player.number].changemsg(player.msg)
        #--------------- shell hit an enemy --------------------
        for enemyturret in enemyturretgroup:
            crashedShell = pygame.sprite.spritecollide(
            enemyturret,shellgroup,False,pygame.sprite.collide_rect)
            for shell in crashedShell:
                shell.kill()
                enemyturret.armor -= shell.damage
                if enemyturret.armor > 0:
                    enemyHitSound.play()
                if enemyturret.armor <= 0:
                    enemyturret.kill()
                    del EnemyTurret.book[enemyturret.number]
                    enemyDestroyedSound.play()
        #--------------- enemy shell hit player or enemy -------------------
        for enemyshell in enemyshellgroup:
            if player.rectCollision.colliderect(enemyshell.rect):
                player.armor -= enemyshell.damage
                if player.armor <= 0:
                    player.armor = 0
                enemyshell.kill()
                if player.trackHit:
                    player.msg =  '''Armor: %i/%i  Track Status: %s  Repair Package Left: %i''' % (player.armor,player.maxarmor,"Track hit! Need repair!",player.repair)
                    Text.book[player.number].changemsg(player.msg)
                else:
                    player.msg =  '''Armor: %i/%i  Track Status: %s  Repair Package Left: %i''' % (player.armor,player.maxarmor,"Operational",player.repair)
                    Text.book[player.number].changemsg(player.msg)
                if player.armor > 0:
                    playerHitSound.play()
                else:
                    playerDestroyedSound.play()
                    player.alive = False
        #--------------- player and enemy collide with each other ------------
        for enemyturret in enemyturretgroup:
            if player.rectCollision.colliderect(enemyturret.rect):
                if abs(player.speed) <= player.maxspeed/4:
                    player.speed *= -1.5
                elif player.maxspeed/4 < abs(player.speed) <= player.maxspeed/2:
                    player.speed *= -1
                elif player.maxspeed/2 < abs(player.speed) <= player.maxspeed*3/4:
                    player.speed *= -0.5
                elif player.maxspeed*3/4 < abs(player.speed) <= player.maxspeed:
                    player.speed *= -0.3
                if abs(player.speed) >= player.maxspeed:
                    enemyturret.armor -= player.rammingDamage
                    player.armor -= player.rammingDamage
                    if player.armor <= 0:
                        player.armor = 0
                    if player.trackHit:
                        player.msg =  '''Armor: %i/%i  Track Status: %s  Repair Package Left: %i''' % (player.armor,player.maxarmor,"Track hit! Need repair!",player.repair)
                        Text.book[player.number].changemsg(player.msg)
                    else:
                        player.msg =  '''Armor: %i/%i  Track Status: %s  Repair Package Left: %i''' % (player.armor,player.maxarmor,"Operational",player.repair)
                        Text.book[player.number].changemsg(player.msg)
                    if player.armor > 0:
                        playerHitSound.play()
                    else:
                        playerDestroyedSound.play()
                        player.alive = False
                    if enemyturret.armor > 0:
                        enemyHitSound.play()
                    if enemyturret.armor <= 0:
                        enemyturret.kill()
                        del EnemyTurret.book[enemyturret.number]
                        enemyDestroyedSound.play()
                    
        #-------------- game over ------------------
        if not player.alive:
            over = True
            game_over(over)
        
        if (not Info.book) and (not EnemyTurret.book):
            win = True
            game_win(win)
            
        if scrollx == 0 and scrolly == 0:    # only necessery if there was no scrolling
            allgroup.clear(screen, background) # funny effect if you outcomment this line
        else:
            background = bigmap.subsurface((Config.cornerpos[0],
                                            Config.cornerpos[1],
                                            windowSize[0],
                                            windowSize[1])) # take snapshot of bigmap
            screen.blit(background, (0,0))
    #------------------ clear, draw, update, flip -----------------------
        screen.blit(background, (0,0))
        allgroup.clear(screen,background)
        allgroup.update(seconds)
        allgroup.draw(screen)
        
        
        player.update(seconds)
        turret.update(seconds)
        player.render(screen)
        turret.render(screen)
        pygame.display.flip()
        clock.tick(FPS)
        
def game_map_4():
    # start
    screen = pygame.display.set_mode(windowSize)
    pygame.display.set_caption("World of Tanks")
    clock = pygame.time.Clock()
    
    #--------------------- game intro screen --------------------------
    #global pause
    pause = False
    over = False
    # note that "map" is an pygame function and can not be used as a name for a variable
    bigmap = pygame.Surface((bigmapWidth,bigmapHeight))
    # ----------------- create bigmap -------------------
    battlemap = pygame.image.load(battlemap_4).convert()
    bigmap.blit(battlemap,[0,0])
    # ------- background is a subsurface of bigmap ----------
    background = pygame.Surface((screen.get_size()))
    backgroundrect = background.get_rect()
    background = bigmap.subsurface((Config.cornerpos[0],
                                    Config.cornerpos[1],
                                    windowSize[0],
                                    windowSize[1])) # take snapshot of bigmap
    # -----------------------------------
    background = background.convert()
    screen.blit(background, (0,0)) # delete all
    #------------- play background music --------------
    pygame.mixer.music.load(BGM2)
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1,0.0)
    
    done = False
    
    #------------  deal with all sprite groups before main loop  -------------
    allgroup = pygame.sprite.Group()
    shellgroup = pygame.sprite.Group()
    housegroup = pygame.sprite.Group()
    rockgroup = pygame.sprite.Group()
    landminegroup = pygame.sprite.Group()
    rivergroup = pygame.sprite.Group()
    infogroup = pygame.sprite.Group()
    enemyturretgroup = pygame.sprite.Group()
    enemyshellgroup = pygame.sprite.Group()
    reticlegroup = pygame.sprite.Group()
    
    Shell.groups = shellgroup, allgroup
    House.groups = housegroup, allgroup
    Rock.groups = rockgroup, allgroup
    Landmine.groups = landminegroup, allgroup
    River.groups = rivergroup, allgroup
    Info.groups = infogroup, allgroup
    EnemyTurret.groups = enemyturretgroup, allgroup
    EnemyShell.groups = enemyshellgroup, allgroup
    Reticle.groups = reticlegroup, allgroup
    Text.groups = allgroup
    Minimap.groups = allgroup
    
    player = Tank()
    turret = Turret()
    Minimap()
    Reticle()
    
    #------------ construct the map -----------------
    #----- house -----
    House([165,96],50,50)
    House([177,246],50,50)
    House([303,432],50,50)
    House([276,633],50,50)
    House([273,759],50,50)
    House([252,939],50,50)
    House([252,1092],50,50)
    House([318,1341],50,50)
    House([471,1344],50,50)
    House([465,1173],50,50)
    House([624,1065],50,50)
    House([621,1218],50,50)
    House([780,1167],50,50)
    House([870,1035],50,50)
    #----- rock -----
    Rock([816,330],75,213)
    Rock([807,669],100,350)
    Rock([918,1206],100,350)
    #----------- river -----------
    River([972,6],135,303)
    River([1203,396],291,102)
    River([1131,846],338,387)
    #----- landmine -----
    Landmine([549,1296],50,50)
    Landmine([1110,1059],50,50)
    Landmine([690,525],50,50)
    Landmine([366,480],50,50)
    Landmine([681,903],50,50)
    Landmine([987,120],50,50)
    #----- info -----
    Info([1140,75],50,50)
    Info([1281,81],50,50)
    Info([1212,204],50,50)
    Info([1395,249],50,50)
    Info([1248,810],50,50)
    Info([1335,933],50,50)
    Info([1377,1162],50,50)
    Info([1359,1389],50,50)
    #----- enemies -----
    EnemyTurret([429,549])
    EnemyTurret([492,1137])
    EnemyTurret([1139,1344])
    EnemyTurret([1116,1173])
    EnemyTurret([1194,687])
    #EnemyTurret([936,513])
    #EnemyTurret([828,150])
    
    while not done:
        milliseconds = clock.tick(FPS)  # milliseconds passed since last frame
        seconds = milliseconds / 1000.0 # seconds passed since last frame (float)
        pause = False
        over = False
        win = False
        
        if turret.cooldown > 0:
            turret.cooldown -= seconds
        else:
            turret.cooldown = 0 # avoid negative numbers
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        #------------- pause and repair ------------------
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = True
                    paused(pause)
                if event.key == pygame.K_r:
                    if player.repair > 0:
                        player.trackHit = False
                        if player.repair <= 0:
                            player.repair = 0
                        player.armor += 30
                        if player.armor >= player.maxarmor:
                            player.armor = player.maxarmor
                        player.repair -= 1
                    player.msg =  '''Armor: %i/%i  Track Status: %s  Repair Package Left: %i''' % (player.armor,player.maxarmor,"Operational",player.repair)
                    Text.book[player.number].changemsg(player.msg)
        #------------- tank stops when key is not pressed --------------
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    player.speed = 0
                if event.key == pygame.K_s:
                    player.speed = 0
        #------------- fire -------------
            if event.type == pygame.MOUSEBUTTONDOWN and turret.cooldown <= 0:
                mouseMotion_x, mouseMotion_y = pygame.mouse.get_pos()
                turret_cx,turret_cy=player.pos[0], player.pos[1]
                Shell([turret_cx,turret_cy],turret.angle)
                turret.cooldown = turret.cooldownTime # reset the cooldown time
                fireSound.play()
        # -------- scroll the big map ----------
        scrollx = 0
        scrolly = 0
        pressedkeys = pygame.key.get_pressed()
        # --- handle Cursor keys to scroll map ----
        if pressedkeys[pygame.K_LEFT]:
                scrollx -= scrollstepx
        if pressedkeys[pygame.K_RIGHT]:
                scrollx += scrollstepx
        if pressedkeys[pygame.K_UP]:
                scrolly -= scrollstepy
        if pressedkeys[pygame.K_DOWN]:
                scrolly += scrollstepy
        # -------- scroll the visible part of the map ------
        Config.cornerpos[0] += scrollx
        Config.cornerpos[1] += scrolly
        #--------- do not scroll out of bigmap edge -----
        if Config.cornerpos[0] < 0:
            Config.cornerpos[0] = 0
            scrollx = 0
        elif Config.cornerpos[0] > bigmapWidth - windowSize[0]:
            Config.cornerpos[0] = bigmapWidth - windowSize[0]
            scrollx = 0
        if Config.cornerpos[1] < 0:
            Config.cornerpos[1] = 0
            scrolly = 0
        elif Config.cornerpos[1] > bigmapHeight - windowSize[1]:
            Config.cornerpos[1] = bigmapHeight - windowSize[1]
            scrolly = 0
        #-----------------------------------------------
        #------------ check for collision --------------
        #-----------------------------------------------
        #------------ shell or enemyshell or player hit a house -----------
        for house in housegroup:
            crashedShell = pygame.sprite.spritecollide(
            house,shellgroup,False,pygame.sprite.collide_rect)
            crashedEnemyShell = pygame.sprite.spritecollide(
            house,enemyshellgroup,False,pygame.sprite.collide_rect)
            for shell in crashedShell:
                shell.kill()
            for enemyshell in crashedEnemyShell:
                enemyshell.kill()
            if crashedShell: # if crashedSHell is not an empty list, kill the house
                house.kill()
                del House.book[house.number]
            if crashedEnemyShell:
                house.kill()
                del House.book[house.number]
            if player.rectCollision.colliderect(house.rect):
                house.kill()
                del House.book[house.number]
        # ----------- shell or enemyshell or player hit a rock --------------
        for rock in rockgroup:
            crashedShell = pygame.sprite.spritecollide(
            rock,shellgroup,False,pygame.sprite.collide_rect)
            crashedEnemyShell = pygame.sprite.spritecollide(
            rock,enemyshellgroup,False,pygame.sprite.collide_rect)
            for shell in crashedShell:
                shell.kill()
            for enemyshell in crashedEnemyShell:
                enemyshell.kill()
            if player.rectCollision.colliderect(rock.rect):
                if abs(player.speed) <= player.maxspeed/4:
                    player.speed *= -1.5
                elif player.maxspeed/4 < abs(player.speed) <= player.maxspeed/2:
                    player.speed *= -0.1
                elif player.maxspeed/2 < abs(player.speed) <= player.maxspeed*3/4:
                    player.speed *= -0.5
                elif player.maxspeed*3/4 < abs(player.speed) <= player.maxspeed:
                    player.speed *= -0.3
        #--------------- player crossing river ---------------------
        for river in rivergroup:
            if player.rectCollision.colliderect(river.rect):
                if player.speed > 0:
                    player.speed = player.maxspeed/river.resistence
                elif player.speed < 0:
                    player.speed = player.maxspeed/river.resistence * (-1)
                else:
                    player.speed = 0
        #--------------- player collecting info ------------------
        for info in infogroup:
            if player.rectCollision.colliderect(info.rect):
                player.infoGet += 1
                info.kill()
                del Info.book[info.number]
        #--------------- player hit a landmine ---------------------
        for landmine in landminegroup:
            if player.rectCollision.colliderect(landmine.rect):
                player.trackHit = True
                player.speed = 0
                player.armor -= landmine.damage
                if player.armor <= 0:
                    player.armor = 0
                landmine.kill()
                player.msg =  '''Armor: %i/%i  Track Status: %s  Repair Package Left: %i''' % (player.armor,player.maxarmor,"Track hit! Need repair!",player.repair)
                Text.book[player.number].changemsg(player.msg)
        #--------------- shell hit an enemy --------------------
        for enemyturret in enemyturretgroup:
            crashedShell = pygame.sprite.spritecollide(
            enemyturret,shellgroup,False,pygame.sprite.collide_rect)
            for shell in crashedShell:
                shell.kill()
                enemyturret.armor -= shell.damage
                if enemyturret.armor > 0:
                    enemyHitSound.play()
                if enemyturret.armor <= 0:
                    enemyturret.kill()
                    del EnemyTurret.book[enemyturret.number]
                    enemyDestroyedSound.play()
        #--------------- enemy shell hit player or enemy -------------------
        for enemyshell in enemyshellgroup:
            if player.rectCollision.colliderect(enemyshell.rect):
                player.armor -= enemyshell.damage
                if player.armor <= 0:
                    player.armor = 0
                enemyshell.kill()
                if player.trackHit:
                    player.msg =  '''Armor: %i/%i  Track Status: %s  Repair Package Left: %i''' % (player.armor,player.maxarmor,"Track hit! Need repair!",player.repair)
                    Text.book[player.number].changemsg(player.msg)
                else:
                    player.msg =  '''Armor: %i/%i  Track Status: %s  Repair Package Left: %i''' % (player.armor,player.maxarmor,"Operational",player.repair)
                    Text.book[player.number].changemsg(player.msg)
                if player.armor > 0:
                    playerHitSound.play()
                else:
                    playerDestroyedSound.play()
                    player.alive = False
        #--------------- player and enemy collide with each other ------------
        for enemyturret in enemyturretgroup:
            if player.rectCollision.colliderect(enemyturret.rect):
                if abs(player.speed) <= player.maxspeed/4:
                    player.speed *= -1.5
                elif player.maxspeed/4 < abs(player.speed) <= player.maxspeed/2:
                    player.speed *= -1
                elif player.maxspeed/2 < abs(player.speed) <= player.maxspeed*3/4:
                    player.speed *= -0.5
                elif player.maxspeed*3/4 < abs(player.speed) <= player.maxspeed:
                    player.speed *= -0.3
                if abs(player.speed) >= player.maxspeed:
                    enemyturret.armor -= player.rammingDamage
                    player.armor -= player.rammingDamage
                    if player.armor <= 0:
                        player.armor = 0
                    if player.trackHit:
                        player.msg =  '''Armor: %i/%i  Track Status: %s  Repair Package Left: %i''' % (player.armor,player.maxarmor,"Track hit! Need repair!",player.repair)
                        Text.book[player.number].changemsg(player.msg)
                    else:
                        player.msg =  '''Armor: %i/%i  Track Status: %s  Repair Package Left: %i''' % (player.armor,player.maxarmor,"Operational",player.repair)
                        Text.book[player.number].changemsg(player.msg)
                    if player.armor > 0:
                        playerHitSound.play()
                    else:
                        playerDestroyedSound.play()
                        player.alive = False
                    if enemyturret.armor > 0:
                        enemyHitSound.play()
                    if enemyturret.armor <= 0:
                        enemyturret.kill()
                        del EnemyTurret.book[enemyturret.number]
                        enemyDestroyedSound.play()
                    
        #-------------- game over ------------------
        if not player.alive:
            over = True
            game_over(over)
        
        if (not Info.book) and (not EnemyTurret.book):
            win = True
            game_win(win)
            
        if scrollx == 0 and scrolly == 0:    # only necessery if there was no scrolling
            allgroup.clear(screen, background) # funny effect if you outcomment this line
        else:
            background = bigmap.subsurface((Config.cornerpos[0],
                                            Config.cornerpos[1],
                                            windowSize[0],
                                            windowSize[1])) # take snapshot of bigmap
            screen.blit(background, (0,0))
    #------------------ clear, draw, update, flip -----------------------
        screen.blit(background, (0,0))
        allgroup.clear(screen,background)
        allgroup.update(seconds)
        allgroup.draw(screen)
        
        
        player.update(seconds)
        turret.update(seconds)
        player.render(screen)
        turret.render(screen)
        pygame.display.flip()
        clock.tick(FPS)
        
def game_map_3():
    # start
    screen = pygame.display.set_mode(windowSize)
    pygame.display.set_caption("World of Tanks")
    clock = pygame.time.Clock()
    
    #--------------------- game intro screen --------------------------
    #global pause
    pause = False
    over = False
    # note that "map" is an pygame function and can not be used as a name for a variable
    bigmap = pygame.Surface((bigmapWidth,bigmapHeight))
    # ----------------- create bigmap -------------------
    battlemap = pygame.image.load(battlemap_3).convert()
    bigmap.blit(battlemap,[0,0])
    # ------- background is a subsurface of bigmap ----------
    background = pygame.Surface((screen.get_size()))
    backgroundrect = background.get_rect()
    background = bigmap.subsurface((Config.cornerpos[0],
                                    Config.cornerpos[1],
                                    windowSize[0],
                                    windowSize[1])) # take snapshot of bigmap
    # -----------------------------------
    background = background.convert()
    screen.blit(background, (0,0)) # delete all
    
    
    #------------- play background music --------------
    pygame.mixer.music.load(BGM2)
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1,0.0)
    
    done = False
    
    #------------  deal with all sprite groups before main loop  -------------
    allgroup = pygame.sprite.Group()
    shellgroup = pygame.sprite.Group()
    housegroup = pygame.sprite.Group()
    rockgroup = pygame.sprite.Group()
    landminegroup = pygame.sprite.Group()
    rivergroup = pygame.sprite.Group()
    infogroup = pygame.sprite.Group()
    enemyturretgroup = pygame.sprite.Group()
    enemyshellgroup = pygame.sprite.Group()
    reticlegroup = pygame.sprite.Group()
    
    Shell.groups = shellgroup, allgroup
    House.groups = housegroup, allgroup
    Rock.groups = rockgroup, allgroup
    Landmine.groups = landminegroup, allgroup
    River.groups = rivergroup, allgroup
    Info.groups = infogroup, allgroup
    EnemyTurret.groups = enemyturretgroup, allgroup
    EnemyShell.groups = enemyshellgroup, allgroup
    Reticle.groups = reticlegroup, allgroup
    Text.groups = allgroup
    Minimap.groups = allgroup
    
    player = Tank()
    turret = Turret()
    Minimap()
    Reticle()
    
    #------------ construct the map -----------------
    #----- house -----
    House([165,96],50,50)
    House([177,246],50,50)
    House([303,432],50,50)
    House([276,633],50,50)
    House([273,759],50,50)
    House([252,939],50,50)
    House([252,1092],50,50)
    House([318,1341],50,50)
    House([471,1344],50,50)
    House([465,1173],50,50)
    House([624,1065],50,50)
    House([621,1218],50,50)
    House([780,1167],50,50)
    House([870,1035],50,50)
    #----- rock -----
    Rock([489,399],60,60)
    Rock([774,420],60,60)
    Rock([810,225],60,120)
    Rock([960,456],60,120)
    Rock([1029,282],60,120)
    #----- landmine -----
    Landmine([549,1296],50,50)
    Landmine([1110,1059],50,50)
    Landmine([690,525],50,50)
    Landmine([366,480],50,50)
    Landmine([681,903],50,50)
    Landmine([987,120],50,50)
    #----- info -----
    Info([486,699],50,50)
    Info([669,765],50,50)
    Info([876,771],50,50)
    Info([36,141],50,50)
    Info([48,1401],50,50)
    Info([702,99],50,50)
    Info([339,162],50,50)
    #----- enemies -----
    EnemyTurret([1005,1266])
    EnemyTurret([1311,1263])
    EnemyTurret([1173,792])
    EnemyTurret([1260,315])
    EnemyTurret([126,609])
    EnemyTurret([165,1035])
    
    while not done:
        milliseconds = clock.tick(FPS)  # milliseconds passed since last frame
        seconds = milliseconds / 1000.0 # seconds passed since last frame (float)
        pause = False
        over = False
        win = False
        
        if turret.cooldown > 0:
            turret.cooldown -= seconds
        else:
            turret.cooldown = 0 # avoid negative numbers
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        #------------- pause and repair ------------------
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = True
                    paused(pause)
                if event.key == pygame.K_r:
                    if player.repair > 0:
                        player.trackHit = False
                        if player.repair <= 0:
                            player.repair = 0
                        player.armor += 30
                        if player.armor >= player.maxarmor:
                            player.armor = player.maxarmor
                        player.repair -= 1
                    player.msg =  '''Armor: %i/%i  Track Status: %s  Repair Package Left: %i''' % (player.armor,player.maxarmor,"Operational",player.repair)
                    Text.book[player.number].changemsg(player.msg)
        #------------- tank stops when key is not pressed --------------
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    player.speed = 0
                if event.key == pygame.K_s:
                    player.speed = 0
        #------------- fire -------------
            if event.type == pygame.MOUSEBUTTONDOWN and turret.cooldown <= 0:
                mouseMotion_x, mouseMotion_y = pygame.mouse.get_pos()
                turret_cx,turret_cy=player.pos[0], player.pos[1]
                Shell([turret_cx,turret_cy],turret.angle)
                turret.cooldown = turret.cooldownTime # reset the cooldown time
                fireSound.play()
        # -------- scroll the big map ----------
        scrollx = 0
        scrolly = 0
        pressedkeys = pygame.key.get_pressed()
        # --- handle Cursor keys to scroll map ----
        if pressedkeys[pygame.K_LEFT]:
                scrollx -= scrollstepx
        if pressedkeys[pygame.K_RIGHT]:
                scrollx += scrollstepx
        if pressedkeys[pygame.K_UP]:
                scrolly -= scrollstepy
        if pressedkeys[pygame.K_DOWN]:
                scrolly += scrollstepy
        # -------- scroll the visible part of the map ------
        Config.cornerpos[0] += scrollx
        Config.cornerpos[1] += scrolly
        #--------- do not scroll out of bigmap edge -----
        if Config.cornerpos[0] < 0:
            Config.cornerpos[0] = 0
            scrollx = 0
        elif Config.cornerpos[0] > bigmapWidth - windowSize[0]:
            Config.cornerpos[0] = bigmapWidth - windowSize[0]
            scrollx = 0
        if Config.cornerpos[1] < 0:
            Config.cornerpos[1] = 0
            scrolly = 0
        elif Config.cornerpos[1] > bigmapHeight - windowSize[1]:
            Config.cornerpos[1] = bigmapHeight - windowSize[1]
            scrolly = 0
        #-----------------------------------------------
        #------------ check for collision --------------
        #-----------------------------------------------
        #------------ shell or enemyshell or player hit a house -----------
        for house in housegroup:
            crashedShell = pygame.sprite.spritecollide(
            house,shellgroup,False,pygame.sprite.collide_rect)
            crashedEnemyShell = pygame.sprite.spritecollide(
            house,enemyshellgroup,False,pygame.sprite.collide_rect)
            for shell in crashedShell:
                shell.kill()
            for enemyshell in crashedEnemyShell:
                enemyshell.kill()
            if crashedShell: # if crashedSHell is not an empty list, kill the house
                house.kill()
                del House.book[house.number]
            if crashedEnemyShell:
                house.kill()
                del House.book[house.number]
            if player.rectCollision.colliderect(house.rect):
                house.kill()
                del House.book[house.number]
        # ----------- shell or enemyshell or player hit a rock --------------
        for rock in rockgroup:
            crashedShell = pygame.sprite.spritecollide(
            rock,shellgroup,False,pygame.sprite.collide_rect)
            crashedEnemyShell = pygame.sprite.spritecollide(
            rock,enemyshellgroup,False,pygame.sprite.collide_rect)
            for shell in crashedShell:
                shell.kill()
            for enemyshell in crashedEnemyShell:
                enemyshell.kill()
            if player.rectCollision.colliderect(rock.rect):
                if abs(player.speed) <= player.maxspeed/4:
                    player.speed *= -1.5
                elif player.maxspeed/4 < abs(player.speed) <= player.maxspeed/2:
                    player.speed *= -0.1
                elif player.maxspeed/2 < abs(player.speed) <= player.maxspeed*3/4:
                    player.speed *= -0.5
                elif player.maxspeed*3/4 < abs(player.speed) <= player.maxspeed:
                    player.speed *= -0.3
        #--------------- player crossing river ---------------------
        for river in rivergroup:
            if player.rectCollision.colliderect(river.rect):
                if player.speed > 0:
                    player.speed = player.maxspeed/river.resistence
                elif player.speed < 0:
                    player.speed = player.maxspeed/river.resistence * (-1)
                else:
                    player.speed = 0
        #--------------- player collecting info ------------------
        for info in infogroup:
            if player.rectCollision.colliderect(info.rect):
                player.infoGet += 1
                info.kill()
                del Info.book[info.number]
        #--------------- player hit a landmine ---------------------
        for landmine in landminegroup:
            if player.rectCollision.colliderect(landmine.rect):
                player.trackHit = True
                player.speed = 0
                player.armor -= landmine.damage
                if player.armor <= 0:
                    player.armor = 0
                landmine.kill()
                player.msg =  '''Armor: %i/%i  Track Status: %s  Repair Package Left: %i''' % (player.armor,player.maxarmor,"Track hit! Need repair!",player.repair)
                Text.book[player.number].changemsg(player.msg)
        #--------------- shell hit an enemy --------------------
        for enemyturret in enemyturretgroup:
            crashedShell = pygame.sprite.spritecollide(
            enemyturret,shellgroup,False,pygame.sprite.collide_rect)
            for shell in crashedShell:
                shell.kill()
                enemyturret.armor -= shell.damage
                if enemyturret.armor > 0:
                    enemyHitSound.play()
                if enemyturret.armor <= 0:
                    enemyturret.kill()
                    del EnemyTurret.book[enemyturret.number]
                    enemyDestroyedSound.play()
        #--------------- enemy shell hit player or enemy -------------------
        for enemyshell in enemyshellgroup:
            if player.rectCollision.colliderect(enemyshell.rect):
                player.armor -= enemyshell.damage
                if player.armor <= 0:
                    player.armor = 0
                enemyshell.kill()
                if player.trackHit:
                    player.msg =  '''Armor: %i/%i  Track Status: %s  Repair Package Left: %i''' % (player.armor,player.maxarmor,"Track hit! Need repair!",player.repair)
                    Text.book[player.number].changemsg(player.msg)
                else:
                    player.msg =  '''Armor: %i/%i  Track Status: %s  Repair Package Left: %i''' % (player.armor,player.maxarmor,"Operational",player.repair)
                    Text.book[player.number].changemsg(player.msg)
                if player.armor > 0:
                    playerHitSound.play()
                else:
                    playerDestroyedSound.play()
                    player.alive = False
        #--------------- player and enemy collide with each other ------------
        for enemyturret in enemyturretgroup:
            if player.rectCollision.colliderect(enemyturret.rect):
                if abs(player.speed) <= player.maxspeed/4:
                    player.speed *= -1.5
                elif player.maxspeed/4 < abs(player.speed) <= player.maxspeed/2:
                    player.speed *= -1
                elif player.maxspeed/2 < abs(player.speed) <= player.maxspeed*3/4:
                    player.speed *= -0.5
                elif player.maxspeed*3/4 < abs(player.speed) <= player.maxspeed:
                    player.speed *= -0.3
                if abs(player.speed) >= player.maxspeed:
                    enemyturret.armor -= player.rammingDamage
                    player.armor -= player.rammingDamage
                    if player.armor <= 0:
                        player.armor = 0
                    if player.trackHit:
                        player.msg =  '''Armor: %i/%i  Track Status: %s  Repair Package Left: %i''' % (player.armor,player.maxarmor,"Track hit! Need repair!",player.repair)
                        Text.book[player.number].changemsg(player.msg)
                    else:
                        player.msg =  '''Armor: %i/%i  Track Status: %s  Repair Package Left: %i''' % (player.armor,player.maxarmor,"Operational",player.repair)
                        Text.book[player.number].changemsg(player.msg)
                    if player.armor > 0:
                        playerHitSound.play()
                    else:
                        playerDestroyedSound.play()
                        player.alive = False
                    if enemyturret.armor > 0:
                        enemyHitSound.play()
                    if enemyturret.armor <= 0:
                        enemyturret.kill()
                        del EnemyTurret.book[enemyturret.number]
                        enemyDestroyedSound.play()
                    
        #-------------- game over ------------------
        if not player.alive:
            over = True
            game_over(over)
        
        if (not Info.book) and (not EnemyTurret.book):
            win = True
            game_win(win)
            
        if scrollx == 0 and scrolly == 0:    # only necessery if there was no scrolling
            allgroup.clear(screen, background) # funny effect if you outcomment this line
        else:
            background = bigmap.subsurface((Config.cornerpos[0],
                                            Config.cornerpos[1],
                                            windowSize[0],
                                            windowSize[1])) # take snapshot of bigmap
            screen.blit(background, (0,0))
    #------------------ clear, draw, update, flip -----------------------
        screen.blit(background, (0,0))
        allgroup.clear(screen,background)
        allgroup.update(seconds)
        allgroup.draw(screen)
        player.update(seconds)
        turret.update(seconds)
        player.render(screen)
        turret.render(screen)
        pygame.display.flip()
        clock.tick(FPS)
########################################################################
###########################    classes    ##############################
########################################################################
class Config(object):
    cornerpos = [0,0]

class Text(pygame.sprite.Sprite):
    # a helper class to write text on the screen
    # cited from: http://thepythongamebook.com/en:part2:pygame:step022
    number = 0 
    book = {}
    def __init__(self, pos, msg):
        self.number = Text.number # get a unique number
        Text.number += 1 # prepare number for next Textsprite
        Text.book[self.number] = self # store myself into the book
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.pos = [0.0,0.0]
        self.pos[0] = pos[0]
        self.pos[1] = pos[1]
        self.msg = msg
        self.changemsg(msg)
    def update(self, seconds):        
        self.rect = self.image.get_rect()
        self.rect.centerx = self.pos[0]
        self.rect.centery = self.pos[1]
    def changemsg(self,msg):
        self.msg = msg
        self.image = write(self.msg)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.pos[0] 
        self.rect.centery = self.pos[1]

class Tank(pygame.sprite.Sprite):
    number = 0
    book = {}
    def __init__(self):
        self.number = Tank.number # now i have a unique tank number
        Tank.number += 1 # prepare number for next tank
        Tank.book[self.number] = self # store myself into the tank book
        self.tankImage = pygame.image.load(HT_body).convert()
        self.tankImage.set_colorkey(WHITE) 
        # -------------- tank's status ---------------------
        self.alive = True
        self.maxarmor = 200
        self.armor = self.maxarmor
        self.rammingDamage = 10
        self.trackHit = False
        self.maxrepair = 5
        self.repair = self.maxrepair
        self.infoGet = 0
        # set up tank's initial speed, position, and angle of tank's body
        self.speed = 0
        self.maxspeed = 6
        self.acc = 0.04 # accleration
        self.pos = [windowSize[0]/2, windowSize[1]/2]
        self.angle = 90
        self.rect = self.tankImage.get_rect()
        # self.rectCollision is for collision detection
        self.rectCollision = pygame.Rect(
        self.rect.x+imageSize/4,
        self.rect.y+imageSize/4,100,100)
        self.msg =  '''Armor: %i/%i  Track Status: %s  Repair Package Left: %i'''\
        % (self.armor,self.maxarmor,"Operational",self.repair)
        Text((windowSize[0]/2, margin+margin*self.number), self.msg) # create status line text sprite
        
    def render(self, surface):
        # this method draw the tank image on the surface
        surface.blit(self.tankImage1,(self.rect.x,self.rect.y))
        
    def update(self,seconds):
        #------------ tank body keyboard control ---------------
        pressedkeys = pygame.key.get_pressed()
        if not self.trackHit:
            if self.speed < self.maxspeed:
                if pressedkeys[pygame.K_w]:
                    self.speed += self.acc
            elif self.speed >= self.maxspeed:
                self.speed = self.maxspeed
            if self.speed > self.maxspeed*(-1):
                if pressedkeys[pygame.K_s]:
                    self.speed -= self.acc
            elif self.speed <= self.maxspeed*(-1):
                self.speed = self.maxspeed*(-1)
            if pressedkeys[pygame.K_a]:
                self.angle += 1
            if pressedkeys[pygame.K_d]:
                self.angle -= 1
        self.angle_rad = math.radians(self.angle)
        self.tankImage1 = rot_center(self.tankImage, self.angle)
        self.dx = math.cos(self.angle_rad)*self.speed
        self.dy = math.sin(self.angle_rad)*self.speed*(-1)
        self.pos[0] += self.dx # X coordinate
        self.pos[1] += self.dy # Y coordinate
        if self.pos[0] + self.rectCollision.width/2 >= bigmapWidth:
            self.pos[0] = bigmapWidth - self.rectCollision.width/2
            self.dx = 0 # crash into border
        elif self.pos[0] -self.rectCollision.width/2 <= 0:
            self.pos[0] = 0 + self.rectCollision.width/2
            self.dx = 0
        if self.pos[1] + self.rectCollision.height/2 >= bigmapHeight:
            self.pos[1] = bigmapHeight - self.rectCollision.height/2
            self.dy = 0 # crash into border
        elif self.pos[1] -self.rectCollision.height/2 <= 0:
            self.pos[1] = 0 + self.rectCollision.height/2
            self.dy = 0  
        self.rect.centerx = round(self.pos[0]-Config.cornerpos[0], 0) 
        self.rect.centery = round(self.pos[1]-Config.cornerpos[1], 0) 
        self.rectCollision = pygame.Rect(self.rect.x+imageSize/4,
        self.rect.y+imageSize/4,100,100)

        
class Turret(pygame.sprite.Sprite):
    def __init__(self):
        # load image here
        # make sure to type in the full directory 
        # in the pygame.image.load() function
        self.turretImage = pygame.image.load(HT_turret).convert()
        # make the white areas transparent
        self.turretImage.set_colorkey(WHITE)
        self.turretImageRecoil = pygame.image.load(HT_turret_recoil).convert()
        self.turretImageRecoil.set_colorkey(WHITE)
        self.rect = self.turretImage.get_rect()
        self.angle = 0
        # -------- cooldown time of cannon (cannon needs to recoil)----------
        self.cooldown = 0.0
        self.cooldownTime = 2.5
        # -------- turning speed of turret -----------
        self.turnSpeed = 100
        self.turndirection = 0
        
    def render(self, surface):
        surface.blit(self.turretImage2,(self.rect.x,self.rect.y))
    
    def aim_at_mouse(self):
        # this function make player turret  aim at the mouse
        mouse = pygame.mouse.get_pos()
        deltax = mouse[0]+Config.cornerpos[0] - Tank.book[0].pos[0]
        deltay = mouse[1]+Config.cornerpos[1] - Tank.book[0].pos[1]
        angle = math.atan2(-deltax,-deltay)/math.pi*180.0     
        diff = (angle - self.angle - 90) % 360 #reset at 360
        diff -= 180
        # to avoid a jittering canon introduce a tolerance range of 10 degrees
        if abs(diff) < 5:
            self.turndirection = 0
        elif diff > 0:
            self.turndirection = 1
        else:
            self.turndirection = -1
    
    def update(self,seconds):
        self.aim_at_mouse()
        self.pos = [Tank.book[0].pos[0],Tank.book[0].pos[1]]
        self.angle += self.turndirection * self.turnSpeed * seconds * (-1)
        if self.cooldown >= self.cooldownTime*5/6:
            self.turretImage2 = rot_center(self.turretImageRecoil,self.angle)
        else:
            self.turretImage2 = rot_center(self.turretImage,self.angle)
        self.rect = self.turretImage2.get_rect()
        self.rect.centerx = round(self.pos[0]-Config.cornerpos[0], 0)
        self.rect.centery = round(self.pos[1]-Config.cornerpos[1], 0)

class EnemyTurret(pygame.sprite.Sprite):
    number = 0
    book = {}
    size = 100
    def __init__(self,pos):
        self.number = EnemyTurret.number
        EnemyTurret.book[self.number] = self
        EnemyTurret.number += 1
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.pos = pos
        self.color = (100,100,255)
        self.side = 100
        self.angle = random.randint(1,360) # angle should be calculated with player.pos and Enemy.pos
        self.cooldownTime = 2.0
        self.cooldown = 0.0
        self.turnSpeed = 80
        self.turndirection = 0
        self.armor = 100
        #--------------- drawing ----------------
        image = pygame.Surface((self.side,self.side)) # created on the fly
        image.fill((128,128,128)) # fill grey
        pygame.draw.rect(image, self.color, 
        (5,5,self.side-10, self.side-10)) #tank body
        pygame.draw.rect(image, (90,90,90), 
        (0,0,self.side/6, self.side)) # track left
        pygame.draw.rect(image, (90,90,90), 
        (self.side-self.side//6, 0, self.side,self.side)) # right track
        pygame.draw.rect(image, (255,0,0), 
        (self.side/6+5 , 10, 10, 5)) # red bow rect left
        pygame.draw.circle(image, (150,134,0), 
        (self.side/2,self.side/2), self.side/3) # red circle for turret
        pygame.draw.rect(image,RED,
        (self.side/2-5,5,10,self.side/2))
        image = pygame.transform.rotate(image,-90) # rotate so to look east
        self.image0 = image.convert_alpha()
        self.image = image.convert_alpha()
        self.rect = self.image0.get_rect()
        
    def aim_at_player(self,targetNum = 0):
        # this function make enemy turret automatically aim at the player
        # cited from: http://thepythongamebook.com/en:part2:pygame:step022
        deltax = Tank.book[targetNum].pos[0] - self.pos[0] # x difference between two tanks
        deltay = Tank.book[targetNum].pos[1] - self.pos[1] # y difference between two tanks
        angle = math.atan2(-deltax,-deltay)/math.pi*180.0        
        diff = (angle - self.angle - 90) % 360 #reset at 360
        diff -= 180
        # to avoid a jittering canon introduce a tolerance range of 2 degrees
        if abs(diff) < 1:
            self.turndirection = 0
        elif diff > 0:
            self.turndirection = 1
        else:
            self.turndirection = -1
            
    def distance_from_player(self,targetNum = 0):
        # this method calculates and returns the distance between the player and the turret
        deltax = Tank.book[targetNum].pos[0] - self.pos[0] # x difference between two tanks 
        deltay = Tank.book[targetNum].pos[1] - self.pos[1] # y difference between two tanks 
        distance = math.sqrt(deltax**2 + deltay**2)
        return distance
            
    def update(self,seconds):
        self.aim_at_player()
        distance = self.distance_from_player()
        self.angle += self.turndirection * self.turnSpeed * seconds
        if self.cooldown == 0:
            if distance <= 400:
                EnemyShell(self.pos,self.angle)
                self.cooldown = self.cooldownTime
        elif self.cooldown > 0:
            self.cooldown -= seconds
        else:
            self.cooldown = 0 # avoid negative numbers
        oldcenter = self.rect.center
        oldrect = self.image.get_rect() # store current surface rect
        self.image  = pygame.transform.rotate(self.image0, self.angle) 
        self.rect = self.image.get_rect()
        self.rect.center = oldcenter
        self.rect.centerx = self.pos[0]-Config.cornerpos[0] 
        self.rect.centery = self.pos[1]-Config.cornerpos[1] 

class Shell(pygame.sprite.Sprite):
    side = 10 # small side of the rectangle
    color = RED
    maxLifeTime = 3.0
    def __init__(self,startPoint=[0,0],angle=0):
        pygame.sprite.Sprite.__init__(self, self.groups)
        #------------ deal with shell image -------------
        image = pygame.Surface((Shell.side * 2, Shell.side))
        image.fill((128,128,128)) # fill grey
        pygame.draw.rect(image, self.color, (0,0,int(Shell.side * 1.5), Shell.side)) 
        pygame.draw.circle(image, self.color, (int(self.side *1.5) ,self.side//2), self.side//2) 
        image.set_colorkey((128,128,128)) # grey transparent
        self.image0 = image.convert_alpha()
        self.image = pygame.transform.rotate(self.image0, angle)
        self.rect = self.image.get_rect()
        #------------ deal with parameters ---------------
        self.startPoint = startPoint # a list
        self.angle = angle
        self.pos = startPoint
        # the following two lines make sure that 
        # shells are fired out of the tip of the cannon
        self.pos[0]+=math.cos(math.radians(self.angle))*imageSize/2*(-1)
        self.pos[1]+=math.sin(math.radians(self.angle))*imageSize/2
        self.vel = 1600 # velocity
        self.lifeTime = 0.0
        # dx and dy of following are the x and y component of velocity
        self.dx = math.cos(math.radians(self.angle)) * self.vel * (-1)
        self.dy = math.sin(math.radians(self.angle)) * self.vel
        # damage
        self.damage = random.randint(20,40)
        
    def update(self,seconds=0.0):
        # ------ kill if the shell exists for too long ------
        self.lifeTime += seconds
        if self.lifeTime > Shell.maxLifeTime:
            self.kill()
        # ----------- calculate movement -------------
        self.pos[0] += self.dx * seconds
        self.pos[1] += self.dy * seconds
        self.rect.centerx = round(self.pos[0]-Config.cornerpos[0],0) 
        self.rect.centery = round(self.pos[1]-Config.cornerpos[1],0) 

class EnemyShell(pygame.sprite.Sprite):
    side = 5 # small side of the rectangle
    color = DARKYELLOW
    maxLifeTime = 3.0
    def __init__(self,startPoint=[0,0],angle=0):
        pygame.sprite.Sprite.__init__(self, self.groups)
        #------------ deal with shell image -------------
        image = pygame.Surface((Shell.side * 2, Shell.side))
        image.fill((128,128,128)) # fill grey
        pygame.draw.rect(image, self.color, 
        (0,0,int(Shell.side*1.5), Shell.side)) 
        pygame.draw.circle(image, self.color,
        (int(self.side*1.5) ,self.side/2), self.side/2) 
        image.set_colorkey((128,128,128)) # grey transparent
        self.image0 = image.convert_alpha()
        self.image = pygame.transform.rotate(self.image0, angle)
        self.rect = self.image.get_rect()
        #------------ deal with parameters ---------------
        self.startPoint = startPoint # a list
        self.angle = angle
        self.pos = copy.copy(startPoint)
        # the following two lines make sure that 
        # shells are fired out of the tip of the cannon
        self.pos[0]+=math.cos(math.radians(self.angle))*EnemyTurret.size/2
        self.pos[1]+=math.sin(math.radians(self.angle))*EnemyTurret.size/2*(-1)
        self.vel = 1600 # velocity
        self.lifeTime = 0.0
        # dx and dy of following are the x and y component of velocity
        self.dx = math.cos(math.radians(self.angle)) * self.vel
        self.dy = math.sin(math.radians(self.angle)) * self.vel * (-1)
        # damage
        self.damage = random.randint(10,20)
        
    def update(self,seconds=0.0):
        # ------ kill if the shell exists for too long ------
        self.lifeTime += seconds
        if self.lifeTime > Shell.maxLifeTime:
            self.kill()
        # ----------- calculate movement -------------
        self.pos[0] += self.dx * seconds
        self.pos[1] += self.dy * seconds
        self.rect.centerx = round(self.pos[0]-Config.cornerpos[0],0) 
        self.rect.centery = round(self.pos[1]-Config.cornerpos[1],0) 

class Rock(pygame.sprite.Sprite):
    # rocks cannot be destroyed by shells or by ramming
    # need position (a list), width, height to construct a rect rock
    number = 0
    book = {}
    def __init__(self,pos,width,height):
        self.number = Rock.number
        Rock.number += 1
        Rock.book[self.number] = self
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.pos = pos
        self.width = width
        self.height = height
        # -------- setup the image of a rock ---------      
        image = pygame.Surface((self.width,self.height))
        image.fill(BLACK) # fill balck
        pygame.draw.rect(image,ROCKCOLOR,(0,0,self.width,self.height)) 
        image.set_colorkey(BLACK) # BLACK transparent
        self.image = image.convert_alpha()
        self.rect = self.image.get_rect()
    def update(self,seconds):
        self.rect.x = round(self.pos[0]-Config.cornerpos[0],0) 
        self.rect.y = round(self.pos[1]-Config.cornerpos[1],0) 
        
class House(pygame.sprite.Sprite):
    # houses can be destroyed by shells or by ramming
    # need position (a list), width, height to construct a rect house
    number = 0
    book = {}
    def __init__(self,pos,width,height):
        self.number = House.number
        House.number += 1
        House.book[self.number] = self
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.pos = pos
        self.width = width
        self.height = height
        # -------- setup the image of a house ---------      
        image = pygame.Surface((self.width,self.height))
        image.fill(BLACK) # fill balck
        pygame.draw.rect(image,HOUSECOLOR,(0,0,self.width,self.height)) 
        image.set_colorkey(BLACK) # BLACK transparent
        self.image = image.convert_alpha()
        self.rect = self.image.get_rect()
    def update(self,seconds):
        self.rect.x = round(self.pos[0]-Config.cornerpos[0],0) 
        self.rect.y = round(self.pos[1]-Config.cornerpos[1],0) 
        
class Landmine(pygame.sprite.Sprite):
    # landmine can break the track of the tank
    # need position (a list), width, height to construct a rect landmine
    number = 0
    book = {}
    def __init__(self,pos,width,height):
        self.number = Landmine.number
        Landmine.number += 1
        Landmine.book[self.number] = self
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.pos = pos
        self.width = width
        self.height = height
        # -------- setup the image of a rock ---------      
        image = pygame.Surface((self.width,self.height))
        image.fill(BLACK) # fill balck
        pygame.draw.rect(image,LANDMINECOLOR,(0,0,self.width,self.height)) 
        image.set_colorkey(BLACK) # BLACK transparent
        self.image = image.convert_alpha()
        self.rect = self.image.get_rect()
        self.damage = 10
    def update(self,seconds):
        self.rect.x = round(self.pos[0]-Config.cornerpos[0],0) 
        self.rect.y = round(self.pos[1]-Config.cornerpos[1],0) 
        
class River(pygame.sprite.Sprite):
    # river slows tanks down
    # need position (a list), width, height to construct river
    number = 0
    book = {}
    def __init__(self,pos,width,height):
        self.number = River.number
        River.number += 1
        River.book[self.number] = self
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.pos = pos
        self.width = width
        self.height = height
        self.resistence = 4
        # -------- setup the image of a river ---------      
        image = pygame.Surface((self.width,self.height))
        image.fill(BLACK) # fill balck
        pygame.draw.rect(image,RIVERCOLOR,(0,0,self.width,self.height)) 
        image.set_colorkey(BLACK) # BLACK transparent
        self.image = image.convert_alpha()
        self.rect = self.image.get_rect()
    def update(self,seconds):
        self.rect.x = round(self.pos[0]-Config.cornerpos[0],0) 
        self.rect.y = round(self.pos[1]-Config.cornerpos[1],0) 

class Info(pygame.sprite.Sprite):
    # player needs to collect info
    # need position (a list), width, height to construct a rect info
    number = 0
    book = {}
    def __init__(self,pos,width,height):
        self.number = Info.number
        Info.number += 1
        Info.book[self.number] = self
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.pos = pos
        self.width = width
        self.height = height
        # -------- setup the image of a info ---------      
        image = pygame.Surface((self.width,self.height))
        image.fill(BLACK) # fill balck
        pygame.draw.rect(image,INFOCOLOR,(0,0,self.width,self.height)) 
        image.set_colorkey(BLACK) # BLACK transparent
        self.image = image.convert_alpha()
        self.rect = self.image.get_rect()
    def update(self,seconds):
        self.rect.x = round(self.pos[0]-Config.cornerpos[0],0) 
        self.rect.y = round(self.pos[1]-Config.cornerpos[1],0) 

class Reticle(pygame.sprite.Sprite):
    # reticle for aiming
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.side = 30
        # --------- drawing -----------
        image = pygame.Surface((self.side,self.side))
        image.fill(WHITE)
        pygame.draw.rect(image,RED,((0,0),(self.side,self.side)),5)
        pygame.draw.line(image,RED,(0,self.side/2),(self.side,self.side/2),4)
        pygame.draw.line(image,RED,(self.side/2,0),(self.side/2,self.side),4)
        self.image = image.convert_alpha()
        self.rect = self.image.get_rect()
        mouse = pygame.mouse.get_pos()
        self.rect.centerx = mouse[0]
        self.rect.centery = mouse[1]
    
    def update(self,seconds):
        mouse = pygame.mouse.get_pos()
        self.rect.centerx = mouse[0] 
        self.rect.centery = mouse[1] 
        
class Minimap(pygame.sprite.Sprite):
    # this class creates a mini radar map at the right down corner
    # cited from: http://thepythongamebook.com/en:part2:pygame:step022
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((minimapWidth,minimapHeight))
        self.paintmap() # self image's color is not defined, therfore it remains black
        self.rect = self.image.get_rect()
        self.rect.topleft = (windowSize[0] - minimapWidth, windowSize[1] - minimapHeight)
        self.factorx = minimapWidth  * 1.0 / bigmapWidth 
        self.factory = minimapHeight *1.0 / bigmapHeight
        
    def paintmap(self):
        self.image.fill((0,0,0))
        pygame.draw.rect(self.image,(150,0,0),(0,0,minimapWidth,minimapHeight),1)    
    
    def update(self, seconds):
        self.paintmap() # redraw black map # outcomment for funny painting effect
        pygame.draw.rect(self.image, (255,255,255), (round(Config.cornerpos[0] * self.factorx,0),
                                                     round(Config.cornerpos[1] * self.factory,0),
                                                     round(windowSize[0] * self.factorx, 0),
                                                     round(windowSize[1] * self.factory, 0)),1)
        for tanknumber in Tank.book:
            pos = Tank.book[tanknumber].pos
            pygame.draw.circle(self.image,YELLOW,(int(pos[0] * self.factorx),
                                                  int(pos[1] * self.factory)),4)
        for enemynumber in EnemyTurret.book:
            pos = EnemyTurret.book[enemynumber].pos
            pygame.draw.circle(self.image,GREEN, (int(pos[0] * self.factorx),
                                                  int(pos[1] * self.factory)),4)
        for rocknumber in Rock.book:
            pos = Rock.book[rocknumber].pos
            pygame.draw.circle(self.image,ROCKCOLOR, (int(pos[0] * self.factorx),
                                                  int(pos[1] * self.factory)),4)
        for housenumber in House.book:
            pos = House.book[housenumber].pos
            pygame.draw.circle(self.image,HOUSECOLOR, (int(pos[0] * self.factorx),
                                                  int(pos[1] * self.factory)),4)
        for rivernumber in River.book:
            pos = River.book[rivernumber].pos
            pygame.draw.circle(self.image,RIVERCOLOR, (int(pos[0] * self.factorx),
                                                  int(pos[1] * self.factory)),4)
        for infonumber in Info.book:
            pos = Info.book[infonumber].pos
            pygame.draw.circle(self.image,INFOCOLOR, (int(pos[0] * self.factorx),
                                                  int(pos[1] * self.factory)),4)


########################################################################
###################### universal functions #############################
########################################################################

def game_intro():
    # this function shows the start screen
    intro = True
    #---------- start menu BGM setup -------------
    pygame.mixer.music.load(BGM3)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1,0.0)
    #---------- start meny background image setup ------------
    startBackground = pygame.image.load(wallpaper_1).convert()
    #---------- button parameters setup -----------
    buttonWidth = 300
    buttonHeight = 60
    # start button:
    startLeft = windowSize[0]/2-buttonWidth/2
    startTop = windowSize[1]/2 + buttonHeight*2/2
    # help button:
    helpLeft = windowSize[0]/2-buttonWidth/2
    helpTop = windowSize[1]/2 + buttonHeight*5/2
    # quit buttion:
    quitLeft = windowSize[0]/2-buttonWidth/2
    quitTop = windowSize[1]/2 + buttonHeight*8/2
    #---------- game intro main loop ------------
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.blit(startBackground,[0,0])
        #---------- start screen buttons drawing and interaction ------------
        # if a button is hovered, the color of the button will change
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        # first draw three WHITE rects around three buttons
        pygame.draw.rect(screen,WHITE,
        (startLeft-5,startTop-5,buttonWidth+10,buttonHeight+10))
        pygame.draw.rect(screen,WHITE,
        (helpLeft-5,helpTop-5,buttonWidth+10,buttonHeight+10))
        pygame.draw.rect(screen,WHITE,
        (quitLeft-5,quitTop-5,buttonWidth+10,buttonHeight+10))
        if startLeft < mouse[0] < startLeft+buttonWidth and \
        startTop < mouse[1] < startTop+buttonHeight:
            pygame.draw.rect(screen,GREEN,
            (startLeft,startTop,buttonWidth,buttonHeight)) # start button hovered
            if click[0]:
                buttonClickSound.play()
                game_map() # start button clicked
        else: 
            pygame.draw.rect(screen,DARKGREEN,
            (startLeft,startTop,buttonWidth,buttonHeight)) # start button
        if helpLeft < mouse[0] < helpLeft+buttonWidth and \
        helpTop < mouse[1] < helpTop+buttonHeight:
            pygame.draw.rect(screen,BLUE,
            (helpLeft,helpTop,buttonWidth,buttonHeight)) # help button hovered
            if click[0]:
                buttonClickSound.play()
                game_help() # help button clicked
        else:
            pygame.draw.rect(screen,DARKBLUE,
            (helpLeft,helpTop,buttonWidth,buttonHeight)) # help button
        if quitLeft < mouse[0] < quitLeft+buttonWidth and \
        quitTop < mouse[1] < quitTop+buttonHeight:
            pygame.draw.rect(screen,RED,
            (quitLeft,quitTop,buttonWidth,buttonHeight)) # quit button hovered
            if click[0]:
                buttonClickSound.play()
                pygame.quit() # quit button clicked
                sys.exit()
        else:
            pygame.draw.rect(screen,DARKRED,
            (quitLeft,quitTop,buttonWidth,buttonHeight)) # quit button

        #------------ draw start screen text --------------
        # button font setup
        buttonTextFont = pygame.font.Font("freesansbold.ttf",30)
        # Start Button setup
        startTextSurf,startTextRect = text_objects("ROLL OUT!",buttonTextFont)
        startTextRect.center = ((startLeft+buttonWidth/2),(startTop+buttonHeight/2))
        screen.blit(startTextSurf,startTextRect)
        # Help Button setup
        helpTextSurf,helpTextRect = text_objects("MISSION BRIEFING",buttonTextFont)
        helpTextRect.center = ((helpLeft+buttonWidth/2),(helpTop+buttonHeight/2))
        screen.blit(helpTextSurf,helpTextRect)
        # Quit Button setup
        quitTextSurf,quitTextRect = text_objects("BAIL OUT!",buttonTextFont)
        quitTextRect.center = ((quitLeft+buttonWidth/2),(quitTop+buttonHeight/2))
        screen.blit(quitTextSurf,quitTextRect)
        
        pygame.display.update()
        clock.tick(FPS)

def game_map():
    # this function shows the start screen
    map_intro = True
    #---------- start menu BGM setup -------------
    pygame.mixer.music.load(BGM3)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1,0.0)
    #---------- start meny background image setup ------------
    startBackground = pygame.image.load(wallpaper_1).convert()
    #---------- button parameters setup -----------
    buttonWidth = 300
    buttonHeight = 60
    # first button:
    firstLeft = windowSize[0]/4-buttonWidth/2
    firstTop = windowSize[1]/4 - buttonHeight/2
    # second button:
    secondLeft = windowSize[0]*3/4-buttonWidth/2
    secondTop = windowSize[1]/4 - buttonHeight/2
    # third buttion:
    thirdLeft = windowSize[0]/4-buttonWidth/2
    thirdTop = windowSize[1]*3/4 - buttonHeight/2
    # fourth button:
    fourthLeft = windowSize[0]*3/4-buttonWidth/2
    fourthTop = windowSize[1]*3/4 - buttonHeight/2
    #---------- game intro main loop ------------
    while map_intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        #screen.fill(BLACK)
        screen.blit(startBackground,[0,0])
        #---------- start screen buttons drawing and interaction ------------
        # if a button is hovered, the color of the button will change
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        # first draw three WHITE rects around three buttons
        pygame.draw.rect(screen,WHITE,
        (firstLeft-5,firstTop-5,buttonWidth+10,buttonHeight+10))
        pygame.draw.rect(screen,WHITE,
        (secondLeft-5,secondTop-5,buttonWidth+10,buttonHeight+10))
        pygame.draw.rect(screen,WHITE,
        (thirdLeft-5,thirdTop-5,buttonWidth+10,buttonHeight+10))
        pygame.draw.rect(screen,WHITE,
        (fourthLeft-5,fourthTop-5,buttonWidth+10,buttonHeight+10))
        if firstLeft < mouse[0] < firstLeft+buttonWidth and \
        firstTop < mouse[1] < firstTop+buttonHeight:
            pygame.draw.rect(screen,GREEN,
            (firstLeft,firstTop,buttonWidth,buttonHeight)) # start button hovered
            if click[0]:
                buttonClickSound.play()
                game_map_1() # start button clicked
        else: 
            pygame.draw.rect(screen,DARKGREEN,
            (firstLeft,firstTop,buttonWidth,buttonHeight)) # start button
        if secondLeft < mouse[0] < secondLeft+buttonWidth and \
        secondTop < mouse[1] < secondTop+buttonHeight:
            pygame.draw.rect(screen,BLUE,
            (secondLeft,secondTop,buttonWidth,buttonHeight)) # help button hovered
            if click[0]:
                buttonClickSound.play()
                game_map_2() # help button clicked
        else:
            pygame.draw.rect(screen,DARKBLUE,
            (secondLeft,secondTop,buttonWidth,buttonHeight)) # help button
        if thirdLeft < mouse[0] < thirdLeft+buttonWidth and \
        thirdTop < mouse[1] < thirdTop+buttonHeight:
            pygame.draw.rect(screen,RED,
            (thirdLeft,thirdTop,buttonWidth,buttonHeight)) # quit button hovered
            if click[0]:
                buttonClickSound.play()
                game_map_3() # quit button clicked
        else:
            pygame.draw.rect(screen,DARKRED,
            (thirdLeft,thirdTop,buttonWidth,buttonHeight)) # quit button
        if fourthLeft < mouse[0] < fourthLeft+buttonWidth and \
        fourthTop < mouse[1] < fourthTop+buttonHeight:
            pygame.draw.rect(screen,YELLOW,
            (fourthLeft,fourthTop,buttonWidth,buttonHeight)) # quit button hovered
            if click[0]:
                buttonClickSound.play()
                game_map_4() # quit button clicked
        else:
            pygame.draw.rect(screen,DARKYELLOW,
            (fourthLeft,fourthTop,buttonWidth,buttonHeight)) # quit button

        #------------ draw start screen text --------------
        # button font setup
        buttonTextFont = pygame.font.Font("freesansbold.ttf",30)
        # Start Button setup
        firstTextSurf,firstTextRect = text_objects("Malinovka",buttonTextFont)
        firstTextRect.center = ((firstLeft+buttonWidth/2),(firstTop+buttonHeight/2))
        screen.blit(firstTextSurf,firstTextRect)
        secondTextSurf,secondTextRect = text_objects("Erlenberg",buttonTextFont)
        secondTextRect.center = ((secondLeft+buttonWidth/2),(secondTop+buttonHeight/2))
        screen.blit(secondTextSurf,secondTextRect)
        thirdTextSurf,thirdTextRect = text_objects("Himmelsdorf",buttonTextFont)
        thirdTextRect.center = ((thirdLeft+buttonWidth/2),(thirdTop+buttonHeight/2))
        screen.blit(thirdTextSurf,thirdTextRect)
        fourthTextSurf,fourthTextRect = text_objects("Prohorovka",buttonTextFont)
        fourthTextRect.center = ((fourthLeft+buttonWidth/2),(fourthTop+buttonHeight/2))
        screen.blit(fourthTextSurf,fourthTextRect)
        
        pygame.display.update()
        clock.tick(FPS)

def game_help():
    # this function shows the help screen
    Config.help = True
    pages = 2
    pageNum = 1
    #---------- start menu BGM setup -------------
    pygame.mixer.music.load(BGM1)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1,0.0)
    #---------- start meny background image setup ------------
    startBackground = pygame.image.load(wallpaper_2).convert()
    #---------- button parameters setup -----------
    buttonWidth = 100
    buttonHeight = 60
    # back button:
    backLeft = buttonWidth/2
    backTop = windowSize[1] - buttonHeight*2
    # next button:
    nextLeft = windowSize[0] - buttonWidth*3/2
    nextTop = windowSize[1] - buttonHeight*2
    # menu buttion:
    menuLeft = windowSize[0]/2 - buttonWidth/2
    menuTop = windowSize[1] - buttonHeight*2
    #---------- help screen main loop ------------
    while Config.help:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        #screen.fill(BLACK)
        screen.blit(startBackground,[0,0])
        #---------- start screen buttons drawing and interaction ------------
        # if a button is hovered, the color of the button will change
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        # first draw three WHITE rects around three buttons
        pygame.draw.rect(screen,WHITE,
        (backLeft-5,backTop-5,buttonWidth+10,buttonHeight+10))
        pygame.draw.rect(screen,WHITE,
        (nextLeft-5,nextTop-5,buttonWidth+10,buttonHeight+10))
        pygame.draw.rect(screen,WHITE,
        (menuLeft-5,menuTop-5,buttonWidth+10,buttonHeight+10))
        pygame.draw.rect(screen,BLACK,
        (backLeft,backTop,buttonWidth,buttonHeight))        
        # Back button:
        if pageNum > 1:
            if backLeft < mouse[0] < backLeft+buttonWidth and \
            backTop < mouse[1] < backTop+buttonHeight:
                pygame.draw.rect(screen,GREEN,
                (backLeft,backTop,buttonWidth,buttonHeight)) # back button hovered
                if click[0]:
                    pageNum -= 1
                    #print "%d / %d" % (pageNum,pages)
                    buttonClickSound.play()
                    # back button clicked
            else: 
                pygame.draw.rect(screen,DARKGREEN,
                (backLeft,backTop,buttonWidth,buttonHeight)) # back button
        else:
            pygame.draw.rect(screen,BLACK,
            (backLeft,backTop,buttonWidth,buttonHeight))
        # Next button
        if pageNum < pages:
            if nextLeft < mouse[0] < nextLeft+buttonWidth and \
            nextTop < mouse[1] < nextTop+buttonHeight:
                pygame.draw.rect(screen,BLUE,
                (nextLeft,nextTop,buttonWidth,buttonHeight)) # next button hovered
                if click[0]:
                    pageNum += 1
                    buttonClickSound.play()
                    # next button clicked
            else:
                pygame.draw.rect(screen,DARKBLUE,
                (nextLeft,nextTop,buttonWidth,buttonHeight)) # next button
        else:
            pygame.draw.rect(screen,BLACK,
            (nextLeft,nextTop,buttonWidth,buttonHeight))
        # Menu button:
        if menuLeft < mouse[0] < menuLeft+buttonWidth and \
        menuTop < mouse[1] < menuTop+buttonHeight:
            pygame.draw.rect(screen,RED,
            (menuLeft,menuTop,buttonWidth,buttonHeight)) # menu button hovered
            if click[0]:
                buttonClickSound.play()
                Config.help = False
                game_intro() # menu button clicked
        else:
            pygame.draw.rect(screen,DARKRED,
            (menuLeft,menuTop,buttonWidth,buttonHeight)) # menu button

        #------------ draw help screen button text --------------
        # button font setup
        buttonTextFont = pygame.font.Font("freesansbold.ttf",25)
        # Back Button setup
        backTextSurf,backTextRect = text_objects("BACK",buttonTextFont)
        backTextRect.center = ((backLeft+buttonWidth/2),(backTop+buttonHeight/2))
        if pageNum > 1:
            screen.blit(backTextSurf,backTextRect)
        # Next Button setup
        nextTextSurf,nextTextRect = text_objects("NEXT",buttonTextFont)
        nextTextRect.center = ((nextLeft+buttonWidth/2),(nextTop+buttonHeight/2))
        if pageNum < pages:
            screen.blit(nextTextSurf,nextTextRect)
        # Menu Button setup
        menuTextSurf,menuTextRect = text_objects("MENU",buttonTextFont)
        menuTextRect.center = ((menuLeft+buttonWidth/2),(menuTop+buttonHeight/2))
        screen.blit(menuTextSurf,menuTextRect)
        #------------ draw help screen help content --------------
        helpImage_1 = pygame.image.load(help_1).convert()
        helpImage_2 = pygame.image.load(help_2).convert()
        helpRect_1 = helpImage_1.get_rect()
        helpRect_2 = helpImage_2.get_rect()
        if pageNum == 1:
            screen.blit(helpImage_1,
            (windowSize[0]/2-helpRect_1.width/2,windowSize[1]/8))
        if pageNum == 2:
            screen.blit(helpImage_2,
            (windowSize[0]/2-helpRect_2.width/2,windowSize[1]/8))
        pygame.display.update()
        clock.tick(FPS)


def paused(pause):
    #---------- background setup ------------
    screen.fill(WHITE)
    #---------- button parameters setup -----------
    buttonWidth = 150
    buttonHeight = 60
    # resume button:
    backLeft =windowSize[0]/4 - buttonWidth/2
    backTop = windowSize[1] - buttonHeight*2
    # menu buttion:
    menuLeft = windowSize[0]*3/4 - buttonWidth/2
    menuTop = windowSize[1] - buttonHeight*2
    #---------- help screen main loop ------------
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        #---------- start screen buttons drawing and interaction ------------
        # if a button is hovered, the color of the button will change
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        # first draw three WHITE rects around three buttons
        pygame.draw.rect(screen,BLACK,
        (backLeft-5,backTop-5,buttonWidth+10,buttonHeight+10))
        pygame.draw.rect(screen,BLACK,
        (menuLeft-5,menuTop-5,buttonWidth+10,buttonHeight+10))       
        # resume button:
        if backLeft < mouse[0] < backLeft+buttonWidth and \
        backTop < mouse[1] < backTop+buttonHeight:
            pygame.draw.rect(screen,GREEN,
            (backLeft,backTop,buttonWidth,buttonHeight)) # back button hovered
            if click[0]:
                buttonClickSound.play()
                pause = False# back button clicked
        else: 
            pygame.draw.rect(screen,DARKGREEN,
            (backLeft,backTop,buttonWidth,buttonHeight)) # back button
        # Menu button:
        if menuLeft < mouse[0] < menuLeft+buttonWidth and \
        menuTop < mouse[1] < menuTop+buttonHeight:
            pygame.draw.rect(screen,RED,
            (menuLeft,menuTop,buttonWidth,buttonHeight)) # menu button hovered
            if click[0]:
                buttonClickSound.play()
                pause = False
                game_intro() # menu button clicked
        else:
            pygame.draw.rect(screen,DARKRED,
            (menuLeft,menuTop,buttonWidth,buttonHeight)) # menu button

        #------------ draw pause screen button text --------------
        # button font setup
        buttonTextFont = pygame.font.Font("freesansbold.ttf",25)
        # Back Button setup
        backTextSurf,backTextRect = text_objects("RESUME",buttonTextFont)
        backTextRect.center = ((backLeft+buttonWidth/2),(backTop+buttonHeight/2))
        screen.blit(backTextSurf,backTextRect)
        # Menu Button setup
        menuTextSurf,menuTextRect = text_objects("MENU",buttonTextFont)
        menuTextRect.center = ((menuLeft+buttonWidth/2),(menuTop+buttonHeight/2))
        screen.blit(menuTextSurf,menuTextRect)
        # pause text
        pauseTextFont = pygame.font.Font("freesansbold.ttf",100)
        pauseTextSurf,pauseTextRect = text_objects("Paused",pauseTextFont)
        pauseTextRect.center = ((windowSize[0]/2),(windowSize[1]/2))
        screen.blit(pauseTextSurf,pauseTextRect)

        pygame.display.update()
        clock.tick(FPS)

def game_over(over):
    #---------- background setup ------------
    screen.fill(WHITE)
    #---------- button parameters setup -----------
    buttonWidth = 150
    buttonHeight = 60
    # resume button:
    backLeft =windowSize[0]/4 - buttonWidth/2
    backTop = windowSize[1] - buttonHeight*2
    # menu buttion:
    menuLeft = windowSize[0]*3/4 - buttonWidth/2
    menuTop = windowSize[1] - buttonHeight*2
    #---------- help screen main loop ------------
    while over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        #---------- start screen buttons drawing and interaction ------------
        # if a button is hovered, the color of the button will change
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        # first draw three WHITE rects around three buttons
        pygame.draw.rect(screen,BLACK,
        (backLeft-5,backTop-5,buttonWidth+10,buttonHeight+10))
        pygame.draw.rect(screen,BLACK,
        (menuLeft-5,menuTop-5,buttonWidth+10,buttonHeight+10))       
        # resume button:
        if backLeft < mouse[0] < backLeft+buttonWidth and \
        backTop < mouse[1] < backTop+buttonHeight:
            pygame.draw.rect(screen,GREEN,
            (backLeft,backTop,buttonWidth,buttonHeight)) # back button hovered
            if click[0]:
                buttonClickSound.play()
                over = False
                game_intro()# back button clicked 
        else: 
            pygame.draw.rect(screen,DARKGREEN,
            (backLeft,backTop,buttonWidth,buttonHeight)) # back button
        # Menu button:
        if menuLeft < mouse[0] < menuLeft+buttonWidth and \
        menuTop < mouse[1] < menuTop+buttonHeight:
            pygame.draw.rect(screen,RED,
            (menuLeft,menuTop,buttonWidth,buttonHeight)) # menu button hovered
            if click[0]:
                pygame.quit()
                sys.exit() # menu button clicked
        else:
            pygame.draw.rect(screen,DARKRED,
            (menuLeft,menuTop,buttonWidth,buttonHeight)) # menu button

        #------------ draw pause screen button text --------------
        # button font setup
        buttonTextFont = pygame.font.Font("freesansbold.ttf",25)
        # Back Button setup
        backTextSurf,backTextRect = text_objects("MENU",buttonTextFont)
        backTextRect.center = ((backLeft+buttonWidth/2),(backTop+buttonHeight/2))
        screen.blit(backTextSurf,backTextRect)
        # Menu Button setup
        menuTextSurf,menuTextRect = text_objects("QUIT",buttonTextFont)
        menuTextRect.center = ((menuLeft+buttonWidth/2),(menuTop+buttonHeight/2))
        screen.blit(menuTextSurf,menuTextRect)
        # pause text
        pauseTextFont = pygame.font.Font("freesansbold.ttf",50)
        pauseTextSurf,pauseTextRect = text_objects("Deploy smoke! Every one get out!",pauseTextFont)
        pauseTextRect.center = ((windowSize[0]/2),(windowSize[1]/2))
        screen.blit(pauseTextSurf,pauseTextRect)

        pygame.display.update()
        clock.tick(FPS)
        
def game_win(win):
    #---------- background setup ------------
    screen.fill(WHITE)
    #---------- button parameters setup -----------
    buttonWidth = 150
    buttonHeight = 60
    # resume button:
    backLeft =windowSize[0]/4 - buttonWidth/2
    backTop = windowSize[1] - buttonHeight*2
    # menu buttion:
    menuLeft = windowSize[0]*3/4 - buttonWidth/2
    menuTop = windowSize[1] - buttonHeight*2
    #---------- help screen main loop ------------
    while win:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        #---------- start screen buttons drawing and interaction ------------
        # if a button is hovered, the color of the button will change
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        # first draw three WHITE rects around three buttons
        pygame.draw.rect(screen,BLACK,
        (backLeft-5,backTop-5,buttonWidth+10,buttonHeight+10))
        pygame.draw.rect(screen,BLACK,
        (menuLeft-5,menuTop-5,buttonWidth+10,buttonHeight+10))       
        # resume button:
        if backLeft < mouse[0] < backLeft+buttonWidth and \
        backTop < mouse[1] < backTop+buttonHeight:
            pygame.draw.rect(screen,GREEN,
            (backLeft,backTop,buttonWidth,buttonHeight)) # back button hovered
            if click[0]:
                buttonClickSound.play()
                win = False
                game_intro()# back button clicked 
        else: 
            pygame.draw.rect(screen,DARKGREEN,
            (backLeft,backTop,buttonWidth,buttonHeight)) # back button
        # Menu button:
        if menuLeft < mouse[0] < menuLeft+buttonWidth and \
        menuTop < mouse[1] < menuTop+buttonHeight:
            pygame.draw.rect(screen,RED,
            (menuLeft,menuTop,buttonWidth,buttonHeight)) # menu button hovered
            if click[0]:
                pygame.quit()
                sys.exit() # menu button clicked
        else:
            pygame.draw.rect(screen,DARKRED,
            (menuLeft,menuTop,buttonWidth,buttonHeight)) # menu button

        #------------ draw pause screen button text --------------
        # button font setup
        buttonTextFont = pygame.font.Font("freesansbold.ttf",25)
        # Back Button setup
        backTextSurf,backTextRect = text_objects("MENU",buttonTextFont)
        backTextRect.center = ((backLeft+buttonWidth/2),(backTop+buttonHeight/2))
        screen.blit(backTextSurf,backTextRect)
        # Menu Button setup
        menuTextSurf,menuTextRect = text_objects("QUIT",buttonTextFont)
        menuTextRect.center = ((menuLeft+buttonWidth/2),(menuTop+buttonHeight/2))
        screen.blit(menuTextSurf,menuTextRect)
        # pause text
        pauseTextFont = pygame.font.Font("freesansbold.ttf",50)
        pauseTextSurf,pauseTextRect = text_objects("Mission Accomplished!",pauseTextFont)
        pauseTextRect.center = ((windowSize[0]/2),(windowSize[1]/2))
        screen.blit(pauseTextSurf,pauseTextRect)

        pygame.display.update()
        clock.tick(FPS)

def text_objects(text,font):
    # this function makes text drawing easier
    textSurface = font.render(text,True,BLACK)
    return textSurface,textSurface.get_rect()

def rot_center(image,angle):
    # this function rotates and image around its center
    orig_rect = image.get_rect(center=(150,150))
    rot_image = pygame.transform.rotate(image,angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    # rot_rect.center is a tuple, which only changes when imgae rotates
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image
    # cited from online resource:
    # https://www.youtube.com/watch?v=kMkUbumYlak

def write(msg="pygame is cool"):
    # helper function for the Text sprite
    # cited from: http://thepythongamebook.com/en:part2:pygame:step022
    myfont = pygame.font.SysFont("None", 28)
    mytext = myfont.render(msg,True,WHITE)
    mytext = mytext.convert_alpha()
    return mytext 
    
########################################################################
#############################  main game  ##############################
########################################################################
game_intro() 

pygame.quit()
    
    
