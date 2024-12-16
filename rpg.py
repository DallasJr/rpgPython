import random

class Character:
    def __init__(self, name, level=1, hp=100, attack=10, defense=5):
        self.name = name
        self.level = level
        self.hp = hp
        self.max_hp = hp
        self.base_attack = attack
        self.attack = attack
        self.defense = defense
        self.xp = 0
        self.inventory = ['Knife']
        self.equipped_weapon = 'Knife'

    def gain_xp(self, amount):
        self.xp += amount
        if self.xp >= self.level * 100:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.hp = self.max_hp = self.hp + 20
        self.base_attack += 5
        self.defense += 3
        print(f"{self.name} leveled up! Now at level {self.level}.")

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0
        print(f"{self.name} took {amount} damage! HP: {self.hp}/{self.max_hp}")

    def heal(self, amount):
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        print(f"{self.name} healed {amount} HP! HP: {self.hp}/{self.max_hp}")

    def is_alive(self):
        return self.hp > 0

    def show_stats(self):
        print("\nPlayer Stats:")
        print(f"Name: {self.name}")
        print(f"Level: {self.level}")
        print(f"HP: {self.hp}/{self.max_hp}")
        print(f"Base Attack: {self.base_attack}")
        print(f"Attack with {self.equipped_weapon}: {self.attack}")
        print(f"Defense: {self.defense}")
        print(f"XP: {self.xp}/{self.level * 100} XP to next level")
        print(f"Inventory: {', '.join(self.inventory)}")
        print(f"Equipped Weapon: {self.equipped_weapon}\n")

    def equip_weapon(self, weapon):
        self.equipped_weapon = weapon
        if weapon == 'Knife':
            self.attack = self.base_attack + 5
        elif weapon == 'Sword':
            self.attack = self.base_attack + 10
        print(f"{self.name} equipped the {weapon}. Attack is now {self.attack}.")

class Monster:
    def __init__(self, name, level):
        self.name = name
        self.level = level
        self.hp = 50 + level * 10
        self.attack = 5 + level * 2
        self.defense = 3 + level * 2

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0
        print(f"{self.name} took {amount} damage! HP: {self.hp}")

    def is_alive(self):
        return self.hp > 0

