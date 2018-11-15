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

    font = pygame.font.SysFont(font_name, font_size)

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

        self.__screen = pygame.display.set_mode(self.screen_size, FULLSCREEN)
        self.__render_queue = []
        
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
        raise NotImplementedError("preload must overridden by subclass")
    
    def loop(self):
        raise NotImplementedError("loop must overridden by subclass")

    def cleanup(self):
        raise NotImplementedError("cleanup must overridden by subclass")


class RenderableComponent:

    def get_image(self):
        raise NotImplementedError("get_image must be overridden by subclass")

    def get_pos(self):
        raise NotImplementedError("get_pos must be overriden by subclass")

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

class Button(engine.RenderableComponent):

    def __init__(self, topleft, text = None, image = None):
        if text is None and image is None:
            raise Exception("either text of image must be a non-none object")
        
        self.__topleft = topleft

        if image is not None:
            self.image = image
            self.rect = image.get_rect()
            self.rect.move_ip(self.__topleft[0], self.__topleft[1])

        elif text is not None:
            self.image = Engine.font.render(text, False, (255, 255, 255), (0, 0, 0))

    def get_image(self):
        return self.image

    def get_pos(self):
        return self.pos