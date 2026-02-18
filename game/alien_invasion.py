import sys
import os
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from enemy import Enemy

class SpaceWar():
    """게임 자원과 동작을 관리하는 클래스"""
    def __init__(self):
        """게임을 초기화하고 게임 자원을 만듭니다"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
    
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption("SPace War")
        
        base_path = os.path.dirname(__file__)
        bg_path = os.path.join(base_path, "image", "space.png")
        self.bg_image = None

        # 배경 이미지 로드. 이미지가 없으면 검정색 배경 선택
        try:
            bg_raw = pygame.image.load(bg_path)
            self.bg_image = pygame.transform.scale(
                bg_raw,
                (self.settings.screen_width, self.settings.screen_height)
            )
         
        except (pygame.error, FileNotFoundError) :
            pass

        self.ship = Ship(self)
        self.ships_left = self.settings.ship_limit
        self.ships = pygame.sprite.Group()
        self._create_ships()

        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self._create_fleet()
      
    def run_game(self):
        """게임의 메인 루프를 시작합니다"""
        while True:
            self._check_events()
            self.ship.update()
            
            self._update_bullets()
            self._update_enemies()
        
            self._update_screen()
            pygame.display.flip()
            self.clock.tick(60)
    
    def _check_events(self):
        """#키보드와 마우스 이벤트에 응답합니다."""
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)

                elif event.type == pygame.KEYUP:
                    self._check_up_events(event)


    def _check_keydown_events(self, event):
        """키를 누를 때마다 응답합니다"""

        if event.key == pygame.K_F1:
            # F1 키를 누르면 풀스크린 화면으로 전환
            self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height), pygame.FULLSCREEN)
        if event.key == pygame.K_F2 or event.key == pygame.K_ESCAPE:
            self.screen = pygame.display.set_mode((1200, 800))
        if event.key == pygame.K_SPACE:
            self._fire_bullet()
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True

    def _check_up_events(self, event):
        """키를 뗄 때마다 응답합니다"""        
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

        
    def _update_screen(self):
        
        if self.bg_image is not None:
            self.screen.blit(self.bg_image, (0, 0))
        else:
            self.screen.fill((0, 0, 0))  

        self.enemies.draw(self.screen)

        for bullet in self.bullets.sprites():
            bullet.draw()

        self.ship.draw()
        self.ships.draw(self.screen)


      # 탄환 업데이트
    def _update_bullets(self):
        self.bullets.update()

        # 화면 밖 탄환 제거
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
        self._check_bullet_enemy_collisions()

        
    def _check_bullet_enemy_collisions(self):
        """충돌한 탄환과 외계인 제거"""
        # 충돌 처리
        collisions = pygame.sprite.groupcollide(
        self.bullets,
        self.enemies,
        True,
        True
    )
        # 남아 있는 탄환을 제거하고 함대를 새로 만듭니다.      
        if not self.enemies:
            self.bullets.empty()
            self._create_fleet()

    

    def _fire_bullet(self):
        """새 총알 생성"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)


    # 적 함대 업데이트
    def _update_enemies(self):
        """함계가 경계에 도달했는지 확인하고 위치를 업데이트합니다"""
        self._check_fleet_edges()
        # 적이 플레이어와 충돌했는지 확인
        if pygame.sprite.spritecollideany(self.ship, self.enemies):
            self._ship_hit()
        self._check_enemies_bottom()
        self.enemies.update()

    def _create_fleet(self):
        """적 함대 생성"""
        """적군 사이의 공간은 적군의 너비와 높이와 같습니다"""
        enemy = Enemy(self)
        enemy_width, enemy_height = enemy.rect.size
        available_space_x, available_space_y = enemy_width, enemy_height

        while available_space_y < self.settings.screen_height - (3 * enemy_height):
            while available_space_x < self.settings.screen_width - (1.5 * enemy_width):
                self._create_enemy(available_space_x, available_space_y)
                available_space_x += 2 * enemy_width
            # 한 줄이 끝났으니 x값을 초기화하고 y값을 늘립니다
            available_space_x = enemy_width
            available_space_y += 2* enemy_height

    def _create_enemy(self, x_position, y_position):
            """외계인 하나 만들어 배치합니다""" 
            new_enemy = Enemy(self)
            new_enemy.x = x_position
            new_enemy.rect.x = x_position
            new_enemy.rect.y = y_position
            self.enemies.add(new_enemy)


     # 적이 화면 끝에 닿는지 확인
    def _check_fleet_edges(self):
        for enemy in self.enemies.sprites():
            if enemy.check_edges():
                self._change_fleet_direction()
                break
    

    # 적군 방향 전환
    def _change_fleet_direction(self):
        for enemy in self.enemies.sprites():
            enemy.rect.y += self.settings.fleet_drop_speed

        self.settings.fleet_direction *= -1

    def _check_enemies_bottom(self):
        """적이 화면 하단에 닿았는지 확인"""
        screen_rect = self.screen.get_rect()
        for enemy in self.enemies.sprites():
            if enemy.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _create_ships(self):
        """남은 생명을 화면에 표시"""
        for ship_number in range(self.ships_left):
            ship = Ship(self)

            # 크기 줄이기
            ship.image = pygame.transform.scale(ship.image, (50, 50))
            ship.rect = ship.image.get_rect()

            ship.rect.x = 10 + ship_number * 60
            ship.rect.y = 10

            self.ships.add(ship)

    def _ship_hit(self):
        """플레이어가 외계인에 맞았을 때 처리"""
        if self.ships_left > 0:
            self.ships_left -= 1
            self.ships.empty()
            self._create_ships()


            print(f"남은 생명: {self.ships_left}")

            # 화면 정리
            self.enemies.empty()
            self.bullets.empty()
            
            # 함대 다시 생성
            self._create_fleet()

            # 우주선 중앙 재배치
            self.ship.rect.midbottom = self.ship.screen_rect.midbottom
            self.ship.x = float(self.ship.rect.x)
            self.ship.y = float(self.ship.rect.y)

            pygame.time.delay(500)

        else:
            print("게임 오버")
            pygame.quit()
            sys.exit()


    

if __name__ == '__main__':
    #게임 인스턴스를 만들고 게임을 실행합니다.
    ai = SpaceWar()
    ai.run_game()
