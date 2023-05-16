import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


class Chain:
    def __init__(self, number):
        self.id = number
        self.resource = 100
        self.resource_list = []
        self.ride_list = []

    def __repr__(self):
        return str(self.id)


class Cassette:
    def __init__(self):
        self.resource = 100
        self.resource_list = []
        self.ride_list = []


class Transmission:
    def __init__(self, cassette: Cassette, list_of_chains: list):
        self.cassette = cassette
        self.chains = list_of_chains
        self.chain = None

    def ride(self, i):  # not sure if it`s ok to add external 'i' to here
        self.cassette.resource -= (0.0005 + 0.03 * (1 - self.chain.resource / 100)) * self.cassette.resource
        self.chain.resource -= (0.015 + 0.03 * (1 - self.cassette.resource / 100)) * self.chain.resource
        self.chain.ride_list.append(i)
        self.chain.resource_list.append(self.chain.resource)
        self.cassette.ride_list.append(i)
        self.cassette.resource_list.append(self.cassette.resource)

    def change_chain(self, chain):
        self.chain = chain

    def show_chain_status(self):
        # print(f"Current chain installed: {self.chain.number}")
        pass

    def show_resource_status(self):
        # print(f"cassette resource:{round(self.cassette.resource, 2)}, chain resource {round(self.chain.resource, 4)}")
        pass


class ListOfChains:
    def __init__(self):
        self.chains: list[Chain] = []

    def add_chains(self, chain_id: int):
        chain = Chain(number=chain_id)
        self.chains.append(chain)

    def auto_list_creation(self, quantity: int):
        for i in range(quantity):
            self.add_chains(i+1)
        return self.chains

    def __repr__(self):
        return "\n".join(map(str, self.chains))


fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.25)


axfreq = fig.add_axes([0.25, 0.05, 0.65, 0.03])
run_slider = Slider(
    ax=axfreq,
    label='Frequency [rides]',
    valmin=0.1,
    valmax=30,
    valinit=5,
)

axchain = fig.add_axes([0.25, 0.10, 0.3, 0.03])
chain_slider = Slider(
    ax=axchain,
    label='Chains [psc]',
    valmin=1,
    valmax=3,
    valinit=3,
    valstep=1
)


def run_model(runs: int, chains: int):
    list_of_chains = ListOfChains()
    list_of_chains.auto_list_creation(chains)
    cassette = Cassette()

    x = []
    y = cassette.resource_list

    transmission = Transmission(cassette, list_of_chains.chains)

    value = runs
    n = 0
    for i in range(1, 290):
        transmission.chain = list_of_chains.chains[n]
        transmission.ride(i)
        transmission.show_resource_status()
        x.append(i)
        try:
            if i % value == 0 and i >= value:
                n += 1
                if n > len(list_of_chains.chains) - 1:
                    n = 0
                transmission.change_chain(list_of_chains.chains[n])
                transmission.show_chain_status()
            if len(list_of_chains.chains) == 1:  # для одной цепи
                n = 0
                transmission.change_chain(list_of_chains.chains[n])
                transmission.show_chain_status()
        except ZeroDivisionError:
            print('Cannot devide by zero.')

    ax.clear()

    for chain in list_of_chains.chains:
        l, = ax.plot(cassette.ride_list, cassette.resource_list)
        l1, = ax.plot(chain.ride_list, chain.resource_list)

    fig.canvas.draw_idle()


run_model(5, 3)


def colorfunc(val):
    runs = int(run_slider.val)
    chains = int(chain_slider.val)

    run_model(runs, chains)


run_slider.on_changed(colorfunc)
chain_slider.on_changed(colorfunc)

plt.show()
