import pygame, math, random, time

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()
pygame.init()

crunch_sound = pygame.mixer.Sound('sounds/crunch.wav')

cookie_img = pygame.image.load('sprites/cookie.png')
backgroundCookie = pygame.image.load('sprites/backgroundCookie.png')

wooden_bar = pygame.image.load('sprites/wooden_bar.png')
upgrades_wooden_bar = pygame.image.load('sprites/upgrades_wooden_bar.png')
buildings_wooden_bar = pygame.image.load('sprites/buildings_wooden_bar.png')
wooden_background = pygame.image.load('sprites/wooden_background.png')


cursor_img = pygame.image.load('sprites/cursor_img.png')
grandma_img = pygame.image.load('sprites/grandma_img.png')
farm_img = pygame.image.load('sprites/farm_img.png')
mine_img = pygame.image.load('sprites/mine_img.png')
factory_img = pygame.image.load('sprites/factory_img.png')
bank_img = pygame.image.load('sprites/bank_img.png')
temple_img = pygame.image.load('sprites/temple_img.png')
wizard_tower_img = pygame.image.load('sprites/wizard_tower_img.png')

cursor_icon = pygame.image.load('sprites/icons/cursor_icon.png')
grandma_icon = pygame.image.load('sprites/icons/grandma_icon.png')
farm_icon = pygame.image.load('sprites/icons/farm_icon.png')
mine_icon = pygame.image.load('sprites/icons/mine_icon.png')
factory_icon = pygame.image.load('sprites/icons/factory_icon.png')
bank_icon = pygame.image.load('sprites/icons/bank_icon.png')
temple_icon = pygame.image.load('sprites/icons/temple_icon.png')
wizard_tower_icon = pygame.image.load('sprites/icons/wizard_tower_icon.png')

'''Upgrade sprites'''
upgrade_background_frame = pygame.image.load('sprites/upgrades/upgrade_background_frame.png')

cursor_upgrade_img_1 = pygame.image.load('sprites/upgrades/cursor_upgrade_img_1.png')
cursor_upgrade_img_2 = pygame.image.load('sprites/upgrades/cursor_upgrade_img_2.png') 
grandma_upgrade_img_1 = pygame.image.load('sprites/upgrades/grandma_upgrade_img_1.png')
farm_upgrade_img_1 = pygame.image.load('sprites/upgrades/farm_upgrade_img_1.png')
mine_upgrade_img_1 = pygame.image.load('sprites/upgrades/mine_upgrade_img_1.png')
factory_upgrade_img_1 = pygame.image.load('sprites/upgrades/factory_upgrade_img_1.png')
bank_upgrade_img_1 = pygame.image.load('sprites/upgrades/bank_upgrade_img_1.png')
temple_upgrade_img_1 = pygame.image.load('sprites/upgrades/temple_upgrade_img_1.png')
wizard_tower_upgrade_img_1 = pygame.image.load('sprites/upgrades/wizard_tower_upgrade_img_1.png')

mouse_upgrade_img_1 = pygame.image.load('sprites/upgrades/mouse_upgrade_img_1.png')


background_img = pygame.image.load('sprites/background_img.png')
building_display_background = pygame.image.load('sprites/building_display_background.png')


class CookieObj:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.length = 250
        self.height = 250
        
        self.animation_state = 0
    def draw(self):
        if self.animation_state + 0.1 > time.time():
            size_change = (time.time() - self.animation_state) * 2 + 0.8
            cookie_img_scaled = pygame.transform.scale(cookie_img, (int(size_change * self.length), int(size_change * self.height)))
            window.blit(cookie_img_scaled, (cookie_img_scaled.get_rect(  center=(int(self.x + self.length/2), int(self.y + self.height/2))  )))
        else:
            window.blit(cookie_img, (cookie_img.get_rect(  center=(int(self.x + self.length/2), int(self.y + self.height/2))  )))
    def collidepoint(self, point):
        return pygame.Rect(self.x, self.y, self.length, self.height).collidepoint(point)
     
