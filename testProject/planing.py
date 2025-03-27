import time

class Team:
    def __init__(self, name):
        self.name = name
        self.members = []

    def add_member(self, character):
        self.members.append(character)

    def is_defeated(self):
        return all(member.hp <= 0 for member in self.members)

    def get_alive_members(self):
        return [member for member in self.members if member.hp > 0]


class Character:
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp
        self.skills = []

    def add_skill(self, skill):
        self.skills.append(skill)

    def take_damage(self, amount):
        self.hp -= amount
        print(f"{self.name} 受到 {amount} 傷害，剩餘 HP：{self.hp}")
        if self.hp <= 0:
            print(f"{self.name} 倒下了！")

    def use_skill(self, skill_index, target):
        if 0 <= skill_index < len(self.skills):
            skill = self.skills[skill_index]
            skill.use(self, target)
        else:
            print("技能不存在")


class Skill:
    def __init__(self, name, description=""):
        self.name = name
        self.description = description

    def use(self, user, target):
        raise NotImplementedError("請由子類別實作")


class SingleTargetSkill(Skill):
    def __init__(self, name, damage, description=""):
        super().__init__(name, description)
        self.damage = damage

    def use(self, user, target):
        print(f"{user.name} 對 {target.name} 使用【{self.name}】！")
        print(self.description)
        target.take_damage(self.damage)


class AoESkill(Skill):
    def __init__(self, name, damage, description=""):
        super().__init__(name, description)
        self.damage = damage

    def use(self, user, target_team):
        print(f"{user.name} 使用群體技能【{self.name}】攻擊整隊 {target_team.name}！")
        print(self.description)
        for target in target_team.get_alive_members():
            target.take_damage(self.damage)


class DelayedSkill(Skill):
    def __init__(self, name, damage, delay_turns=1, description=""):
        super().__init__(name, description)
        self.damage = damage
        self.delay_turns = delay_turns
        self.pending = []

    def use(self, user, target):
        print(f"{user.name} 開始蓄力技能【{self.name}】，將在 {self.delay_turns} 回合後發動！")
        self.pending.append((self.delay_turns, user, target))

    def update_pending(self):
        new_pending = []
        for delay, user, target in self.pending:
            if delay <= 1:
                print(f"技能【{self.name}】延遲發動！{user.name} 對 {target.name} 發動攻擊！")
                target.take_damage(self.damage)
            else:
                new_pending.append((delay - 1, user, target))
        self.pending = new_pending


# 建立角色與技能
hero = Character("勇者", 100)
mage = Character("法師", 80)
goblin1 = Character("哥布林A", 40)
goblin2 = Character("哥布林B", 40)

# 加入技能
fire = SingleTargetSkill("火球術", 30, "🔥 一發火球直擊！")
meteor = AoESkill("流星雨", 20, "☄️ 群體傷害！")
charge = DelayedSkill("蓄力斬", 50, 2, "⚡️ 蓄力斬將在兩回合後釋放！")

hero.add_skill(fire)
mage.add_skill(meteor)
hero.add_skill(charge)

# 建立隊伍
player_team = Team("玩家隊伍")
enemy_team = Team("敵人隊伍")
player_team.add_member(hero)
player_team.add_member(mage)
enemy_team.add_member(goblin1)
enemy_team.add_member(goblin2)

# 回合模擬
turn = 1
while not enemy_team.is_defeated():
    print(f"\n=== 回合 {turn} ===")

    # 玩家使用技能
    hero.use_skill(0, goblin1)   # 火球術打哥布林A
    mage.use_skill(0, enemy_team)  # 法師用流星雨
    hero.use_skill(1, goblin2)   # 蓄力斬指定哥布林B

    # 技能延遲處理
    charge.update_pending()

    turn += 1
    time.sleep(1)

print("戰鬥結束！")
