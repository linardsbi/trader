import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import sys, asyncio
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from watch_prices import Watcher

matplotlib.use('TKAgg')
loop = asyncio.get_event_loop()

class DynamicChart:
    def __init__(self) -> None:
        self.prev_changes = []
        self.fig, self.ax = plt.subplots()
        self.win = self.fig.canvas.manager.window
        self.watch = Watcher()
        self.initialized = False

        self.title = "Graph"
        self.xlabel = "X axis"
        self.ylabel = "Y axis"
        self.annotated = False

    
    def set_options(self, **kwargs):
        """ 
        Valid options:
        :param str title: Chart title
        :param str xlabel: x label
        :param str ylabel: y label
        :param bool annotated: Bool value for adding annotations to bars
        """

        vars(self).update(kwargs)

        
    def show(self) -> None:
        import matplotlib.animation as ani
        animator = ani.FuncAnimation(self.fig, self.__anim_wrapper, interval=3000)
        plt.show()

    def __anim_wrapper(self, i):
        loop.run_until_complete(self.animated_barplot(i))

    async def animated_barplot(self, i):
        def autolabel(rects):
            for rect in rects:
                height = rect.get_height()
                self.ax.annotate('{:.2f}%'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')

        changes = await self.watch.get_changed_coins(change_threshold=5.0)

        if not changes and self.initialized: return
        
        symbols = [price["symbol"] for price in changes]
        percent_changes = [price["change"] for price in changes]

        y_pos = np.arange(len(symbols))

        self.ax.clear()
        # TODO: fix overlap by changing the same bar on update
        self.rects = plt.bar(y_pos, percent_changes, align='center', color="blue")
        plt.xticks(y_pos, symbols)
        plt.ylabel(self.ylabel)
        plt.xlabel(self.xlabel)
        plt.title(self.title)
        autolabel(self.rects)
        self.initialized = True
        self.prev_changes = changes

# async def main():

chart = DynamicChart()
chart.set_options(title='Coin price changes in % \n', xlabel="Coins", ylabel=r"% change", annotated=True)
chart.show()


# loop.run_until_complete(main())