class BackgroundCookie:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.length = 40
        self.height = 40
        
    def animate(self, list_of_cookies):
        self.y += 5
        if self.y > window_height:
            list_of_cookies.remove(self)
            
    def draw(self):
        window.blit(backgroundCookie, (self.x, self.y))
     
class CookieDisplayObj:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.length = 100
        self.height = 100
        
        self.score = 0
                
    def draw(self, score, user_cps):
        font = pygame.font.Font('Font/ChelseaMarket-Regular.ttf', 24)
        small_font = pygame.font.Font('Font/ChelseaMarket-Regular.ttf', 15)
        
        text = font.render('{} cookies'.format(int( format_number(score) )), True, WHITE)
        cps = small_font.render('per second: {}'.format(int( format_number( format_number(user_cps) ))), True, WHITE)
        window.blit( text, (  text.get_rect(center=(int(self.x + self.length / 2), int(self.y + self.height / 2)))  ) )
        window.blit( cps, (  cps.get_rect(center=(int(self.x + self.length / 2), int(self.y + self.height / 2) + 20))  ) )

class Building:
    def __init__(self, name, x, y, image, icon, base_cost, increase_per_purchase, cps):
        self.x = x
        self.y = y
        self.length = 300
        self.height = 64
        
        self.name = name
        self.image = image
        self.icon = icon
        
        self.quantity = 0
        self.base_cost = base_cost
        self.increase_per_purchase = increase_per_purchase
        self.cps = cps
        
        self.created = 0
    def collidepoint(self, point):
        return pygame.Rect(self.x, self.y, self.length, self.height).collidepoint(point)
    def getTotalCost(self):
        return int(self.base_cost * self.increase_per_purchase**(self.quantity))
    
    def draw(self, solid=True):
        
        store_cost_font = pygame.font.Font('Font/ChelseaMarket-Regular.ttf', 17)
        store_quantity_font = pygame.font.Font('Font/ChelseaMarket-Regular.ttf', 36)
        
        icon = self.image
        cost = store_cost_font.render('{}'.format( format_number(self.getTotalCost()) ), True, LIGHT_GREEN)
        quantity = store_quantity_font.render('{}'.format(self.quantity), True, GRAY)
        if solid == False:    
            icon.set_alpha(100)
        else:
            icon.set_alpha(255)
        window.blit(icon, (self.x, self.y))
        window.blit(cost, (self.x + 85, self.y + self.height - 30))
        window.blit(quantity, (self.x + self.length - 40, self.y + 10))
        
    def drawDisplayBox(self):
        building_font = pygame.font.Font('Font/ChelseaMarket-Regular.ttf', 20)
        building_title = building_font.render('{}'.format(self.name), True, WHITE)
        
        description_font = pygame.font.Font('Font/ChelseaMarket-Regular.ttf', 12)
        production = description_font.render('Each {} produces {:.1f} cookies per second'.format(self.name, self.cps), True, WHITE)
        quantity = description_font.render('You have {} {}s producing {:.1f} cookies per second'.format(self.quantity, self.name, self.cps * self.quantity), True, WHITE)
        created = description_font.render('{}s have created {} cookies so far'.format(self.name, math.floor(self.created)), True, WHITE)
        
        x_pos = self.x - 380
        y_pos = pygame.mouse.get_pos()[1] - 72
        
        window.blit(building_display_background, (x_pos, y_pos))
        window.blit(self.icon, (x_pos + 3, y_pos + 3))
        window.blit(building_title, (x_pos + 43, y_pos + 3))
        
        '''Description'''
        space_between_lines = 16
        window.blit(production, (x_pos + 10, y_pos + 50))
        window.blit(quantity, (x_pos + 10, y_pos + 50 + space_between_lines*1))
        window.blit(created, (x_pos + 10, y_pos + 50 + space_between_lines*2))
        
    def addUpgrade(self):
        I = 0
        II = 9
        III = 24
        if self.name == 'Cursor':
            if self.quantity == I:
                list_of_upgrades.append(Upgrade('Reinforced Index Finger I', cost=self.getTotalCost()*10, upgrade=self.name))
                list_of_upgrades.append(Upgrade('Double Click', cost=1000, upgrade='Mouse'))
            elif self.quantity == II:
                list_of_upgrades.append(Upgrade('Arthritis prevention cream', cost=self.getTotalCost()*10, upgrade=self.name))
                list_of_upgrades.append(Upgrade('Double Click', cost=2000, upgrade='Mouse'))
            elif self.quantity == III:
                list_of_upgrades.append(Upgrade('Ambidextrous', cost=self.getTotalCost()*10, upgrade=self.name))
                list_of_upgrades.append(Upgrade('Double Click', cost=4000, upgrade='Mouse'))
        elif self.name == 'Grandma':
            if self.quantity == I:
                list_of_upgrades.append(Upgrade('Forwards from grandma', cost=self.getTotalCost()*10, upgrade=self.name))
            elif self.quantity == II:
                list_of_upgrades.append(Upgrade('Steel-plated rolling pins', cost=self.getTotalCost()*10, upgrade=self.name))
            elif self.quantity == III:
                list_of_upgrades.append(Upgrade('Lubricated dentures', cost=self.getTotalCost()*10, upgrade=self.name))                
        elif self.name == 'Farm':
            if self.quantity == I:
                list_of_upgrades.append(Upgrade('Cheap hoes', cost=self.getTotalCost()*10, upgrade=self.name))
            elif self.quantity == II:
                list_of_upgrades.append(Upgrade('Fertilizer', cost=self.getTotalCost()*10, upgrade=self.name))
            elif self.quantity == III:
                list_of_upgrades.append(Upgrade('Lubricated dentures', cost=self.getTotalCost()*10, upgrade=self.name))
        elif self.name == 'Mine':
            if self.quantity == I:
                list_of_upgrades.append(Upgrade('Sugar gas', cost=self.getTotalCost()*10, upgrade=self.name))
            elif self.quantity == II:
                list_of_upgrades.append(Upgrade('Megadrill', cost=self.getTotalCost()*10, upgrade=self.name))
            elif self.quantity == III:
                list_of_upgrades.append(Upgrade('Ultradrill', cost=self.getTotalCost()*10, upgrade=self.name))
        elif self.name == 'Factory':
            if self.quantity == I:
                list_of_upgrades.append(Upgrade('Sturdier conveyor belts', cost=self.getTotalCost()*10, upgrade=self.name))
            elif self.quantity == II:
                list_of_upgrades.append(Upgrade('Child labor', cost=self.getTotalCost()*10, upgrade=self.name))
            elif self.quantity == III:
                list_of_upgrades.append(Upgrade('Sweatshop', cost=self.getTotalCost()*10, upgrade=self.name))
        elif self.name == 'Bank':
            if self.quantity == I:
                list_of_upgrades.append(Upgrade('Taller tellers', cost=self.getTotalCost()*10, upgrade=self.name))
            elif self.quantity == II:
                list_of_upgrades.append(Upgrade('Credit cards', cost=self.getTotalCost()*10, upgrade=self.name))
            elif self.quantity == III:
                list_of_upgrades.append(Upgrade('Acid-proof vaults', cost=self.getTotalCost()*10, upgrade=self.name))
        elif self.name == 'Temple':
            if self.quantity == I:
                list_of_upgrades.append(Upgrade('Golden idols', cost=self.getTotalCost()*10, upgrade=self.name))
            elif self.quantity == II:
                list_of_upgrades.append(Upgrade('Sacrifices', cost=self.getTotalCost()*10, upgrade=self.name))
            elif self.quantity == III:
                list_of_upgrades.append(Upgrade('Delicious blessing', cost=self.getTotalCost()*10, upgrade=self.name))
        elif self.name == 'Wizard':
            if self.quantity == I:
                list_of_upgrades.append(Upgrade('Pointier hats', cost=self.getTotalCost()*10, upgrade=self.name))
            elif self.quantity == II:
                list_of_upgrades.append(Upgrade('Beardlier beards', cost=self.getTotalCost()*10, upgrade=self.name))
            elif self.quantity == III:
                list_of_upgrades.append(Upgrade('Ancient grimoires', cost=self.getTotalCost()*10, upgrade=self.name))

                
