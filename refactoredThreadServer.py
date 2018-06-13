from BaseGame import *
import copy
import multiprocessing as mp
del_bullets = dict()
g = GameMode(server=True)


class GameInstance:
    def __init__(self, name, clients):
        'name: str; clients = [(conn,addr)]'
        self.player_dict = {}
        self.player_health_dict = {}
        self.running = True
        self.instance = GameMode(server=True)
        print("finish loading images")
        self.send_dict = dict()
        self.game = self.instance
        self.clients = clients
        assaultrifle = Gun('AR',image.load('Weapons/lightbullet.png'),5,image.load('Weapons/machinegun.png'),0,0.15)
        shotgun = Gun('Shotgun', image.load('Weapons/shellBullet.png'),10,image.load('Weapons/shotgunb.png'), 6,0)
        sniper = Gun('Sniper',image.load('Weapons/heavyBullet.png'),25,image.load('Weapons/sniper.png'),1,0)
        rpg = Gun('RPG',image.load('Weapons/rocketammo.png'),50,image.load('Weapons/rpg.png'),1,0)
        self.weapon_dict = {"Shotgun":shotgun,"AR":assaultrifle,"Sniper":sniper,"RPG":rpg}
        self.weapon_map =[]
        
        for i in range(20):
            weapon = choice(list(self.weapon_dict))
            wx,wy = (randint(100,11900),randint(100,7900))
            self.weapon_map.append([weapon,(wx,wy),100])
            #self.weapon_map will be sent along with player_dict, client will send weapon that they picked up, and the weapon they will drop (or none)
        #Storm
        self.storm_time  = 30000000000000000 #Tim
        self.storm_moving  = 6000000000000
        self.storm_next = "idle"
        self.storm_pos = []
        self.storm_rad = [6000,4000,3000,2000,1000,500]
        self.dam = 0
        self.stormB = True
        self.storm_state = 0
        self.storm(True)
        for a in range(len(self.storm_rad)):
            if self.storm_rad[a] == 6000:
                self.storm_pos.append([6000,4000])
            elif self.storm_rad[a] == 4000:
                self.storm_pos.append([randint(3000,9000),randint(3000,5000)])
            else:
                print((self.storm_pos[a-1][0],self.storm_rad[a-1]))
                print((self.storm_pos[a-1][1],self.storm_rad[a-1]))
                x = randint(self.storm_pos[a-1][0]-self.storm_rad[a-1]-self.storm_rad[a]+200,self.storm_pos[a-1][0]+self.storm_rad[a-1]-self.storm_rad[a]-200)
                y = randint(self.storm_pos[a-1][1]-self.storm_rad[a-1]-self.storm_rad[a]+200,self.storm_pos[a-1][1]+self.storm_rad[a-1]-self.storm_rad[a]-200)
                self.storm_pos.append([x,y])
        threading.Thread(target=self.check_damage).start()
        threading.Thread(target=self.storm).start()
    def create_thread(self,username):
        for c in self.clients:
<<<<<<< HEAD
            if c[0] == username:
                conn, addr = (c[2], c[3])
                threading.Thread(target=self.listen_client, args=(conn, addr)).start()
            else:
                return
=======
            conn, addr = (c[2], c[3])
            threading.Thread(target=self.listen_client, args=(conn, addr)).start()
<<<<<<< HEAD
            print("create thread")
        
        
        
        
        
     
              
=======
>>>>>>> d5971fea5d549f76e757f0bfc3d83e3ae1fc9c3b
        print("create thread")
