import pygame
import random

# 初始化
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("撲克牌發牌動畫")

# 顏色與字體
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CARD_COLOR = (200, 0, 0)
FONT = pygame.font.SysFont(None, 24)

# 撲克牌資料
SUITS = ['♠', '♥', '♦', '♣']
RANKS = ['A'] + [str(i) for i in range(2, 11)] + ['J', 'Q', 'K']
DECK = [f"{suit}{rank}" for suit in SUITS for rank in RANKS]
random.shuffle(DECK)

# 卡片類別
class Card:
    def __init__(self, value, target_x, target_y):
        self.value = value
        self.width, self.height = 60, 90
        self.x, self.y = WIDTH//2, HEIGHT//2  # 發牌起點：中央
        self.target_x = target_x
        self.target_y = target_y
        self.speed = 10
        self.reached = False
        self.hovered = False

    def update(self):
        if not self.reached:
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            distance = (dx**2 + dy**2)**0.5
            if distance < self.speed:
                self.x, self.y = self.target_x, self.target_y
                self.reached = True
            else:
                self.x += self.speed * dx / distance
                self.y += self.speed * dy / distance

    def draw(self, surface):
        # 如果 hover 就往上浮出
        offset = -20 if self.hovered else 0
        rect = pygame.Rect(self.x, self.y + offset, self.width, self.height)
        pygame.draw.rect(surface, CARD_COLOR, rect)
        pygame.draw.rect(surface, BLACK, rect, 2)

        # 顯示文字
        text = FONT.render(self.value, True, WHITE)
        surface.blit(text, (self.x + 8, self.y + 8 + offset))

    def check_hover(self, mouse_pos):
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.hovered = rect.collidepoint(mouse_pos)


# 玩家手牌初始化（橫向排開，有一點疊起來）
player_hand = []
hand_start_x = 100
hand_y = 450
overlap = 50  # 疊牌的寬度
for i in range(5):
    card = Card(DECK.pop(), hand_start_x + i * overlap, hand_y)
    player_hand.append(card)

# 遊戲主迴圈
clock = pygame.time.Clock()
running = True
while running:
    screen.fill((0, 100, 0))  # 綠色背景像桌面

    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 更新與繪製每張牌
    for card in player_hand:
        card.update()
        card.check_hover(mouse_pos)
        card.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