class Upgrade:
    def __init__(self, name, cost, upgrade):
        self.name = name
        self.cost = cost

        self.x = 700
        self.y = 16
        self.length = 60
        self.height = 60
        
        self.upgrade = upgrade
        
        '''Sets images'''
        if upgrade == 'Mouse':
            self.image = mouse_upgrade_img_1
        elif upgrade == 'Cursor':
            randomNumber = random.randint(0, 1)
            if randomNumber == 0:
                self.image = cursor_upgrade_img_1
            else:
                self.image = cursor_upgrade_img_2
        elif upgrade == 'Grandma':
            self.image = grandma_upgrade_img_1
        elif upgrade == 'Farm':
            self.image = farm_upgrade_img_1
        elif upgrade == 'Mine':
            self.image = mine_upgrade_img_1
        elif upgrade == 'Factory':
            self.image = factory_upgrade_img_1
        elif upgrade == 'Bank':
            self.image = bank_upgrade_img_1
        elif upgrade == 'Temple':
            self.image = temple_upgrade_img_1
        elif upgrade == 'Wizard Tower':
            self.image = wizard_tower_upgrade_img_1
            
    def collidepoint(self, point):
        return pygame.Rect(self.x, self.y, self.length, self.height).collidepoint(point)
    
    def draw(self, solid=True):
        icon = self.image
        frame = upgrade_background_frame
        if solid == False:    
            icon.set_alpha(100)
            frame.set_alpha(100)
        else:
            icon.set_alpha(255)
            frame.set_alpha(255)
        window.blit(frame, (self.x, self.y))
        window.blit(icon, (icon.get_rect(center=(int(self.x + self.length / 2), int(self.y + self.height / 2)))))
    
    def drawDisplayBox(self):
        upgrade_font = pygame.font.Font('Font/ChelseaMarket-Regular.ttf', 20)
        upgrade_title = upgrade_font.render('{}'.format(self.name), True, WHITE)
        
        cost_font = pygame.font.Font('Font/ChelseaMarket-Regular.ttf', 14)
        cost = cost_font.render('Cost: {}'.format( format_number(self.cost) ), True, LIGHT_GREEN)
        
        description_font = pygame.font.Font('Font/ChelseaMarket-Regular.ttf', 12)
        description = description_font.render('{}s are twice as efficient.'.format(self.upgrade), True, WHITE)
        
        x_pos = 700 - 380
        y_pos = pygame.mouse.get_pos()[1] - 72
        if y_pos < 0:
            y_pos = 0
        
        window.blit(building_display_background, (x_pos, y_pos))
        window.blit(self.image, (x_pos + 3, y_pos + 3))
        window.blit(upgrade_title, (x_pos + 43, y_pos + 3))
        
        '''Cost'''
        window.blit(cost, (x_pos + 10, y_pos + 50))
        
        '''Description'''
        space_between_lines = 16
        window.blit(description, (x_pos + 10, y_pos + 50 + space_between_lines))
        
    def upgradeBuilding(self, list_of_buildings):
        if self.upgrade == 'Mouse':
            user.click_multiplier *= 2
        elif self.upgrade == 'Cursor':
            cursor.cps *= 2
        elif self.upgrade == 'Grandma':
            grandma.cps *= 2
        elif self.upgrade == 'Farm':
            farm.cps *= 2
        elif self.upgrade == 'Mine':
            mine.cps *= 2
        elif self.upgrade == 'Factory':
            factory.cps *= 2
        elif self.upgrade == 'Bank':
            bank.cps *= 2
        elif self.upgrade == 'Temple':
            temple.cps *= 2
        elif self.upgrade == 'Wizard Towers':
            wizard_tower.cps *= 2
            
