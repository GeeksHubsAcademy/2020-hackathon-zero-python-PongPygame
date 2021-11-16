import pygame, sys, random, cv2

# 변수들 설정
White = (255,255,255)
score_pl = 0
score_ai = 0

# 스코어가 증가하는 함수
def increase_Player_score():
	global score_pl
	score_pl += 1

def increase_AI_score():
	global score_ai
	score_ai += 1

# 스코어 보드 함수
def player_scoreboard():
	global score_pl
	score_font = pygame.font.Font('freesansbold.ttf', 20)
	text_score = score_font.render('PL Score : %s' % score_pl, True, White)
	text_rect = text_score.get_rect()
	text_rect.centerx = round(screen_width / 2 + 180)
	text_rect.y = 35
	screen.blit(text_score, text_rect)

def AI_scoreboard():
	global score_ai
	score_font = pygame.font.Font('freesansbold.ttf', 20)
	text_score = score_font.render('AI Score : %s' % score_ai, True, White)
	text_rect = text_score.get_rect()
	text_rect.centerx = round(screen_width / 2 - 180)
	text_rect.y = 35
	screen.blit(text_score, text_rect)

# 공 움직임 함수
def ball_animation():
	global ball_speed_x, ball_speed_y, score_pl
	
	ball.x += ball_speed_x
	ball.y += ball_speed_y

	if ball.top <= 0 or ball.bottom >= screen_height:
		ball_speed_y *= -1

	if ball.left <= 0 :
		increase_Player_score()
		ball_start()

	if ball.right >= screen_width :
		increase_AI_score()
		ball_start()

	# 충돌 감지 colliderect
	if ball.colliderect(player) or ball.colliderect(opponent):
		ball_speed_x *= -1

# 컴퓨터와 플레이어의 BAR 움직임 함수
def player_animation():
	player.y += player_speed

	if player.top <= 0:
		player.top = 0
	if player.bottom >= screen_height:
		player.bottom = screen_height

def opponent_ai():
	if opponent.top < ball.y:
		opponent.y += opponent_speed
	if opponent.bottom > ball.y:
		opponent.y -= opponent_speed

	if opponent.top <= 0:
		opponent.top = 0
	if opponent.bottom >= screen_height:
		opponent.bottom = screen_height

# 공 초기화 함수
def ball_start():
	global ball_speed_x, ball_speed_y

	ball.center = (screen_width/2, screen_height/2)
	ball_speed_y *= random.choice((1,-1))
	ball_speed_x *= random.choice((1,-1))

# 파이게임 세팅
pygame.init()
clock = pygame.time.Clock()

#Opencv 세팅
cap = cv2.VideoCapture(0)

# 파이 게임의 창 크기
screen_width = 600
screen_height = 400
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Pong')

# 색깔
light_grey = (200,200,200)
bg_color = pygame.Color('grey12')

# 도형의 크기
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 70)
opponent = pygame.Rect(10, screen_height / 2 - 70, 10, 70)

# 공의 속도
ball_speed_x = 10 * random.choice((1,-1))
ball_speed_y = 10 * random.choice((1,-1))

# 상대방의 속도(플레이어 속도 초기화)
player_speed = 0
opponent_speed = 5

#게임 실행
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	if score_ai == 5:
			print("Player Lose!")
			pygame.quit()
			sys.exit()
	elif score_pl == 5:
			print("Player Win!")
			pygame.quit()
			sys.exit()
	# 카메라로 부터 사진 한장 읽기
	_, frame = cap.read()
	frame_resize = cv2.resize(frame, (500, 400))
	# 이미지 색 바꾸기
	grayimage = cv2.cvtColor(frame_resize, cv2.COLOR_RGB2GRAY)
	# 주먹을 인식하는 알고리즘 파일 가져오기
	cascade_file = cv2.CascadeClassifier("fist.xml")
	fist = cascade_file.detectMultiScale(grayimage,scaleFactor=1.05,
										minNeighbors=4,minSize=(60, 60),
										flags=cv2.CASCADE_SCALE_IMAGE)
	# 주먹에 대한 Rectangle을 그린다
	# Rectangle의 Y좌표를 이용하여 플레이어의 바(BAR)를 움직인다
	for x,y,w,h in fist:
		k = cv2.rectangle(frame_resize, (x,y), (x + w, y + h), (255, 255, 255), 5)

		cx = int(x + (w / 2))
		cy = y - 50
		cv2.circle(frame_resize, (cx, cy), 10, (255, 255, 0))

		if -50 <= cy <= 0:
			player_speed = -5
		elif 0 < cy <= 60:
			player_speed = -3
		elif 60 < cy <= 120:
			player_speed = 0
		elif 120 < cy <= 160:
			player_speed = 3
		elif 160 < cy <= 250:
			player_speed = 5
		
	# 카메라 이미지를 보여준다
	cv2.imshow("contour", frame_resize)

	#게임 진행을 위한 함수 실행
	ball_animation()
	player_animation()
	opponent_ai()

	# 파이게임 비주얼 설정 
	screen.fill(bg_color)
	pygame.draw.rect(screen, light_grey, player)
	pygame.draw.rect(screen, light_grey, opponent)
	pygame.draw.ellipse(screen, light_grey, ball)
	pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0),(screen_width / 2, screen_height))
	player_scoreboard()
	AI_scoreboard()
	pygame.display.flip()
	clock.tick(60)