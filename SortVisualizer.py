import pygame
import random
import math
pygame.init()

class DrawInfo:
    BLACK = 0,0,0
    WHITE = 255,255,255
    GREEN = 0,255,0
    RED = 255,0,0
    BACKGROUND_COLOR = WHITE
    BLUE = 0,100,255

    GRADIENTS = [(128,128,128),(160,160,160),(192,192,192)]

    FONT = pygame.font.SysFont("Calibri",20)
    LARGE_FONT = pygame.font.SysFont("Calibri",30)
    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self,width,height,lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width,height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_list(lst)

    def set_list(self,lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.block_width = round((self.width-self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2

def gen_start_list(n,min_val,max_val):
    lst = []
    for _ in range(n):
        val = random.randint(min_val,max_val)
        lst.append(val)
    return lst

def draw(draw_info,sortingAlgoName,ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    if ascending:
        direction = "Ascending"
    else:
        direction = "Descending"

    title = draw_info.FONT.render((str(sortingAlgoName) + "- {}".format(direction)),1,draw_info.BLUE)
    draw_info.window.blit(title,(draw_info.width/2 - title.get_width()/2,5))

    controls = draw_info.FONT.render("R - Reset | Space - Start Sort | A - Ascending | D - Descending",1,draw_info.BLACK)
    draw_info.window.blit(controls,(draw_info.width/2 - controls.get_width()/2,45))

    sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort",1,draw_info.BLACK)
    draw_info.window.blit(sorting,(draw_info.width/2 - sorting.get_width()/2,75))
    
    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info,color_pos = {}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, draw_info.width - draw_info.SIDE_PAD,
                      draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window,draw_info.BACKGROUND_COLOR,clear_rect)
        

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GRADIENTS[i%3]

        if i in color_pos:
            color = color_pos[i]

        pygame.draw.rect(draw_info.window,color,(x,y,draw_info.block_width,draw_info.height))

    if clear_bg:
        pygame.display.update()

def bubble_sort(draw_info, ascending = True):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 -i):
            num1 = lst[j]
            num2 = lst[j+1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j+1] = lst[j+1],lst[j]
                draw_list(draw_info,{j:draw_info.GREEN, j+1:draw_info.RED}, True)
                yield True
    return lst

def insertion_sort(draw_info, ascending = True):
    lst = draw_info.lst
    for i in range(1,len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i>0 and lst[i-1]> current and ascending
            descending_sort = i>0 and lst[i-1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i-1]
            i = i - 1
            lst[i] = current
            draw_list(draw_info,{i:draw_info.GREEN,i-1:draw_info.RED},True)
            yield True
    return lst

def main():
    running = True
    clock = pygame.time.Clock()
    
    n = 100
    min_val = 0
    max_val = 100

    lst = gen_start_list(n,min_val,max_val)
    draw_info = DrawInfo(800,600,lst)
    sorting = False
    ascending = True

    sortingAlgo = bubble_sort
    sortingAlgoName = "Bubble Sort"
    sortingAlgoGen = None

    while running:
        clock.tick(2000)

        if sorting:
            try:
                next(sortingAlgoGen)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sortingAlgoName, ascending)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:
                lst = gen_start_list(n,min_val,max_val)
                draw_info.set_list(lst)
                sorting = False

            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sortingAlgoGen = sortingAlgo(draw_info,ascending)
                
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_i and not sorting:
                sortingAlgo = insertion_sort
                sortingAlgoName = "Insertion Sort"
            elif event.key == pygame.K_b and not sorting:
                sortingAlgo = bubble_sort
                sortingAlgoName = "Bubble Sort"
                
    pygame.quit()
if __name__ == "__main__":
    main()


        
        
        
