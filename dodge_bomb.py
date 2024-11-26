import os
import pygame as pg
from random import randint
import sys
import time



WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0)
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def gameover(screen: pg.Surface) -> None:
    x, y = WIDTH//2, HEIGHT//2
    black_sur = pg.Surface((WIDTH,HEIGHT)) 
    black_sur.fill((0, 0, 0))
    black_rct = black_sur.get_rect(center=(WIDTH//2, HEIGHT//2)) #背景用中央座標を取得
    black_sur.set_alpha(180)# 黒画面を透けるように
    screen.blit(black_sur,black_rct)
    fonto = pg.font.Font(None, 80) #文字サイズを80に設定
    txt = fonto.render("Game Over", True, (255, 255, 255))
    txt_rct = txt.get_rect(center=(WIDTH // 2, HEIGHT // 2))#テキスト用中央座標
    screen.blit(txt, txt_rct)
    kksad_img = pg.transform.rotozoom(pg.image.load("fig/8.png"),0, 2.0)#泣いているこうかとんを格納
    sad_x, sad_y = WIDTH//2, HEIGHT//2 #画面の中央座標を取得
    screen.blit(kksad_img, (sad_x + 200, sad_y - 60)) #右側のこうかとんを表示
    screen.blit(kksad_img, (sad_x - sad_x//2, sad_y - 60)) #左側のこうかとんを表示
    pg.display.update()
    time.sleep(5)



def check_bound(rct: pg.rect) -> tuple[bool, bool]:
    """
    引数で与えられたRectの画面内外を判定する
    引数 : こうかとんRect or 爆弾Rect
    戻り値 : 真理値タプル (横, 縦) / 画面内 : True, 画面外 : False
    """
    yoko, tate = True, True
    if rct.left < 0 or rct.right > WIDTH:
        yoko = False
    if rct.top < 0 or rct.bottom > HEIGHT:
        tate = False
    return yoko,tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    bb_img = pg.Surface((20, 20)) #爆弾用空Sur
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10) #爆弾円を描く
    bb_rct = bb_img.set_colorkey((0, 0, 0)) 
    bb_rct = bb_img.get_rect() #爆弾Rect抽出
    bb_rct.center = randint(0, WIDTH), randint(0, HEIGHT)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300,200
    vx, vy = 5, 5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
          gameover(screen)
          return 
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, taple in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += taple[0]
                sum_mv[1] += taple[1]
        
        kk_rct.move_ip(sum_mv)
        #　画面外にこうかとんが出たら、元の場所に戻す
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        #　爆弾の画面内判定
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        bb_rct.move_ip(vx,vy)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
