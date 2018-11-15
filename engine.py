import pygame, os

"""engine contains the Engine class, which should be 
extended by your main class (or cutsey named 'Game' class) 
where your own code goes. Ex.

class Game(Engine):

    def preload(self):
        #do something

    def loop(self):
        #do something each frame (for instance:)
        super().render(pygame.Surface(100, 100), (0, 0))

    def cleanup(self):
        #do some stuff when the game ends


game = Game()
game.start(screen_size=[800, 600], pygame.FULLSCREEN, )
"""

class Engine:

    font = None # TODO: this is janky and bad coding aaaaaa
    eventcache = None

    def start(self, screen_size, FULLSCREEN = 0, font_name='', font_size = 16):
        """This method is called to start the game. It sets up the game defaults
        and calls the following methods:
        1. preloading
        2. loop #(while super().running is True)
        3. cleanup
        
        At the end of each loop, it blits to screen all surfaces passed to the 
        engine via Engine.draw(Engine.RenderComponent), dropping frames if the 
        loop method is running slowly.
        """

        self.screen_size = screen_size

        pygame.init()

        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0)

        Engine.eventcache = EventCache()

        self.__screen = pygame.display.set_mode(self.screen_size, FULLSCREEN)
        self.__render_queue = []
        
        Engine.font = pygame.font.SysFont(font_name, font_size)# TODO: this is janky and bad coding aaaaaa

        self.fps = 60
        self.frame_count = 0
        self.running = True

        self.preload()

        clock = pygame.time.Clock()
        overtime = 0

        while self.running:
            start_time = pygame.time.get_ticks()
            self.loop()

            while len(self.__render_queue) > 0:
                if pygame.time.get_ticks() - start_time - overtime > 1000/self.fps:
                    self.__render_queue = []
                    break
                else: 
                    render_component = self.__render_queue.pop()
                    self.__screen.blit(render_component.get_image(), render_component.get_pos())
            
            self.frame_count +=1
            if self.frame_count == 1000: self.frame_count == 0

            pygame.display.flip()
            clock.tick(self.fps)
            overtime += clock.get_time() - 1000/self.fps

        self.cleanup()

    def render_later(self, renderable_component):
        self.__render_queue.insert(0, renderable_component)

    def preload(self):
        raise NotImplementedError("preload(self) must overridden by subclass")
    
    def loop(self):
        raise NotImplementedError("loop(self) must overridden by subclass")

    def cleanup(self):
        raise NotImplementedError("cleanup(self) must overridden by subclass")


class RenderableComponent:

    def get_image(self):
        raise NotImplementedError("get_image(self) must be overridden by subclass")

    def get_pos(self):
        raise NotImplementedError("get_pos(self) must be overriden by subclass")

    def update(self):
        raise NotImplementedError("update(self) must be overriden by subclass")

class EventCache:

    def __init__(self):
        self.__events = []
        self.__mouse_buttons = pygame.mouse.get_pressed()
        self.__mouse_buttons_lastframe = None

    def update(self):
        self.__events = pygame.event.get()
        self.__mouse_buttons_lastframe = self.__mouse_buttons
        self.__mouse_buttons = pygame.mouse.get_pressed()

    def key_down(self, key):
        for event in self.__events:
            if event.type == pygame.KEYDOWN and event.key == key:
                return True

        return False

    def key_up(self, key):
        for event in self.__events:
            if event.type == pygame.KEYUP and event.key == key:
                return True

        return False

    def mouse_pressed(self, button):
        return self.__mouse_buttons[button] and not self.__mouse_buttons_lastframe[button]

    def mouse_released(self, button):
        return not self.__mouse_buttons[button] and self.__mouse_buttons_lastframe[button]

    def mouse_long_pressed(self, button):
        return self.__mouse_buttons[button] and self.__mouse_buttons_lastframe[button]

class Button(RenderableComponent):

    def __init__(self, topleft = (0, 0), text = None, image = None):
        if text is None and image is None:
            raise Exception("either text of image must be a non-none object")

        if image is not None:
            self.__inactive_image = image
            self.__active_image = self.__inactive_image.copy()
            self.__active_image.set_alpha(200)

        elif text is not None:
            self.text = text #used in the update method
            self.__inactive_image = Engine.font.render(text, False, (255, 255, 255), (0, 0, 0))
            self.__active_image = Engine.font.render(text, False, (0, 0, 0), (255, 255, 255))
        
        self.__image = self.__inactive_image

        self.rect = self.__image.get_rect()
        self.rect.move_ip(topleft[0], topleft[1])

        self.__pressed = False

    def get_image(self):
        return self.__image

    def get_pos(self):
        return self.rect.topleft

    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if Engine.eventcache.mouse_long_pressed(0):
                self.__image = self.__inactive_image
            else:
                self.__image = self.__active_image

            if Engine.eventcache.mouse_released(0):
                self.__pressed = True
            else: self.__pressed = False
        else: self.__image = self.__inactive_image

    def is_pressed(self):
        return self.__pressed

