import PySimpleGUI as sg
import random as rand
import functions as dan
import re
import os
import json

rand.seed()

sg.set_options(font='Times 12')
sg.theme('SandyBeach')

def iniPrint(iniOrder, monsters) :
    iniOrder = ''
    for x in range(30, 0, -1) :
        if x >= 10 :
            iniOrder += str(x) + '|  '
        else :
            iniOrder += '  ' + str(x) + '|  '
        for y in monsters :
            if isinstance(y, monster) :
                if x == y.rollTotal :
                    iniOrder += str(y.name) + '  '
        iniOrder += '\n'
    else :
        return window['-ORDER-'].update(iniOrder)

iniOrder = '30|\n29|\n28|\n27|\n26|\n25|\n24|\n23|\n22|\n21|\n20|\n19|\n18|\n17|\n16|\n15|\n14|\n13|\n12|\n11|\n10|\n  9|\n  8|\n  7|\n  6|\n  5|\n  4|\n  3|\n  2|\n  1|\n'

sizes = ['Tiny', 'Small', 'Medium', 'Large', 'Huge', 'Gargantuan']

actionIniValues = [
    'Fastest action',
    'Fast action (melee light, finesse)',
    'Normal action',
    'Slow action (melee heavy, two-handed)',
    'Slowest action (ranged loading)',
    'Custom action (spellcasting)'
]

customActionValues = []
for x in range(-10,11) :
    customActionValues.append(x)

class monster :
    def __init__(self) -> None:
        self.index = 0
        self.name = 'Monster'
        self.size = 'Medium'
        self.ac = 10
        self.mHp = 1
        self.cHp = self.mHp
        self.dex = 10
        self.actionMod = 0
        self.totalBonus = 0
        self.d20 = 10
        self.rollTotal = 0
    def roll(self) :
        self.d20 = rand.randint(1,20)
        self.rollTotal = min(30, max(1, int(self.d20+self.totalBonus)))

monsters = []
monsterIndex = 0
groupSize = 0
monsterCont = 0

iniCol = [
    [sg.Stretch(), sg.Text('\t===\tInitiative Order\t===\t', expand_x=True), sg.Stretch()],
    [sg.Text(iniOrder, key = '-ORDER-', expand_x=True)],
    [sg.Button('Roll', key = '-ROLL-', expand_x=True)]
]

monsterCol = [
    [sg.Frame(title='',
                layout=[[sg.Button(button_text='Add', key='-ADD-'),
                        sg.Button(button_text='Clear', key='-CLEAR-', visible=True),
                        sg.FileBrowse('Load', key='-BROWSE-', target='-LOAD-', file_types=[['JSON Files', '*.json']]),
                        sg.Input('', key='-LOAD-', enable_events=True, readonly=True, disabled_readonly_background_color=sg.theme_input_background_color(), visible=False),
                        sg.FileBrowse('Load Group', key='-BROWSEG-', target='-LOAD_GROUP-', file_types=[['JSON Files', '*.json']]),
                        sg.Input('', key='-LOAD_GROUP-', enable_events=True, readonly=True, disabled_readonly_background_color=sg.theme_input_background_color(), visible=False),
                        sg.Stretch(),
                        sg.Text(text='Group size:'),
                        sg.Text(text='', size=(3, 1), key='-GROUP_COUNT-')]],
                relief=sg.RELIEF_RAISED,
                border_width=1,
                expand_x=True)]
]

layout = [
    [sg.Column(iniCol, key = '-INI_COL-', element_justification='left', size=(400,800)),sg.Push(), sg.Column(monsterCol, key = '-MON_COL-', size=(450,800), element_justification='left', scrollable=True, vertical_scroll_only=True)]
]

window = sg.Window('Speed Factor Initiative', layout, size=(950,700), resizable=True)

