import pygame,random,sys
from pygame.locals import *
from time import sleep
# -*- coding: utf-8 -*-
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
Display_width = 1000    # 1000 * 600 Display 크기
Display_height = 600
enemy_mini_width = 100     # 적군 크기
enemy_mini_height = 90
enemy_boss_width = 100    # 적군 크기
enemy_boss_height = 300
Aircraft_width = 100     # 비행기 크기
Aircraft_height = 90

FireBall1_width = 130
FireBall1_height = 60

chanceReset = 1   # 적군이 화면 밖으로 나간 횟수 한번 리셋 시켜줌
finalReset = 1    # 아이템 2번째 사용 용도
PressZ = False   # Z 아이템 사용;


FPS = 60 # 게임 프레임

def textObj(text, font):   #게임화면에 표시될 텍스트 모양과 영역 설정1
    textSurface = font.render(text, True, RED)
    return textSurface, textSurface.get_rect()

def HighScore(highscore):       # 최고점일 떄 출력하는 창
    global Display
    font = pygame.font.SysFont(None, 25)
    text = font.render('High Score : ' + str(highscore), True, RED)
    Display.blit(text,(450,0))

def DrawScore(count):   # 'Point'  표시
    global Display
    font = pygame.font.SysFont(None, 25)
    text = font.render('Point : ' + str(count), True, RED)
    Display.blit(text,(0,0))

def itemReset(): # item 쓸 수 있는 것을 표시
    global Display
    font = pygame.font.SysFont(None, 25)
    text = font.render("Item Available!", True, RED)
    Display.blit(text,(870,0))

def GameOver(): # 적이 3번 넘었을 떄
    global Display
    displayMessage('Game Over')
    if (int(point)> int(highscore)):
        f = open('highscore.txt','w')
        f.write(str(point))
        f.close()
    if (int(point) > int(highscore)): # 지금 점수가 최고점을 넘었을 시 실행
        drawobject(BackGround, 0, 0)
        DrawScore(point)
        HighScore(highscore)
        HighScoreDisplay()
    pygame.quit()
    quit()

def displayMessage(text):              # 'text'를 출력
    global Display

    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = textObj(text, largeText)
    TextRect.center = ((Display_width/2) , (Display_height/2))
    Display.blit(TextSurf, TextRect)
    pygame.display.update()
    sleep(2)

    #pygame.quit()
    #quit()          # 2초간 쉬고 종료
    # RunGame()

def crash(): # 비행기가 적군 + 파이어볼에 맞았는가 안맞았는가
    global Display
    displayMessage('Crashed')
    drawobject(BackGround,0,0)

    DrawScore(point)
    HighScore(highscore)
    GameOver()

def HighScoreDisplay():
    global Display
    displayMessage('High Score!')
    drawobject(BackGround,0,0)
    DrawScore(point)
    HighScore(highscore)



def drawobject(obj,x,y): # 객체 소환
    global Display
    Display.blit(obj,(x,y))

def RunSecondDisplay(): # 첫 시작화면에서 키보드 '2'를 눌렀을 때, 뜨는 화면
    global Display, HowToPlay

    HowToPlay = pygame.image.load("HowToPlay.png");
    crashed = False


    while not crashed:
        drawobject(HowToPlay, 0, 0)
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.type == K_ESCAPE):
                crashed = True  # 게임 종료
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_1:
                    RunGame()
                elif event.key == pygame.K_SPACE:
                    RunGame()

        pygame.display.update()

def RunFirstDisplay(): # 게임 첫화면
    global Display, BackGround, StartPile, HowToPlay

    StartPile = pygame.image.load("GameStartPage.png")
    crashed = False
    drawobject(StartPile, 0, 0)

    while not crashed:
        for event in pygame.event.get():  # 게임판에서 발생하는 다양한 키값을 리턴
            if event.type == QUIT or (event.type == KEYUP and event.type == K_ESCAPE):
                crashed = True  # 게임 종료
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    RunGame()

                elif event.key == pygame.K_2:
                    RunSecondDisplay()
                    #Display.fill(WHITE)
                    #drawobject(HowToPlay,0,0)

                elif event.key == K_3:
                    pygame.quit()
                    quit()

                elif event.key == K_SPACE:
                    RunGame()

        pygame.display.flip() #사진 렌더링



    pygame.quit()
    quit()

