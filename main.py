import random
from agent import Client


def imprime_estado_agentes(clientes:dict):
    for cliente in clientes.values():
        print(cliente.__str__())


def main():
    num_agents = 20  # Number of agents

    clientes = {}  # Dictionary to store the agents
    list_onshop = []  # List of customers in the shop
    list_outshop = []  # List of customers outside the shop
    queue_shop = []  # Queue for customers in queues inside the shop

    # Create the agents with random attributes and add them to the dictionary
    for i in range(1, num_agents + 1):
        items = random.randint(6, 10)
        items_threshold = random.randint(2, 6)
        waiting_time_threshold = random.randint(2, 10)

        cliente = Client(i, items, items_threshold, waiting_time_threshold)
        clientes[i] = cliente
        list_onshop.append(i)

    time_limit = 10000  # Set the time limit for the simulation

    # Simulation loop
    for tick in range(time_limit):
        if tick % 100 == 0:
            imprime_estado_agentes(clientes)

        # Update the tick for each agent
        for cliente in clientes.values():
            cliente.increment_tick()
            # Check if agent has completed shopping
            if cliente.get_items() == 0:
                cliente.set_state("outshop")
                list_onshop.remove(cliente.get_id())
                list_outshop.append(cliente.get_id())


            # Check if agent should join a queue
            if (
                cliente.get_state() == "inshop"
                and cliente.get_items() <= cliente.get_items_threshold()
                and len(queue_shop) + len(list_onshop) < num_agents
            ):
                if random.random() < 0.5:  # Randomly decide whether to join the queue or not
                    cliente.set_state("queue")
                    queue_shop.append(cliente.get_id())
                    cliente.increment_nr_times_queue()
                    list_onshop.remove(cliente.get_id())

        if len(list_onshop) < len(queue_shop) and (len(list_outshop) + len(list_onshop) != len(num_agents)):
            break

    # End of simulation
    imprime_estado_agentes(clientes)
    onshop_update(clientes, list_onshop, list_outshop, queue_shop)
    remove_from_queue(clientes, queue_shop, list_onshop)
    quit_queue(clientes, queue_shop, list_onshop)

    print("***************************")
    print("Final state")
    print(f"Nr. Ticks: {time_limit}")
    print(f"Nr. Agents: {num_agents}")
    print(f"On queues: {len(queue_shop)}")
    print(f"On shopping: {len(list_onshop)}")
    print(f"Out of the shop: {len(list_outshop)}")
    mean_waiting_time = sum(cliente.get_waiting_time() for cliente in clientes.values()) / num_agents
    print(f"Mean waiting time: {mean_waiting_time} ticks")
    total_nr_times_queues = sum(cliente.nr_times_queues for cliente in clientes.values())
    percentage_dropouts = (sum(cliente.nr_drop_outs for cliente in clientes.values()) / total_nr_times_queues) * 100 if total_nr_times_queues != 0 else 0
    print(f"Percentage of drop-outs: {percentage_dropouts:.1f}%")


def onshop_update(clientes:dict, list_onshop:list, list_outshop:list, queue_shop):
        for cliente_id in list_onshop:
            cliente = clientes[cliente_id]
            decrease_items(clientes, list_onshop)
            if cliente.get_items() == 0:
                no_items(clientes, list_onshop, list_outshop)
            elif cliente.get_items() <= cliente.get_items_threshold():
                go_queue(clientes, list_onshop, queue_shop)


def decrease_items(clientes, list_onshop):
        for cliente_id in list_onshop:
            cliente = clientes[cliente_id]
            if cliente.get_items() > 0:
                items_to_decrease = random.randint(1, cliente.get_items())
                cliente.reduce_item(items_to_decrease)

def no_items(clientes, list_onshop, list_outshop):
        for cliente_id in list_onshop:
            cliente = clientes[cliente_id]
            if cliente.get_items() == 0:
                cliente.set_state("outshop")
                list_onshop.remove(cliente_id)
                list_outshop.append(cliente_id)

def go_queue(clientes, list_onshop, queue_shop):
        for cliente_id in list_onshop:
            cliente = clientes[cliente_id]
            if cliente.get_items() <= cliente.get_items_threshold():
                cliente.set_state("queue")
                queue_shop.append(cliente_id)

def remove_from_queue(clientes, queue_shop, list_onshop):
        if len(queue_shop) > 0:
            cliente_id = queue_shop.pop(0)
            cliente = clientes[cliente_id]
            if cliente.get_tick() % 2 == 0:
                additional_items = random.randint(0, 4)
                cliente.set_items(cliente.get_items() + additional_items)
                cliente.set_state("onshop")
                list_onshop.append(cliente_id)

def quit_queue(clientes, queue_shop, list_onshop):
        for cliente_id in queue_shop:
            cliente = clientes[cliente_id]
            cliente.increment_waiting_time(1)
            waiting_time_threshold = cliente.get_waiting_time_threshold()
            if waiting_time_threshold is not None and cliente.get_waiting_time() > waiting_time_threshold:
                cliente.set_state("onshop")
                cliente.reset_waiting_time()
                queue_shop.remove(cliente_id)
                list_onshop.append(cliente_id)


if __name__ == "__main__":
    main()