class Player:
    def __init__(self):
        self.score = 0
        self.click_multiplier = 1
        self.total_cps = 0
    def updateTotalCPS(self, list_of_buildings):
        global timer, n_of_cookies
        
        self.total_cps = 0
        for building in list_of_buildings:
            self.total_cps += building.cps * building.quantity
        '''Updates number of falling cookies'''
        timer = 0
        if self.total_cps > 100000:
            n_of_cookies = 6
        elif self.total_cps > 10000:
            n_of_cookies = 8
        elif self.total_cps > 1000:
            n_of_cookies = 9
        elif self.total_cps > 100:
            n_of_cookies = 10
        elif self.total_cps > 10:
            n_of_cookies = 11
        elif self.total_cps > 0:
            n_of_cookies = 15
        
def format_number(n):
    if n >= 1000000000:
        if (n / 1000000000 )% 1 == 0:
            n = '{:.0f} billion'.format(n / 1000000000)
        else:
            n = '{:.2f} billion'.format(n / 1000000000)
    elif n >= 1000000:
        if (n / 1000000) % 1 == 0:
            n = '{:.0f} million'.format(n / 1000000) 
        else:
            n = '{:.2f} million'.format(n / 1000000)
    return n

def draw():
    global timer
    
    '''Draw background'''
    window.blit(background_img, (0, 0))
    window.blit(wooden_bar, (684, 0))
    window.blit(wooden_background, (700, 0))
    
    '''Draws falling cookies'''
    if timer == n_of_cookies:
        list_of_falling_cookies.append(BackgroundCookie(random.randint(0, 400), 0))
        timer = 0
    else:
        timer += 1
    for falling_cookie in list_of_falling_cookies:
        falling_cookie.draw()
        falling_cookie.animate(list_of_falling_cookies)
    
    '''Draws cookie and cookie display'''
    cookie.draw()
    cookie_display.draw(user.score, user.total_cps)
    
    '''Draws clicked cookies'''
    for falling_cookie in list_of_clicked_cookies:
        falling_cookie.animate(list_of_clicked_cookies)
        falling_cookie.draw()
    
    '''Draw Buildings'''
    for building in list_of_buildings:
        if user.score >= building.getTotalCost():
            building.draw(solid=True)
        else:
            building.draw(solid=False)
        
            '''Adds cookies made through building'''
        user.score += building.quantity * building.cps * .01
        building.created += building.quantity * building.cps * .01
        
        '''Draws building stats if mouse hover'''
        if building.collidepoint(pygame.mouse.get_pos()):
            building.drawDisplayBox()
    
    '''Draw upgrades'''
    for i in range(0, len(list_of_upgrades)):
        
        upgrade = list_of_upgrades[i]
        '''Sets position of upgrade'''
        upgrade.x = upgrades_x + (i % 5) *60
        upgrade.y = upgrades_y + (i // 5) * 60
        
        '''Draws solid/transparent'''
        if user.score >= upgrade.cost:
            upgrade.draw(solid=True)
        else:
            upgrade.draw(solid=False)
        
        '''Draws upgrade stats if mouse hover'''
        if upgrade.collidepoint(pygame.mouse.get_pos()):
            upgrade.drawDisplayBox()

    '''Draws wooden bars'''
    window.blit(upgrades_wooden_bar, (700, 0))
    window.blit(buildings_wooden_bar, (700, store_y - 16))

'''----------------------------------------------------------------------------------'''
cookie = CookieObj(100, 100)
cookie_display = CookieDisplayObj(180, 0)

n_of_cookies = -1
list_of_falling_cookies = []
timer = 0

list_of_clicked_cookies = []


'''Upgrades'''

upgrades_x = 700
upgrades_y = 16

list_of_upgrades = []



'''Buildings'''
store_y = 212
cursor = Building('Cursor', 700, store_y, cursor_img, cursor_icon, base_cost=15, increase_per_purchase=1.15, cps=0.1)
grandma = Building('Grandma', 700, store_y + 64*1, grandma_img, grandma_icon, base_cost=100, increase_per_purchase=1.15, cps=1)
farm = Building('Farm', 700, store_y + 64*2, farm_img, farm_icon, base_cost=1100, increase_per_purchase=1.15, cps=8)
mine = Building('Mine', 700, store_y + 64*3, mine_img, mine_icon, base_cost=12000, increase_per_purchase=1.15, cps=47)
factory = Building('Factory', 700, store_y + 64*4, factory_img, factory_icon, base_cost=130000, increase_per_purchase=1.15, cps=260)
bank = Building('Bank', 700, store_y + 64*5, bank_img, factory_icon, base_cost=1400000, increase_per_purchase=1.15, cps=1400)
temple = Building('Temple', 700, store_y + 64*6, temple_img, temple_icon, base_cost=20000000, increase_per_purchase=1.15, cps=7800)
wizard_tower = Building('Wizard Tower', 700, store_y + 64*7, wizard_tower_img, wizard_tower_icon, base_cost=330000000, increase_per_purchase=1.15, cps=311080)

list_of_buildings = [cursor, grandma, farm, mine, factory, bank, temple, wizard_tower]



user = Player()

window_length = 1000
window_height = 600

DARK_BLUE = (51, 90, 114)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GREEN = (0, 255, 0)
GRAY = (155, 155, 155)

window = pygame.display.set_mode((window_length, window_height))


main = True
timer = 0

while main == True:
    
    pygame.time.delay(10)
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            main = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            '''Click Cookie'''
            if cookie.collidepoint(mouse_pos):
                user.score += 1 * user.click_multiplier

                
                cookie.animation_state = time.time()
                crunch_sound.play()
                '''Draws new falling cookie'''
                list_of_clicked_cookies.append( BackgroundCookie(pygame.mouse.get_pos()[0] - 20, pygame.mouse.get_pos()[1] - 20) )
                
                '''Buy Buildings'''
            for building in list_of_buildings:
                if building.collidepoint(mouse_pos) and user.score >= building.getTotalCost():
                    '''Unlock Upgrades'''
                    building.addUpgrade()
                    
                    user.score -= building.getTotalCost()
                    building.quantity += 1
                    user.updateTotalCPS(list_of_buildings)
                    
                '''Buy Upgrades'''        
            for upgrade in list_of_upgrades:
                if upgrade.collidepoint(mouse_pos) and user.score >= upgrade.cost:
                    user.score -= upgrade.cost
                    upgrade.upgradeBuilding(list_of_buildings)
                    list_of_upgrades.remove(upgrade)
                    user.updateTotalCPS(list_of_buildings)
                    
    if 700 < pygame.mouse.get_pos()[0] < 1000:
        if store_y < pygame.mouse.get_pos()[1] < store_y + 50:
            '''Scroll up store menu'''
            if list_of_buildings[0].y < store_y:
                for building in list_of_buildings:
                    building.y += 4
                    '''Make building appear from view if hidden'''
                    if store_y - 4 - 400 <= building.y < store_y - 400: 
                        building.y += 400
            
            '''Scroll down store menu'''
        elif 550 < pygame.mouse.get_pos()[1] < 600:
            for building in list_of_buildings:
                building.y -= 4
                '''Make building disappear from view once scrolled past'''
                if store_y - 4 <= building.y < store_y:
                    building.y -= 400
    
    draw()
    pygame.display.update()

pygame.quit()
