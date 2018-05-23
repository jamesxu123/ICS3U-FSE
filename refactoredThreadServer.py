from BaseGame import *
import copy
import multiprocessing as mp
bullets = dict()
g = GameMode(server=True)

class Server:

    def __init__(self, game, BUFFER_SIZE):
        self.TCP_IP = ''  # ''159.203.163.149'
        self.TCP_PORT = 4545
        self.BUFFER_SIZE = BUFFER_SIZE  # Normally 1024, but we want fast response
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.TCP_IP, self.TCP_PORT))
        self.s.listen(1)
        self.player_dict = {}
        self.player_health_dict = {}
        self.running = True
        self.instance = GameMode(server=True)
        self.send_dict = dict()
        self.game = game

    def listen(self):
         while self.running:
              print("Before looking")
              conn, addr = self.s.accept()
              print("After looking")
              conn.settimeout(10)
              threading.Thread(target=self.listen_client, args=(conn, addr)).start()

    def listen_client(self, conn, addr):
         print('thread')
         current_player = ''
         while self.running:
              try:
                   data = conn.recv(self.BUFFER_SIZE)
                   if data:
                        try:
                             decoded = pickle.loads(data)
                             self.player_dict[decoded.name] = decoded
                             if decoded.name not in self.player_health_dict.keys():
                                 self.player_health_dict[decoded.name] = decoded.health
                             else:
                                 for key, value in self.player_health_dict.items():
                                     self.player_dict[key].health = value
                             current_player = decoded.name
                             conn.send(pickle.dumps(self.player_dict))
                             bullets[current_player] = decoded.bullets
                        except Exception as E:
                            print("Error:", E)
                   else:
                        pass
              except Exception as E:
                  print(E)

         conn.close()

    def check_damage(self):
        g = self.game
        for name, obj in self.player_dict.items():
            for b in obj.bullets:
                for p in self.player_dict.values():
                    if name == p.name:
                        continue
                    px, py = p.pos
                    nx = b[0][0]
                    ny = b[0][1]
                    lx, ly = (nx - px + 1280 // 2, ny - py
                              + 800 // 2)
                    angle = b[1]
                    interpolate = [(lx - i * cos(radians(angle)),
                                    ly + i * sin(radians(angle))) for i in range(20)]
                    for ix, iy in interpolate:
                        if p.rect.collidepoint((ix, iy)):
                            if self.player_health_dict[p.name] - 10 >= 0:
                                self.player_health_dict[p.name] -= 10
                            obj.bullets.remove(b)
                            break

    def take_damage(self, amount):
        self.player.health -= amount

juniper = Server(g, BUFFER_SIZE)
threading.Thread(target=juniper.listen).start()
while juniper.running:
    try:
##        if __name__ == '__main__':
##            with mp.Pool(mp.cpu_count()) as p:
##                p.map(juniper.check_damage, bullet_list)
        juniper.check_damage()
    except Exception as E:
        print('Error Checking Bullets:', E)