>>>>>>> c49479856d1f719fdeb0a7866811a5a2501a57bc

    def listen_client(self, conn, addr):
        print('listen client')
        current_player = ''
        fps_clock = time.Clock()
        while self.running:
            try:
                data = conn.recv(BUFFER_SIZE)
                if data == pickle.dumps('leave'):
                    print(current_player, 'is leaving')
                    self.remove(current_player)
                if data:
                    try:
                        decoded = pickle.loads(data)
                        current_player = decoded.name
                        self.player_dict[decoded.name] = decoded
                        
                        if current_player not in self.player_health_dict.keys():
                            self.player_health_dict[current_player] = 100
                        else:
                            for key, value in self.player_health_dict.items():
                                self.player_dict[key].health = value
                        #Remove and add weapons
                        #print(self.player_dict[current_player].weapon_send)
                        
                        if len(self.player_dict[current_player].weapon_send) > 0:
                            if len(self.player_dict[current_player].weapon_send) == 1:
                                del self.weapon_map[self.weapon_map.index(self.player_dict[current_player].weapon_send[0])]
                            else:
                                self.weapon_map.append(self.player_dict[current_player].weapon_send[1])
                                del self.weapon_map[self.weapon_map.index(self.player_dict[current_player].weapon_send[0])]
                            self.player_dict[current_player].weapon_send = ["Sent"]
                        if (self.storm_state+1) != len(self.storm_rad):
                            self.player_dict[current_player].storm = [self.storm_pos[self.storm_state],self.storm_rad[self.storm_state],self.storm_next,self.storm_pos[self.storm_state+1],self.storm_rad[self.storm_state+1]]
                        else:
                            self.player_dict[current_player].storm = [self.storm_pos[self.storm_state],self.storm_rad[self.storm_state],self.storm_next]
                                
                        self.player_dict[current_player].weapon_map = self.weapon_map
                        if current_player in del_bullets: #Disconnect, bullets will be deleted
                            self.player_dict[current_player].del_bullets += del_bullets[current_player]
                        del_bullets[current_player] = []
                        conn.send(pickle.dumps(self.player_dict))
                        #print("sent")
                    except Exception as E:
                            print("Error:", E)
                else:
                    pass
            except Exception as E:
                print(E)
                self.remove(current_player)
                break
        conn.close()

    def check_damage(self):
        while self.running:
            g = self.game
            for name, obj in {k: v for k,v in self.player_dict.items()}.items():
                try:
                    x = self.storm_pos[self.storm_state][0]-obj.pos[0]
                    y = self.storm_pos[self.storm_state][1]-obj.pos[1]
                    if hypot(x,y)>self.storm_rad[self.storm_state] and t.time()-self.dam>1:
                        self.dam = t.time()
                        if self.player_health_dict[name] - 1 >= 0:
                            self.player_health_dict[name] -= 1
                except:
                    pass
                        #print("OUTSIDE STORM")
                for b in obj.bullets:
                    for p in [i for i in self.player_dict.values()]:
                        if name == p.name:
                            continue
                        if name in del_bullets.keys():
                            if b in del_bullets[name]:
                                continue
                        px, py = p.pos
                        nx = b[0][0]
                        ny = b[0][1]
                        if hypot(px-nx, py-ny) > 60:
                            continue
                        angle = b[1]
##                        interpolate = [(nx - i * cos(radians(angle)),
##                                        ny + i * sin(radians(angle))) for i in range(b[3])]
                        interpolate = gameMath.interpolate(int(nx),int(ny),int(angle),int(b[3]))
                        counter = 0
                        for ix, iy in interpolate:
                            if hypot(px - nx, py - ny) < 30:
                                counter += 1
                                print(counter, name)
                                obj.bullets.remove(b)
                                if name not in del_bullets.keys():
                                    del_bullets[name] = [b]
                                else:
                                    del_bullets[name].append(b)
                                if self.player_health_dict[p.name] - 10 >= 0:
                                    self.player_health_dict[p.name] -= 10
                                break

    def take_damage(self, amount):
        self.player.health -= amount

    def remove(self, player_name):
        try:
            del self.player_health_dict[player_name]
        except ValueError:
            pass
        try:
            del self.player_dict[player_name]
        except ValueError:
            pass
        try:
            del del_bullets[player_name]
        except ValueError:
            pass
    def storm(self,start = False):
        if start:
            self.storm_time = t.time()
        else:
            while self.running:
                if t.time()-self.storm_time>60:
                    self.storm_time = t.time()
                    if self.storm_next == "idle":
                        self.storm_next = "moving"
                        self.storm_rad[self.storm_state]
                        self.x = int((self.storm_pos[self.storm_state][0]-self.storm_pos[self.storm_state+1][0])/(600))
                        self.y = int((self.storm_pos[self.storm_state][1]-self.storm_pos[self.storm_state+1][1])/(600))
                        print(self.x, self.y)
                        print(self.storm_pos)
                        self.r = int((self.storm_rad[self.storm_state]-self.storm_rad[self.storm_state+1])/600)
                        print(self.r)
                        self.storm_moving = 0
                    
                    else:
                        self.storm_next = "idle"
                        self.storm_state += 1
                    
                    print("THE STORM")
                if t.time()-self.storm_moving>.1 and self.storm_next == "moving":
                    self.storm_moving = t.time()
                    if (self.storm_state+1) != len(self.storm_rad) and self.storm_rad[self.storm_state] >= self.storm_rad[self.storm_state+1]:
                        self.storm_pos[self.storm_state][0]-=self.x-1
                        self.storm_pos[self.storm_state][1]-=self.y-1
                        self.storm_rad[self.storm_state]-= self.r +1
                        #print(self.storm_rad,self.storm_pos)
                        #print("moving")


