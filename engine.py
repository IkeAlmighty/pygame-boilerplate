import pygame

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

        self.font = pygame.font.SysFont(font_name, font_size)
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

    def render(self, renderable_component):
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