while True :
    event, values = window.read()

    if event == sg.WIN_CLOSED :
        break

    if event == '-ROLL-' :
        iniOrder = ''
        for x in range(0, monsterIndex) :
            if isinstance(monsters[x], monster) :
                monsters[x].roll()
                print(monsters[x].name + ': ' + str(monsters[x].rollTotal) + ' (' + str(monsters[x].d20) + ' + ' + str(monsters[x].totalBonus) + ')')
        iniPrint(iniOrder, monsters)
        print('\n\n')

    if event == '-ADD-' :
        monsters.append(monster())
        monsters[monsterIndex].index = monsterIndex
        window.extend_layout(container = window['-MON_COL-'], rows = [[sg.Frame(f'Monster {monsterCont+1}', layout= [
                                                                                                [sg.Input(monsters[monsterIndex].name, key = f'-NAME_{monsterIndex}-', size=(30,1), enable_events=True)],
                                                                                                [sg.Combo(sizes, key = f'-SIZE_{monsterIndex}-', default_value=monsters[monsterIndex].size, enable_events=True)],
                                                                                                [sg.Text('AC'), sg.Input(key = f'-AC_{monsterIndex}-', default_text=monsters[monsterIndex].ac, size=(3,1), enable_events=True)],
                                                                                                [sg.Text('HP'), sg.Input(monsters[monsterIndex].mHp, key = f'-CHP_{monsterIndex}-', size=(3,1), text_color='green', enable_events=True), sg.Text('/'), sg.Input(monsters[monsterIndex].mHp, key = f'-MHP_{monsterIndex}-', size=(3,1), enable_events=True)],
                                                                                                [sg.Text('Dex'), sg.Input(key = f'-DEX_{monsterIndex}-', default_text=monsters[monsterIndex].dex, size=(3,1), enable_events=True)],
                                                                                                [sg.Text('Action Initiative Modifier'), sg.Combo(actionIniValues, key = f'-ACTION_INI_{monsterIndex}-', enable_events=True, size=(31), default_value='Normal action')],
                                                                                                [sg.pin(sg.Button('Remove', key = f'-REMOVE__{monsterIndex}-')), sg.pin(sg.Button('Duplicate', key = f'-DUPLICATE__{monsterIndex}-')), sg.Stretch(), sg.Text('Enter Custom Modifier', key = f'-CUSTOM_MOD_TXT_{monsterIndex}-',visible=False), sg.Input(0, key = f'-CUSTOM_MOD_{monsterIndex}-', size=(3,1), visible=False, enable_events=True)]
                                                                                            ],
                                
                            key = f'-MONSTER_{monsterIndex}-')]])
        window['-MON_COL-'].Widget.update()
        window['-MON_COL-'].contents_changed()
        monsterIndex += 1
        groupSize += 1
        monsterCont += 1
        window['-GROUP_COUNT-'].update(groupSize)


    if event == '-CLEAR-' :
        x = 0
        for element in window.element_list() :
            if isinstance(element.key, str) :
                if element.key.startswith('-MONSTER_') :
                    element.update(visible = False)
                    element.Widget.master.pack_forget()
                    monsters[x] = ''
                    x += 1
        groupSize = 0
        monsterCont = 0
        window['-GROUP_COUNT-'].update(groupSize)
        window['-MON_COL-'].Widget.update()
        window['-MON_COL-'].contents_changed()
        iniPrint(iniOrder, monsters)

    if event == '-LOAD-' :
        monsters.append(monster())
        monsters[monsterIndex].index = monsterIndex
        fileDir = os.path.abspath(values['-LOAD-'])
        try :
            with open(fileDir, 'r') as file :
                creature = json.load(file)
                monsters[monsterIndex].name = creature["name"]
                match creature["size"][0] :
                    case 'T' :
                        monsters[monsterIndex].size = 'Tiny'
                    case 'S' :
                        monsters[monsterIndex].size = 'Small'
                    case 'M' :
                        monsters[monsterIndex].size = 'Medium'
                    case 'L' :
                        monsters[monsterIndex].size = 'Large'
                    case 'H' :
                        monsters[monsterIndex].size = 'Huge'
                    case 'G' :
                        monsters[monsterIndex].size = 'Gargantuan'
                try:
                    monsters[monsterIndex].ac = creature["ac"][0]["ac"]
                except:
                    monsters[monsterIndex].ac = creature["ac"][0]
                monsters[monsterIndex].mHp = creature["hp"]["average"]
                monsters[monsterIndex].dex = creature["dex"]
        except :
            with open(fileDir, 'r') as file :
                creature = json.load(file)
                monsters[monsterIndex].name = creature["monster"][0]["name"]
                match creature["monster"][0]["size"][0] :
                    case 'T' :
                        monsters[monsterIndex].size = 'Tiny'
                    case 'S' :
                        monsters[monsterIndex].size = 'Small'
                    case 'M' :
                        monsters[monsterIndex].size = 'Medium'
                    case 'L' :
                        monsters[monsterIndex].size = 'Large'
                    case 'H' :
                        monsters[monsterIndex].size = 'Huge'
                    case 'G' :
                        monsters[monsterIndex].size = 'Gargantuan'
                monsters[monsterIndex].ac = creature["monster"][0]["ac"][0]["ac"]
                monsters[monsterIndex].mHp = creature["monster"][0]["hp"]["average"]
                monsters[monsterIndex].dex = creature["monster"][0]["dex"]
        window.extend_layout(container = window['-MON_COL-'], rows = [[sg.Frame(f'Monster {monsterCont+1}', layout= [
                                                                                                [sg.Input(monsters[monsterIndex].name, key = f'-NAME_{monsterIndex}-', size=(30,1), enable_events=True)],
                                                                                                [sg.Combo(sizes, key = f'-SIZE_{monsterIndex}-', default_value=monsters[monsterIndex].size, enable_events=True)],
                                                                                                [sg.Text('AC'), sg.Input(key = f'-AC_{monsterIndex}-', default_text=monsters[monsterIndex].ac, size=(3,1), enable_events=True)],
                                                                                                [sg.Text('HP'), sg.Input(monsters[monsterIndex].mHp, key = f'-CHP_{monsterIndex}-', size=(3,1), text_color='green', enable_events=True), sg.Text('/'), sg.Input(monsters[monsterIndex].mHp, key = f'-MHP_{monsterIndex}-', size=(3,1), enable_events=True)],
                                                                                                [sg.Text('Dex'), sg.Input(key = f'-DEX_{monsterIndex}-', default_text=monsters[monsterIndex].dex, size=(3,1), enable_events=True)],
                                                                                                [sg.Text('Action Initiative Modifier'), sg.Combo(actionIniValues, key = f'-ACTION_INI_{monsterIndex}-', enable_events=True, size=(31), default_value='Normal action')],
                                                                                                [sg.pin(sg.Button('Remove', key = f'-REMOVE__{monsterIndex}-')), sg.pin(sg.Button('Duplicate', key = f'-DUPLICATE__{monsterIndex}-')), sg.Stretch(), sg.Text('Enter Custom Modifier', key = f'-CUSTOM_MOD_TXT_{monsterIndex}-',visible=False), sg.Input(0, key = f'-CUSTOM_MOD_{monsterIndex}-', size=(3,1), visible=False, enable_events=True)]
                                                                                            ],
                                
                            key = f'-MONSTER_{monsterIndex}-')]])
        window['-MON_COL-'].Widget.update()
        window['-MON_COL-'].contents_changed()
        monsterIndex += 1
        groupSize += 1
        monsterCont += 1
        window['-GROUP_COUNT-'].update(groupSize)
    
    if event == '-LOAD_GROUP-' :
        fileDirG = os.path.abspath(values['-LOAD_GROUP-'])
        with open(fileDirG, 'r') as fileG :
            group = json.load(fileG)
            for x in group :
                for y in range(group[x]["amount"]) :
                    monsters.append(monster())
                    monsters[monsterIndex].index = monsterIndex
                    fileDir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(fileDirG))) + "\\" + group[x]["source"] + "\\" + group[x]["monster"])
                    try :
                        with open(fileDir, 'r') as file :
                            creature = json.load(file)
                            monsters[monsterIndex].name = creature["name"]
                            match creature["size"][0] :
                                case 'T' :
                                    monsters[monsterIndex].size = 'Tiny'
                                case 'S' :
                                    monsters[monsterIndex].size = 'Small'
                                case 'M' :
                                    monsters[monsterIndex].size = 'Medium'
                                case 'L' :
                                    monsters[monsterIndex].size = 'Large'
                                case 'H' :
                                    monsters[monsterIndex].size = 'Huge'
                                case 'G' :
                                    monsters[monsterIndex].size = 'Gargantuan'
                            try:
                                monsters[monsterIndex].ac = creature["ac"][0]["ac"]
                            except:
                                monsters[monsterIndex].ac = creature["ac"][0]
                            monsters[monsterIndex].mHp = creature["hp"]["average"]
                            monsters[monsterIndex].dex = creature["dex"]
                    except :
                        with open(fileDir, 'r') as file :
                            creature = json.load(file)
                            monsters[monsterIndex].name = creature["monster"][0]["name"]
                            match creature["monster"][0]["size"][0] :
                                case 'T' :
                                    monsters[monsterIndex].size = 'Tiny'
                                case 'S' :
                                    monsters[monsterIndex].size = 'Small'
                                case 'M' :
                                    monsters[monsterIndex].size = 'Medium'
                                case 'L' :
                                    monsters[monsterIndex].size = 'Large'
                                case 'H' :
                                    monsters[monsterIndex].size = 'Huge'
                                case 'G' :
                                    monsters[monsterIndex].size = 'Gargantuan'
                            monsters[monsterIndex].ac = creature["monster"][0]["ac"][0]["ac"]
                            monsters[monsterIndex].mHp = creature["monster"][0]["hp"]["average"]
                            monsters[monsterIndex].dex = creature["monster"][0]["dex"]
                    if(group[x]["amount"] > 1) :
                        suf = " " + str(y+1)
                    else :
                        suf = ""
                    window.extend_layout(container = window['-MON_COL-'], rows = [[sg.Frame(f'Monster {monsterCont+1}', layout= [
                                                                                                            [sg.Input(monsters[monsterIndex].name + suf, key = f'-NAME_{monsterIndex}-', size=(30,1), enable_events=True)],
                                                                                                            [sg.Combo(sizes, key = f'-SIZE_{monsterIndex}-', default_value=monsters[monsterIndex].size, enable_events=True)],
                                                                                                            [sg.Text('AC'), sg.Input(key = f'-AC_{monsterIndex}-', default_text=monsters[monsterIndex].ac, size=(3,1), enable_events=True)],
                                                                                                            [sg.Text('HP'), sg.Input(monsters[monsterIndex].mHp, key = f'-CHP_{monsterIndex}-', size=(3,1), text_color='green', enable_events=True), sg.Text('/'), sg.Input(monsters[monsterIndex].mHp, key = f'-MHP_{monsterIndex}-', size=(3,1), enable_events=True)],
                                                                                                            [sg.Text('Dex'), sg.Input(key = f'-DEX_{monsterIndex}-', default_text=monsters[monsterIndex].dex, size=(3,1), enable_events=True)],
                                                                                                            [sg.Text('Action Initiative Modifier'), sg.Combo(actionIniValues, key = f'-ACTION_INI_{monsterIndex}-', enable_events=True, size=(31), default_value='Normal action')],
                                                                                                            [sg.pin(sg.Button('Remove', key = f'-REMOVE__{monsterIndex}-')), sg.pin(sg.Button('Duplicate', key = f'-DUPLICATE__{monsterIndex}-')), sg.Stretch(), sg.Text('Enter Custom Modifier', key = f'-CUSTOM_MOD_TXT_{monsterIndex}-',visible=False), sg.Input(0, key = f'-CUSTOM_MOD_{monsterIndex}-', size=(3,1), visible=False, enable_events=True)]
                                                                                                        ],
                                            
                                        key = f'-MONSTER_{monsterIndex}-')]])
                    window['-MON_COL-'].Widget.update()
                    window['-MON_COL-'].contents_changed()
                    monsterIndex += 1
                    groupSize += 1
                    monsterCont += 1
                    window['-GROUP_COUNT-'].update(groupSize)
        

    if event.startswith('-REMOVE_') :
        index = re.findall(r'\d+', event)
        window[f'-MONSTER_{int(index[0])}-'].update(visible = False)
        window[f'-MONSTER_{int(index[0])}-'].Widget.master.pack_forget()
        monsters[int(index[0])] = ''
        groupSize -= 1
        monsterCont -= 1
        window['-GROUP_COUNT-'].update(groupSize)
        window['-MON_COL-'].Widget.update()
        window['-MON_COL-'].contents_changed()
        iniPrint(iniOrder, monsters)

    if event.startswith('-DUPLICATE_') :
        index = re.findall(r'\d+', event)
        cont = 1
        for x in monsters :
            if isinstance(x, monster) :
                if x.name.startswith(monsters[int(index[0])].name) :
                    cont += 1
        monsters.append(monster())
        monsters[monsterIndex].index = monsterIndex
        monsters[monsterIndex].name = monsters[int(index[0])].name + ' ' + str(cont)
        monsters[monsterIndex].size = monsters[int(index[0])].size
        monsters[monsterIndex].ac = monsters[int(index[0])].ac
        monsters[monsterIndex].mHp = monsters[int(index[0])].mHp
        monsters[monsterIndex].dex = monsters[int(index[0])].dex
        window.extend_layout(container = window['-MON_COL-'], rows = [[sg.Frame(f'Monster {monsterCont+1}', layout= [
                                                                                                [sg.Input(monsters[monsterIndex].name, key = f'-NAME_{monsterIndex}-', size=(30,1), enable_events=True)],
                                                                                                [sg.Combo(sizes, key = f'-SIZE_{monsterIndex}-', default_value=monsters[monsterIndex].size, enable_events=True)],
                                                                                                [sg.Text('AC'), sg.Input(key = f'-AC_{monsterIndex}-', default_text=monsters[monsterIndex].ac, size=(3,1), enable_events=True)],
                                                                                                [sg.Text('HP'), sg.Input(monsters[monsterIndex].mHp, key = f'-CHP_{monsterIndex}-', size=(3,1), text_color='green', enable_events=True), sg.Text('/'), sg.Input(monsters[monsterIndex].mHp, key = f'-MHP_{monsterIndex}-', size=(3,1), enable_events=True)],
                                                                                                [sg.Text('Dex'), sg.Input(key = f'-DEX_{monsterIndex}-', default_text=monsters[monsterIndex].dex, size=(3,1), enable_events=True)],
                                                                                                [sg.Text('Action Initiative Modifier'), sg.Combo(actionIniValues, key = f'-ACTION_INI_{monsterIndex}-', enable_events=True, size=(31), default_value='Normal action')],
                                                                                                [sg.pin(sg.Button('Remove', key = f'-REMOVE__{monsterIndex}-')), sg.pin(sg.Button('Duplicate', key = f'-DUPLICATE__{monsterIndex}-')), sg.Stretch(), sg.Text('Enter Custom Modifier', key = f'-CUSTOM_MOD_TXT_{monsterIndex}-',visible=False), sg.Input(0, key = f'-CUSTOM_MOD_{monsterIndex}-', size=(3,1), visible=False, enable_events=True)]
                                                                                            ],
                                
                            key = f'-MONSTER_{monsterIndex}-')]])
        window['-MON_COL-'].Widget.update()
        window['-MON_COL-'].contents_changed()
        monsterIndex += 1
        groupSize += 1
        monsterCont += 1
        window['-GROUP_COUNT-'].update(groupSize)

    if event.startswith('-NAME_') or event.startswith('-SIZE_') or event.startswith('-AC_') or event.startswith('-DEX_') or event.startswith('-CHP_') or event.startswith('-MHP_') or event.startswith('-ACTION_INI_') or event.startswith('-CUSTOM_MOD_') :
        index = re.findall(r'\d+', event)
        monsters[int(index[0])].name = values[f'-NAME_{index[0]}-']
        monsters[int(index[0])].size = values[f'-SIZE_{index[0]}-']
        try :
            if 99 >= int(values[f'-AC_{index[0]}-']) > 0 :
                monsters[int(index[0])].ac = values[f'-AC_{index[0]}-']
            else :
                window[f'-AC_{index[0]}-'].update(value=10)
        except :
            window[f'-AC_{index[0]}-'].update(value=10)
        try :
            if 999 >= int(values[f'-MHP_{index[0]}-']) > 0 :
                monsters[int(index[0])].mHp = values[f'-MHP_{index[0]}-']
            else :
                window[f'-MHP_{index[0]}-'].update(value=1)
        except :
            window[f'-MHP_{index[0]}-'].update(value=1)
        try :
            if 30 >= int(values[f'-DEX_{index[0]}-']) > 0 :
                monsters[int(index[0])].dex = values[f'-DEX_{index[0]}-']
            else :
                window[f'-DEX_{index[0]}-'].update(value=10)
        except :
            window[f'-DEX_{index[0]}-'].update(value=10)
        try :
            #if str(values[f'-CHP_{index[0]}-']).startswith('+') :
            #    while not isinstance(values[f'-CHP_{index[0]}-'][0], int) :
            #        values[f'-CHP_{index[0]}-'] = str(values[f'-CHP_{index[0]}-'])[1:]
            #    heal = int(str(values[f'-CHP_{index[0]}-'])[1:])
            #    monsters[int(index[0])].cHp += heal
            #    window[f'-CHP_{index[0]}-'].update(monsters[int(index[0])].cHp)
            #else :
            monsters[int(index[0])].cHp = values[f'-CHP_{index[0]}-']
            if int(values[f'-CHP_{index[0]}-']) > int(values[f'-MHP_{index[0]}-']) :
                window[f'-CHP_{index[0]}-'].update(values[f'-MHP_{index[0]}-'])
            elif int(values[f'-CHP_{index[0]}-']) > int(values[f'-MHP_{index[0]}-'])/2 :
                window[f'-CHP_{index[0]}-'].update(text_color='green')
            elif int(values[f'-CHP_{index[0]}-']) <= int(values[f'-MHP_{index[0]}-'])/2 and not int(values[f'-CHP_{index[0]}-']) <= 0 :
                window[f'-CHP_{index[0]}-'].update(text_color='orange')
            else :
                window[f'-CHP_{index[0]}-'].update(text_color='red')
        except :
            pass
        if not values[f'-ACTION_INI_{index[0]}-'].startswith('Custom') :
            window[f'-CUSTOM_MOD_TXT_{int(index[0])}-'].update(visible=False)
            window[f'-CUSTOM_MOD_{int(index[0])}-'].update(visible=False)
            monsters[int(index[0])].actionMod = dan.speedMod(values[f'-ACTION_INI_{index[0]}-'])
        else :
            window[f'-CUSTOM_MOD_TXT_{int(index[0])}-'].update(visible=True)
            window[f'-CUSTOM_MOD_{int(index[0])}-'].update(visible=True)
            monsters[int(index[0])].actionMod = values[f'-CUSTOM_MOD_{index[0]}-']
            try :
                if not 10 >= int(values[f'-CUSTOM_MOD_{index[0]}-']) >= -10 and values[f'-CUSTOM_MOD_{index[0]}-'] != '-':
                    window[f'-CUSTOM_MOD_{index[0]}-'].update(value=0)
            except :
                pass
        try :
            monsters[int(index[0])].totalBonus = dan.abilityMod(int(monsters[int(index[0])].dex)) + dan.sizeMod(monsters[int(index[0])].size) + int(monsters[int(index[0])].actionMod)
        except :
            pass

window.close()