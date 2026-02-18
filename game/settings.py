class Settings:
    """외계인의 침공 설정을 저장하는 클래스"""

    def __init__(self):
        """게임 설정 초기화"""
        # 화면 설정
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color =  (0, 0, 0)
        self.ship_speed = 4.5

        # 플레이어 생명
        self.ship_limit = 3

        # 탄환 설정
        self.bullet_speed = 3.0
        self.bullets_allowed = 15

        # 적 함대 설정
        self.enemy_speed = 1.5
        self.fleet_drop_speed = 20   # 아래로 내려오는 거리
        self.fleet_direction = 1     # 1=오른쪽, -1=왼쪽
