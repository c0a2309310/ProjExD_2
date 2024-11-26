import os
from random import randint
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0)
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def gameover(screen: pg.Surface) -> None:
    """
    画面を半透明の黒で塗りつぶし「Game Over」を表示する
    Game Over の両隣に泣き顔こうかとんを表示する
    引数:screen(pg.Surface)ゲームウィンドウのSurfaceオブジェクト
    """
    x, y = WIDTH//2, HEIGHT//2
    black_sur = pg.Surface((WIDTH,HEIGHT)) 
    black_sur.fill((0, 0, 0))#黒で塗りつぶす
    black_rct = black_sur.get_rect(center=(WIDTH//2, HEIGHT//2)) #背景用座標を取得
    black_sur.set_alpha(180)# 黒画面を透けるように
    screen.blit(black_sur,black_rct)
    fonto = pg.font.Font(None, 80) #文字サイズを80に設定
    txt = fonto.render("Game Over", True, (255, 255, 255))
    txt_rct = txt.get_rect(center=(WIDTH // 2, HEIGHT // 2))#テキスト用座標
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


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    爆弾の速度とサイズを変更するためのリストを作成する
    戻り値:tuple 爆弾画像リストと加速度リスト
    """
    accs = [a for a in range(1,11)] 
    size = [0 for i in range(1,11)]
    for r in range(1,11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        size[r-1] = bb_img
    return size,accs


def get_moved_image(move: tuple[int, int],kk_img: pg) -> pg.Surface:
    """
    引数で指定される移動量に対応する画像Surfaceを返す
    """
    kk_img2 = pg.transform.flip(kk_img, True, False)
    # 移動量に基づき画像を回転する
    if move == (0, -5):  # 上
        return pg.transform.rotozoom(kk_img2, 90, 1.0) #上向き
    elif move == (0, 5):  # 下
        return pg.transform.rotozoom(kk_img2, -90, 1.0)  # 上下反転
    elif move == (-5, 0):  # 左
        return kk_img
    elif move == (5, 0):  # 右
        return kk_img2  # 右向き
    elif move == (-5, -5):  # 左上
        return pg.transform.rotozoom(kk_img, 45, 1.0)
    elif move == (5, -5):  # 右上
        return pg.transform.rotozoom(kk_img2, -45, 1.0)
    elif move == (-5, 5):  # 左下
        return pg.transform.rotozoom(kk_img, 135, 1.0)
    elif move == (5, 5):  # 右下
        return pg.transform.rotozoom(kk_img, -135, 1.0)
    return kk_img  # 移動がない場合
    

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    bb_imgs, bb_accs = init_bb_imgs()#加速度・サイズのリスト

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
        bb_img = bb_imgs[min(tmr//500, 9)]
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, taple in DELTA.items():
            if key_lst[key]:
                kk_img = get_moved_image(taple)
                sum_mv[0] += taple[0]
                sum_mv[1] += taple[1]
        bb_accs = [a for a in range(1, 11)] #爆弾加速度
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
        avx = vx*bb_accs[min(tmr//500, 9)]
        bb_rct.move_ip(avx,vy)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
