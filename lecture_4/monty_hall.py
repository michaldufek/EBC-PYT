import random

def monty_hall(simulations=1000, change_door=True):
    wins = 0
    for _ in range(simulations):
        # Nastavení - za jedněmi dveřmi je auto (True), za ostatními kozy (False)
        doors = [False, False, False]
        car_position = random.randint(0, 2)
        doors[car_position] = True
        
        # Vyberte si dveře
        choice = random.randint(0, 2)
        
        # Moderátor otevře dveře s kozou
        remaining_doors = [i for i in range(3) if i != choice and doors[i] == False]
        opened_door = random.choice(remaining_doors)
        
        # Rozhodněte se, zda změníte svůj výběr
        if change_door:
            remaining_doors = [i for i in range(3) if i != choice and i != opened_door]
            choice = remaining_doors[0]
        
        # Zjistěte, zda jste vyhráli
        if doors[choice]:
            wins += 1
            
    return wins / simulations

if __name__ == "__main__":
    # Simulujte Monty Hallův problém 1000 krát a vypište pravděpodobnosti výhry
    print("Pravděpodobnost výhry po změně výběru:", monty_hall(1000, True))
    print("Pravděpodobnost výhry bez změny výběru:", monty_hall(1000, False))
