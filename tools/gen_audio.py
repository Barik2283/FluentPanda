"""
Генерация озвучки нейроголосами (бесплатно, без ключей).

  pip install edge-tts
  python tools/gen_audio.py          # сгенерировать
  python tools/gen_audio.py --list   # только посчитать фразы по языкам

Создаст audio/<lang>/<id>.mp3 (слово), audio/<lang>/<id>_ex.mp3 (пример) и audio/manifest.json.
Приложение само увидит manifest.json и начнёт играть файлы вместо системного голоса.
(Работает при открытии через http/https, не через file://.) Если файла нет — звучит голос браузера.
v5: + ru, uk, sr, zh, he. Китайский озвучивается пиньинем, как в приложении
(const ZH_SPEAK_HANZI=true в index.html — тогда иероглифами).
"""
import asyncio, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOICES = {'en': 'en-US-AriaNeural', 'es': 'es-ES-ElviraNeural', 'de': 'de-DE-KatjaNeural', 'fr': 'fr-FR-DeniseNeural',
          'it': 'it-IT-ElsaNeural', 'pt': 'pt-BR-FranciscaNeural', 'tr': 'tr-TR-EmelNeural', 'pl': 'pl-PL-ZofiaNeural',
          'ru': 'ru-RU-SvetlanaNeural', 'uk': 'uk-UA-PolinaNeural', 'sr': 'sr-RS-SophieNeural',
          'zh': 'zh-CN-XiaoxiaoNeural', 'he': 'he-IL-HilaNeural'}

html = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
items = [(m[1], m[2]) for m in re.finditer(r"W\('(\w+)','([^']*)'", html)]
wx = html[html.index('const WX={'):html.index('function wx(')]
items += [(m[1] + '_ex', m[2]) for m in re.finditer(r"(\w+):\['[^']*','[^']*','[^']*','([^']*)'", wx)]

# extra languages: addLang("it",[ ["b1","ciao","ru","ipa","use","example","exRu"], ... ]);
for m in re.finditer(r'addLang\("(\w+)",\[(.*?)\n\]\);', html, re.S):
    for r in re.finditer(r'\["(\w+)","([^"]*)","[^"]*","[^"]*","[^"]*","([^"]*)"', m[2]):
        items += [(m[1] + '_' + r[1], r[2]), (m[1] + '_' + r[1] + '_ex', r[3])]

# v5: addLangX("uk",[[суффикс, слово, ru, en, ipa|иероглифы, эмодзи, use_ru, use_en, пример, пример_ru, пример_en, пример_иероглифы], ...]);
HANZI = 'const ZH_SPEAK_HANZI=true' in html
for m in re.finditer(r'addLangX\("(\w+)",(\[\[.*?\]\])\);', html, re.S):
    for r in json.loads(m[2]):
        word, ex = r[1], r[8]
        if m[1] == 'zh' and HANZI:
            word, ex = r[4] or word, (r[11] if len(r) > 11 and r[11] else ex)
        items += [(m[1] + '_' + r[0], word), (m[1] + '_' + r[0] + '_ex', ex)]

# v5: русский для носителей (A1/A2/B1): RU_NATIVE={"A1":[[слово, ..., пример], ...], ...}
m = re.search(r'const RU_NATIVE=(\{.*?\});\n', html, re.S)
if m:
    for lv, rows in json.loads(m[1]).items():
        for n, r in enumerate(rows, 1):
            items += [('ru_%s_%d' % (lv, n), r[0]), ('ru_%s_%d_ex' % (lv, n), r[7] if len(r) > 7 else '')]

items = [(i, t) for i, t in items if t and i.split('_')[0] in VOICES]

if '--list' in sys.argv:
    from collections import Counter
    print(dict(Counter(i.split('_')[0] for i, _ in items)), 'всего', len(items))
    sys.exit()

import edge_tts
sem = asyncio.Semaphore(4)

async def one(i, text):
    lang = i.split('_')[0]
    out = os.path.join(ROOT, 'audio', lang, i + '.mp3')
    if os.path.exists(out):
        return
    os.makedirs(os.path.dirname(out), exist_ok=True)
    async with sem:
        await edge_tts.Communicate(text, VOICES[lang], rate='-8%').save(out)
        print('ok', i, text)

async def main():
    await asyncio.gather(*(one(i, t) for i, t in items))
    json.dump({'count': len(items), 'voices': VOICES}, open(os.path.join(ROOT, 'audio', 'manifest.json'), 'w'))
    print('Готово:', len(items), 'файлов')

asyncio.run(main())