class Game:
    def __init__(self):
        self.player = None
        self.map_size = (30, 30)
        self.position = (29, 0)
        self.locations = {
            (29, 0): "You are at the edge of the forest, ready to explore.",
            (28, 0): "You are at the edge of the forest, ready to explore.",
            (27, 0): "You are at the edge of the forest, ready to explore.",
            (26, 0): "You are at the edge of the forest, ready to explore.",
            (29, 1): "You are at the edge of the forest, ready to explore.",
            (28, 1): "You are at the edge of the forest, ready to explore.",
            (27, 1): "You are at the edge of the forest, ready to explore.",
            (26, 1): "You are at the edge of the forest, ready to explore.",
            (20, 5): "A small clearing appears between the trees.",
            (19, 5): "A small clearing appears between the trees.",
            (18, 5): "A small clearing appears between the trees.",
            (17, 5): "A small clearing appears between the trees.",
            (20, 6): "A small clearing appears between the trees.",
            (19, 6): "A small clearing appears between the trees.",
            (18, 6): "A small clearing appears between the trees.",
            (17, 6): "A small clearing appears between the trees.",
            (10, 10): "The trees here are very dense, it’s dark.",
            (9, 10): "The trees here are very dense, it’s dark.",
            (8, 10): "The trees here are very dense, it’s dark.",
            (7, 10): "The trees here are very dense, it’s dark.",
            (10, 11): "The trees here are very dense, it’s dark.",
            (9, 11): "The trees here are very dense, it’s dark.",
            (8, 11): "The trees here are very dense, it’s dark.",
            (7, 11): "The trees here are very dense, it’s dark.",
            (5, 20): "A mysterious grove where the air feels strange and heavy.",
            (4, 20): "A mysterious grove where the air feels strange and heavy.",
            (3, 20): "A mysterious grove where the air feels strange and heavy.",
            (2, 20): "A mysterious grove where the air feels strange and heavy.",
            (5, 21): "A mysterious grove where the air feels strange and heavy.",
            (4, 21): "A mysterious grove where the air feels strange and heavy.",
            (3, 21): "A mysterious grove where the air feels strange and heavy.",
            (2, 21): "A mysterious grove where the air feels strange and heavy.",
            (0, 29): "A threatening place... The boss awaits you here.",
            (1, 29): "You are very close to the final boss... Be ready.",
            (2, 29): "You are very close to the final boss... The air feels tense.",
            (3, 29): "You are very close to the final boss... It's almost time.",
            (0, 28): "You are very close to the final boss... The ground shakes.",
            (1, 28): "You are very close to the final boss... Prepare for battle.",
            (2, 28): "You are very close to the final boss... You feel its presence.",
            (3, 28): "You are very close to the final boss... The forest feels darker.",
            (15, 15): "A quiet part of the forest, the sounds of wildlife surround you.",
            (14, 15): "A quiet part of the forest, the sounds of wildlife surround you.",
            (13, 15): "A quiet part of the forest, the sounds of wildlife surround you.",
            (12, 15): "A quiet part of the forest, the sounds of wildlife surround you.",
            (25, 10): "The path becomes overgrown here, hard to find your way.",
            (24, 10): "The path becomes overgrown here, hard to find your way.",
            (23, 10): "The path becomes overgrown here, hard to find your way.",
            (22, 10): "The path becomes overgrown here, hard to find your way.",
            (10, 25): "You are in a quiet, unclear part of the forest.",
            (10, 24): "You are in a quiet, unclear part of the forest.",
            (9, 24): "You are in a quiet, unclear part of the forest.",
            (9, 25): "You are in a quiet, unclear part of the forest.",
        }
        self.boss_defeated = False

    def main_menu(self):
        print("Welcome to the RPG Game!")
        while True:
            print("\nMain Menu:")
            print("1. Start New Game")
            print("2. Quit")
            choice = input("> ")
            if choice == '1':
                self.start_new_game()
            elif choice == '2':
                print("Goodbye!")
                break

    def start_new_game(self):
        print("Enter your character's name:")
        name = input("> ")
        self.player = Character(name)
        print(f"Welcome, {self.player.name}! You awaken in a mysterious forest with only a knife.")
        self.player.equip_weapon('Knife')
        self.game_loop()

    def game_loop(self):
        while True:
            if not self.player.is_alive():
                print("You have been defeated.")
                break
            if self.boss_defeated:
                print("Congratulations! You have defeated the boss and escaped the forest.")
                break
            print(f"\nCurrent Location: {self.position}")
            print(self.locations[self.position])
            print("Commands: Go North, Go South, Go East, Go West, Inventory, Stats, Quit")
            command = input("> ").lower()
            if command.startswith("go"):
                self.move(command.split()[1])
            elif command == "inventory":
                self.show_inventory()
            elif command == "stats":
                self.player.show_stats()
            elif command == "quit":
                print("Goodbye!")
                break
            else:
                print("Invalid command!")

    def move(self, direction):
        x, y = self.position
        if direction == 'north' and x > 0:
            x -= 1
        elif direction == 'south' and x < self.map_size[0] - 1:
            x += 1
        elif direction == 'east' and y < self.map_size[1] - 1:
            y += 1
        elif direction == 'west' and y > 0:
            y -= 1
        else:
            print("You cannot go that way.")
            return

        self.position = (x, y)
        print(f"You moved to position {self.position}.")
        self.location_event()
            
    def location_event(self):
        if self.position in self.locations:
            print(self.locations[self.position])
            if self.position == (0, 29):
                self.combat_boss()
            else:
                self.random_event()
        else:
            print("You are in a random part of the forest.")

    def combat_boss(self):
        if not self.boss_defeated:
            print("The boss is here! Prepare for battle!")
            self.combat()
        else:
            print("The boss has been defeated. You can leave the forest!")

    def random_event(self):
        event = random.choice(['monster', 'item', 'nothing'])
        if event == 'monster':
            self.combat()
        elif event == 'item':
            self.find_item()
        else:
            print("Nothing happens...")

    def combat(self):
        if self.position == 'Boss Lair':
            monster = Monster("Boss", level=10)
        else:
            monster = Monster("Monster", level=random.randint(1, self.player.level + 1))
        print(f"A wild {monster.name} (Level {monster.level}) appears!")
        
        while self.player.is_alive() and monster.is_alive():
            print(f"\nYour HP: {self.player.hp}/{self.player.max_hp}")
            print(f"{monster.name} HP: {monster.hp}")
            print("Choose action: Attack, Inventory, Run")
            action = input("> ").lower()
            if action == "attack":
                self.attack(monster)
            elif action == "inventory":
                self.use_item(monster)
            elif action == "run":
                print("You run away!")
                return
            else:
                print("Invalid action!")
            if monster.is_alive():
                self.monster_attack(monster)

        if self.player.is_alive() and not monster.is_alive():
            xp_gain = monster.level * 50
            print(f"You defeated {monster.name} and gained {xp_gain} XP!")
            self.player.gain_xp(xp_gain)
            if monster.name == "Boss":
                self.boss_defeated = True

    def attack(self, monster):
        player_damage = max(0, self.player.attack - monster.defense)
        monster.take_damage(player_damage)
        if not monster.is_alive():
            print(f"{monster.name} is defeated!")

    def monster_attack(self, monster):
        monster_damage = max(0, monster.attack - self.player.defense)
        self.player.take_damage(monster_damage)
        if not self.player.is_alive():
            print(f"{self.player.name} was defeated by {monster.name}...")

    def find_item(self):
        item = random.choice(['Potion', 'Attack Boost', 'Defense Boost', 'Sword'])
        self.player.inventory.append(item)
        print(f"You found a {item}!")
        if item == 'Sword':
            self.player.equip_weapon('Sword')

    def show_inventory(self):
        if not self.player.inventory:
            print("Your inventory is empty.")
        else:
            print("Inventory:")
            for i, item in enumerate(self.player.inventory, 1):
                print(f"{i}. {item}")
            print("Select an item to use or equip:")
            use_item = input("> ").lower()
            if use_item.isdigit() and 1 <= int(use_item) <= len(self.player.inventory):
                self.use_item(int(use_item) - 1)
            else:
                print("Invalid selection.")

    def use_item(self, item_index, monster=None):
        item = self.player.inventory[item_index]
        if item == 'Potion':
            self.player.heal(50)
            self.player.inventory.pop(item_index)
        elif item == 'Attack Boost':
            self.player.attack += 5
            print(f"{self.player.name}'s attack increased!")
            self.player.inventory.pop(item_index)
        elif item == 'Defense Boost':
            self.player.defense += 5
            print(f"{self.player.name}'s defense increased!")
            self.player.inventory.pop(item_index)
        elif item in ['Knife', 'Sword']:
            self.player.equip_weapon(item)

game = Game()
game.main_menu()