def RunGame():
    global Display,Aircraft,Clock,BackGround,HowToPlay, Enemy_Passed
    global Enemy_Mini, fires, Bullet, Boom, PressZ, chanceReset, finalReset,point,highscore

    isShotEnemy =  False
    Boom_count = 0
    Boom_count_boss = 0

    Enemy_Passed = 0
    highscore = 0
    point = 0
    Bullet_xy = [] # 총알 좌표

    x = Display_width * 0.05
    y = Display_height * 0.75
    y_change = 0



    enemy_mini_x = Display_width
    enemy_mini_y = random.randrange(0,Display_height)
    enemy_boss_x = Display_width
    enemy_boss_y = random.randrange(0,Display_height)
    isShotEnemyBoss = False

    f = open('highscore.txt','r')       #최고점수 불러오는 파일 입출력
    highscore = f.read()
    f.close()

    fire_x = Display_width
    fire_y = random.randrange(0,Display_height)
    random.shuffle(fires)
    fire = fires[0]

    crashed = False # 게임 종료위한 도구

    while not crashed:

        for event in pygame.event.get(): # 게임판에서 발생하는 다양한 키값을 리턴
            if event.type == QUIT or (event.type == KEYUP and event.type == K_ESCAPE):
                crashed = True  # 게임 종료

            if event.type ==pygame.KEYDOWN: # 비행기 이동
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    y_change = -6
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    y_change = 6

                elif event.key == pygame.K_a:   #총알 발사
                    Bullet_x = x + Aircraft_width
                    Bullet_y = y + Aircraft_height/2
                    Bullet_xy.append([Bullet_x,Bullet_y])

                if point >= 100000 and PressZ == False:  # 현재 점수가 100000점 이상 및 'z'키를 누르지 않은 상태
                    if event.key == pygame.K_z:
                        if chanceReset == 1:
                            chanceReset -= 1
                            Enemy_Passed = 0
                            PressZ = True

                elif point >= 300000 and PressZ == False: # 현재 점수가 300000점 이상 및 'z'를 누르지 않은 상태
                    if event.key == pygame.K_z:
                        if chanceReset == 1:
                            chanceReset -= 1
                            Enemy_Passed = 0
                            PressZ = True

                elif event.key == pygame.K_F1: # 'F1'를 누르면....
                    pygame.mixer.music.load('TheFatRat - Unity.mp3')  # 배경음악
                    pygame.mixer.music.play(-1, 0)
                elif event.key == pygame.K_F2:
                    pygame.mixer.music.load('OMFG - I Love You[1].mp3')  # 배경음악
                    pygame.mixer.music.play(-1, 0)
                elif event.key == pygame.K_F3:
                    pygame.mixer.music.load('SKRILLEX - BANGARANG.mp3') # 배경음악
                    pygame.mixer.music.play(-1,0)

                #elif event.key == pygame.K_SPACE:
                #    sleep(5)

            if event.type == pygame.K_DOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0

        Display.fill(BLACK)  # 기본 화면
        #Display.blit(BackGround, (BackGround_x, 0))  # Galaxy 배경 화면(렉이 심함 ㅜ)


        HighScore(highscore) # 파일에서 불러온 최고점수 표시
        DrawScore(point) # 포인트

        if point >= 100000 and PressZ == False: # 아이템 사용
            itemReset()
        elif point >= 300000 and PressZ == False:
            itemReset()

        if Enemy_Passed > 2:  # 적군이 지나간 횟수 test
            GameOver()

        if point >= 300000 and PressZ == True and finalReset == 1: # 300000점 이상시 아이템 한 번 더 사용할 수 있음
                finalReset -= 1
                chanceReset = 1
                PressZ = False

        # 비행기 위치
        y += y_change
        if y < 0:
            y = 0
        elif y > Display_height - Aircraft_height:
            y = Display_height - Aircraft_height

        # 적군(일반인) 위치
        enemy_mini_x -= 7 # 적군 이동속도
        if enemy_mini_x <= 0:  # 적군 생성
            Enemy_Passed += 1
            enemy_mini_x = Display_width
            enemy_mini_y = random.randrange(110, Display_height)

        # 적군 큰 몬스터
        if point >= 20000:
            enemy_boss_x -= 10  #적군 이동속도
            if enemy_boss_x <= 0: # 적군 생성
                Enemy_Passed += 1
                enemy_boss_x = Display_width
                enemy_boss_y = random.randrange(0, Display_height)

        if fire[1] == None: # 파이어볼 이동속도
            fire_x -= 25
        else:
            fire_x -= 15

        if fire_x <= 0:
            fire_x = Display_width
            fire_y = random.randrange(0, Display_height)
            random.shuffle(fires)
            fire = fires[0]  #불덩이 1개와 None 객체 4개

        if len(Bullet_xy)!= 0:     # bullet_xy에 좌표가 있으면 하나씩 추출해서 좌표 갱신 // 총알 속도는 15픽셀로 날아가도록 함
            for i, bxy in enumerate(Bullet_xy):
                bxy[0] += 15
                Bullet_xy[i][0] = bxy[0]
                if bxy[0] > enemy_mini_x:
                    if bxy[1] > enemy_mini_y and bxy[1] < enemy_mini_y + enemy_mini_height:
                        Bullet_xy.remove(bxy)
                        isShotEnemy = True # 총알과 적군의 만남
                        if (point < 1000): # 적군을 없앨을 떄, 점수 얻음  +  일정한 포인트를 얻을 시 적군을 죽였을 때 얻는 포인트 증가
                            point += 100
                        elif (point < 10000):
                            point += 500
                        elif (point < 50000):
                            point += 1100
                        else:
                            point += 1300

                if point>=20000:
                    if bxy[0] > enemy_boss_x:
                        if bxy[1] > enemy_boss_y and bxy[1] < enemy_boss_y + enemy_boss_height:
                            Bullet_xy.remove(bxy)
                            isShotEnemyBoss = True
                            if (point < 200000):
                                point += 3000
                            else:
                                point += 3600

                if bxy[0] >= Display_width:
                    try:
                        Bullet_xy.remove(bxy)
                    except:
                        pass


        if x + Aircraft_width > enemy_mini_x:
            if (y > enemy_mini_y and y < enemy_mini_y + enemy_mini_height) or (y+Aircraft_height > enemy_mini_y and y + Aircraft_height < enemy_mini_y + enemy_mini_height):
                crash()
        if point>=20000:
            if x + Aircraft_width > enemy_boss_x:
                if (y > enemy_boss_y and y < enemy_boss_y + enemy_boss_height) or (y+Aircraft_height > enemy_boss_y and y + Aircraft_height < enemy_boss_y + enemy_boss_height):
                    crash()

        if fire[1] != None: # 비행기와 불덩어리가 충돌
            if fire[0] == 0:
                FireBall_width = FireBall1_width
                FireBall_height = FireBall1_height

            if x + Aircraft_width > fire_x:
                if(y > fire_y and y < fire_y + FireBall_height) or (y+Aircraft_height > fire_y and y + Aircraft_height < fire_y + FireBall_height):
                    crash()

        drawobject(Aircraft, x, y)      # 비행기 화면

        if len(Bullet_xy)!=0:
            for bx,by in Bullet_xy:
                drawobject(Bullet,bx,by)


        if not isShotEnemy: # 총알이 박쥐에 명중하지 않았기에 박쥐를 화면에 계속 그림
                drawobject(enemy_mini,enemy_mini_x,enemy_mini_y)
        else:
                Boom_count += 1
                if Boom_count > 5:
                    Boom_count = 0
                    enemy_mini_x = Display_width
                    enemy_mini_y = random.randrange(90, Display_height-enemy_mini_height)
                    isShotEnemy = False


        if point >= 20000: # 20000점 이상 득점할시 몬스터 소환
                if not isShotEnemyBoss:
                    drawobject(enemy_boss,enemy_boss_x,enemy_boss_y)
                else:
                    Boom_count_boss +=1
                    if Boom_count_boss > 5:
                        Boom_count_boss = 0
                        enemy_boss_x = Display_width
                        enemy_boss_y = random.randrange(0, Display_height - enemy_boss_height)
                        isShotEnemyBoss = False


        if fire[1] != None:
            drawobject(fire[1], fire_x, fire_y)


        #drawobject(enemy_mini, enemy_mini_x, enemy_mini_y) #  작은 몬스터

        #if (point >= 20000):       # 20000점 이상 시 대형 몬스터 소환
        #    drawobject(enemy_boss, enemy_boss_x, enemy_boss_y) # 큰 몬스터

        pygame.display.flip()
        Clock.tick(FPS)

    pygame.quit()
    quit()

