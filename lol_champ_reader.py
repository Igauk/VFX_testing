import json
from typing import Literal


class LoLChampReader:
    def __init__(self):
        self.champ_json = 'LoLChampInfo.json'
        self.json_data = self._read_champ_json()

    def _read_champ_json(self):
        with open(self.champ_json) as f:
            json_data = json.load(f)
            return json_data

    def get_champ_ability(self, champ_name: str, ability: Literal['Q', 'W', 'E', 'R'] = 'Q', filtered=True):
        champ_name = champ_name.title()
        if not champ_name in self.json_data:
            print(f'Champion {champ_name} not in pool.')
            return None
        data = self.json_data[champ_name][ability][0]
        if not filtered:
            return data

        filtered_data = {k: v for k, v in data.items() if v is not None}
        filtered_data['effects'] = ' '.join([effect['description'] for effect in filtered_data['effects']])
        if 'cooldown' in filtered_data:
            filtered_data['cooldown'] = filtered_data['cooldown']['modifiers'][0]['values'][-1]
        if 'cost' in filtered_data:
            filtered_data['cost'] = filtered_data['cost']['modifiers'][0]['values'][-1]
        visual_keys = {'name',
                       'effects',
                       'targeting',
                       'affects',
                       'spellEffects',
                       'projectile',
                       'speed',
                       'width',
                       'castTime',
                       'effectRadius',
                       'notes'}

        visual_data = {key: value for key, value in filtered_data.items() if key in visual_keys}
        return visual_data