class Server:
    def __init__(self, BUFFER_SIZE):
        self.TCP_IP = ''  # ''159.203.163.149'
        self.TCP_PORT = 4545
        self.BUFFER_SIZE = BUFFER_SIZE  # Normally 1024, but we want fast response
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.TCP_IP, self.TCP_PORT))
        self.s.listen(1)
        self.rooms = {'funroom':[]}
        self.game = GameMode(server=True)
        self.game_instances = {}
        self.running = True

    def listen(self):
         while self.running:
              print("Before looking")
              conn, addr = self.s.accept()
              print("After looking")
              conn.settimeout(180)
              STRUCT = ['room name', 'player list']
              threading.Thread(target=self.listen_client, args=(conn, addr)).start()

    def listen_client(self, conn, addr):
        print('room thread')
        data = pickle.loads(conn.recv(self.BUFFER_SIZE))
        name = data['name']
        mode = data['mode']
        room_name = data['room_name']
        if mode == 'join':
            if room_name not in self.rooms.keys():
                conn.send(pickle.dumps('no_such_room'))
                print(self.rooms.keys(), room_name)
                conn.close()
                return
        elif mode == 'create':
            if room_name in self.rooms.keys():
                conn.send(pickle.dumps('room_exists'))
                conn.close()
                return
            else:
                self.rooms[room_name] = []
                
        conn.send(pickle.dumps('all_good'))
        while self.running:
            try:
                data = pickle.loads(conn.recv(self.BUFFER_SIZE))
                name = data['name']
                master = data['master']
                room_name = data['room_name']
                ready = data['ready']
                existing = False
                for p in self.rooms[room_name]:
                    if p[0] == name:
                        existing = True
                        p[1] = ready
                        break
                else:
                    self.rooms.setdefault(room_name, []).append([name, ready, conn, addr])
                start = all([r[1] for r in self.rooms[room_name]])
                print(start)
                if start:
                    msg = 'game_begin'
                    conn.send(pickle.dumps(msg))
<<<<<<< HEAD
                    instance = GameInstance(room_name, self.rooms[room_name])
                    self.game_instances[room_name] = instance
                    if __name__ == "__main__":
                        threading.Thread(target=instance.create_thread, args=(name,)).start()
=======
                    if room_name not in self.game_instances.keys():
                        instance = GameInstance(room_name, self.rooms[room_name])
                        self.game_instances[room_name] = instance
                        if __name__ == "__main__":
                            print("CREATE ONCE")
                            threading.Thread(target=instance.create_thread).start()
>>>>>>> d5971fea5d549f76e757f0bfc3d83e3ae1fc9c3b
                    return True
                else:
                    players = []
                    for player in self.rooms[room_name]:
                        players.append(player[:2])
                    msg = pickle.dumps(players)
                    conn.send(msg)
            except:
                for player in self.rooms[room_name]:
                    if player[0] == name:
                        self.rooms[room_name].remove(player)
                        return
        conn.close()
    def collect_players():
        pass
    def remove(self, room):
        try:
            del self.rooms[room]
        except:
            print('Room Not found: %s' %room)

server = Server(BUFFER_SIZE)
threading.Thread(target=server.listen).start()