def initGame(): # 최초 실행
    global Display,Aircraft,Clock,BackGround,StartPile,HowToPlay
    global enemy_mini,enemy_boss, fires, Bullet

    fires = []

    pygame.init()
    Display = pygame.display.set_mode((Display_width, Display_height)) # 게임 화면(1000 * 600)


    Aircraft = pygame.image.load('AirPlane_1.png')
    BackGround = pygame.image.load('Galaxy.jpg')
    StartPile = pygame.image.load('GameStartPage.png')
    HowToPlay = pygame.image.load('HowToPlay.png')

    pygame.mixer.music.load('OMFG - I Love You[1].mp3')  # 기본 배경음악
    pygame.mixer.music.play(-1,0)
    pygame.display.set_caption('슈팅스타')
    enemy_mini = pygame.image.load('Enemy_Mini.png')
    enemy_boss = pygame.image.load('Enemy_Boss.png')
    fires.append((0, pygame.image.load('FireBall.png')))  #  나의 비행기가 불덩이에 충돌했는지 체크함
    Bullet = pygame.image.load('Bullet.png') # 총알

    for i in range(2): # Fire 출현
        fires.append((i+2, None)) # None도 포함

    Clock = pygame.time.Clock()

    RunFirstDisplay() # 게임 첫 화면 불러오기
    #RunGame()


if __name__ == '__main__':
    initGame()
