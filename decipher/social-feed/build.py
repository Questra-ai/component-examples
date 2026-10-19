from pathlib import Path
import random,html,json
ROOT=Path(__file__).parent
cfg={'feeds':5,'items':30,'versions':8}
(ROOT/'config.json').write_text(json.dumps(cfg,indent=2)) if not (ROOT/'config.json').exists() else None
cfg=json.loads((ROOT/'config.json').read_text())
assert 1 <= cfg['feeds'] <= 12 and 1 <= cfg['items'] <= 60 and 1 <= cfg['versions'] <= 99, 'Use feeds 1-12, items 1-60, versions 1-99'

copy=[
'A slower morning starts with one good cup. Take a moment before the day begins.',
'Your next great idea might be waiting outside. Make room for a little fresh air.',
'A small change of scenery can change the whole day. Where would you go?',
'Less rushing. More noticing. There is something good in the everyday.',
'An open afternoon, a loose plan, and something new to discover.',
'Save a little space for the things you do just because you love them.',
'Good things do not always need a big plan. Start small and see where it goes.',
'Find your own rhythm. There is no single right way to spend a free hour.',
'A fresh perspective is closer than you think. Try a different route today.',
'A reminder to pause, look around, and enjoy the part you are in.',
'Little rituals make ordinary days feel a little more like yours.',
'Here is to making time for something that is not on your to-do list.',
'An invitation to unplug for a while and see what you notice.',
'The best kind of reset? Something simple, with room to breathe.',
'Bring a friend. Bring your curiosity. Leave the complicated plans behind.',
'A quiet corner of the day, saved just for you.',
'Consider this your sign to try the thing you have been putting off.',
'More everyday adventures. Fewer perfect itineraries.',
'There is a lot to love about taking the long way home.',
'Make a little room for wonder, even on a very ordinary Tuesday.',
'Your weekend does not have to be full to feel good.',
'A change of pace, a new favorite, a story worth sharing.',
'Take the pressure off. A little enjoyment is reason enough.',
'A good day can begin with the smallest of decisions.',
'Choose something that makes you feel a little more present.',
'Sometimes the best discovery is right in your own neighborhood.',
'For the moments between big plans: a little everyday inspiration.',
'A simple pleasure is still a pleasure. Let it count.',
'Collect moments that feel like you. There is no need to keep score.',
'Leave a little space in the day for a pleasant surprise.'
]
palettes=[('#f1d7b4','#c97a4c','#527264'),('#dae5dc','#819d7b','#e6ae71'),('#e8d5cd','#b27165','#799587'),('#dae4e8','#8aa8af','#d9ac65'),('#ece4c7','#6e8e69','#d2986e'),('#e4d8df','#9d7b82','#739893'),('#eadccb','#c29568','#546e73'),('#d9e3ce','#7d9660','#c68b55'),('#e7d8bd','#a88862','#698a79'),('#dce4e5','#74969b','#d7a477')]
scenes=[]
for i,(bg,a,b) in enumerate(palettes):
    common=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 400" role="img" aria-label="Original illustration: '+['coffee and a quiet morning','a mountain trail','a sunny neighborhood','a coastal escape','a growing garden','a stack of books','a creative afternoon','a picnic in the park','a warm kitchen','a bike ride'][i]+f'"><rect width="800" height="400" fill="{bg}"/><circle cx="650" cy="85" r="48" fill="#fff8e6"/>'
    scene=[
    f'<path d="M0 290Q230 250 440 300T800 285V400H0Z" fill="{b}"/><ellipse cx="420" cy="308" rx="175" ry="29" fill="#234934" opacity=".15"/><path d="M310 165h180v105q0 50-90 50t-90-50z" fill="#fff7e6"/><path d="M490 180h30q65 0 40 65-12 28-70 20" fill="none" stroke="#fff7e6" stroke-width="22"/><ellipse cx="400" cy="165" rx="90" ry="20" fill="{a}"/><path d="M370 120q-25-30 0-55m60 55q-25-30 0-55" fill="none" stroke="#fff" stroke-width="9" opacity=".7"/>',
    f'<path d="M0 300L220 70l210 240L590 125l210 190v85H0Z" fill="{b}"/><path d="M0 350L250 180l160 140 180-110 210 140v50H0Z" fill="{a}"/><path d="M410 400q-150-80-10-130t-50-65" fill="none" stroke="#f6e7c9" stroke-width="37"/>',
    f'<path d="M0 330H800V400H0" fill="{b}"/>'+''.join(f'<rect x="{x}" y="{y}" width="145" height="{330-y}" fill="{c}"/><path d="M{x-10} {y}l82-65 83 65" fill="#6a715d"/><rect x="{x+50}" y="{y+55}" width="45" height="65" rx="4" fill="#f9e9c8"/>' for x,y,c in [(100,180,a),(325,120,'#e8b97e'),(550,175,'#f7e6cb')]),
    f'<path d="M0 180h800v220H0Z" fill="{a}"/><path d="M0 310q180-90 390 5t410-5v90H0Z" fill="#f5dfb0"/><path d="M480 190l-120 0 120-135z" fill="#fff8e8"/><path d="M340 200h180l-30 27H375Z" fill="{b}"/><path d="M70 240h140m390 35h110" stroke="#f4f4e1" stroke-width="5"/>',
    f'<rect x="0" y="315" width="800" height="85" fill="{b}"/>'+''.join(f'<path d="M{x} 255h110l-18 90h-75z" fill="{a}"/><path d="M{x+55} 260v-145" stroke="#4f6d45" stroke-width="9"/><ellipse cx="{x+26}" cy="175" rx="35" ry="18" transform="rotate(35 {x+26} 175)" fill="#6d8c54"/><ellipse cx="{x+80}" cy="135" rx="38" ry="21" transform="rotate(-35 {x+80} 135)" fill="#789c63"/>' for x in [110,345,580]),
    f'<rect x="0" y="325" width="800" height="75" fill="{b}"/>'+''.join(f'<rect x="{x}" y="{y}" width="{w}" height="45" rx="6" fill="{c}"/><path d="M{x+20} {y+12}h{w-40}m-{w-40} 9h{w-40}" stroke="#fff4d9" stroke-width="4"/>' for x,y,w,c in [(210,275,390,a),(245,225,340,'#ead2a1'),(225,175,380,'#799a8d'),(275,125,295,'#b78666')]),
    f'<path d="M0 290h800v110H0Z" fill="{a}"/><rect x="260" y="65" width="250" height="240" rx="5" fill="#fffae7"/><path d="M280 255l90-145 100 140" fill="{b}"/><circle cx="445" cy="125" r="30" fill="#dbad6a"/><path d="M280 305l-35 90m250-90 35 90" stroke="#715c45" stroke-width="18"/>',
    f'<path d="M0 240q200-100 420 20t380-10v150H0Z" fill="{a}"/><path d="M190 285h390l100 100H100Z" fill="#f6e8c8"/><path d="M190 315h400m-400 35h450m-380-65-20 100m100-100v100m90-100 20 100" stroke="#cb956b" stroke-width="12" opacity=".55"/><path d="M340 280h120v65H340Z" fill="{b}"/><path d="M355 280q45-70 90 0" fill="none" stroke="{b}" stroke-width="12"/>',
    f'<rect x="0" y="275" width="800" height="125" fill="{a}"/><ellipse cx="420" cy="300" rx="170" ry="38" fill="#fff7df"/><path d="M290 225q130-160 260 0v50H290Z" fill="#ce8c4f"/><path d="M350 175l-15 50m75-80-15 70m75-60-15 65" stroke="#f6d097" stroke-width="15"/><path d="M150 280v-130m0 60-35-35m35 65 35-35" stroke="{b}" stroke-width="12"/>',
    f'<path d="M0 315h800v85H0Z" fill="{b}"/><circle cx="260" cy="275" r="77" fill="none" stroke="#486560" stroke-width="12"/><circle cx="570" cy="275" r="77" fill="none" stroke="#486560" stroke-width="12"/><path d="M260 275l90-125 65 125H260l230-120 80 120m-220-125-15-32m155 37-15-45h50" fill="none" stroke="{a}" stroke-width="13"/><path d="M313 115h65" stroke="#486560" stroke-width="14"/>'
    ][i]
    scenes.append(common+scene+'</svg>')
# Genuine tab-delimited DCM design: first three keys, then levels/order/item attributes.
lines=['Version\tTask\tConcept\tCopy\tImage\tOrder\tItem']
for v in range(1,cfg['versions']+1):
    rng=random.Random(78131+v)
    for f in range(1,cfg['feeds']+1):
        copies=list(range(1,31));rng.shuffle(copies)
        imgs=[i%10+1 for i in range(cfg['items'])];rng.shuffle(imgs)
        for i in range(1,cfg['items']+1):lines.append(f'{v}\t{f}\t{i}\t{copies[(i-1)%30]}\t{imgs[i-1]}\t{i}\t{(f-1)*cfg["items"]+i}')
(ROOT/'social-design.dat').write_text('\n'.join(lines)+'\n')
css=(ROOT/'src/feed.css').read_text().replace('@','\\@')
js=(ROOT/'src/feed.js').read_text()
x=['<survey name="Social feed" alt="Social feed" compat="144" fir="on" html:showNumber="0" builder:wizardCompleted="1" state="testing" ss:enableNavigation="0" extraVariables="source">',f'<style name="respview.client.css" mode="after"><![CDATA[\n<style>{css}</style>\n]]></style>',f'<style name="respview.client.js" mode="after" wrap="ready"><![CDATA[\n{js}\n]]></style>']
x.append('''<exec when="init"><![CDATA[
def loadSocialDesign(fname):
    f = open("%s/%s" % (gv.survey.path, fname))
    records = [line.strip("\\r\\n").split("\\t") for line in f.readlines()]
    f.close()
    design = {}
    for row in records[1:]:
        design[(int(row[0]), int(row[1]), int(row[2]))] = [int(n) for n in row[3:]]
    return design
socialDesign = loadSocialDesign("social-design.dat")
]]></exec>''')
for i,c in enumerate(copy,1):x.append(f'<res label="copy{i}">{html.escape(c)}</res>')
for i,svg in enumerate(scenes,1):x.append(f'<res label="image{i}"><![CDATA[{svg}]]></res>')
x.append(f'''<number label="DesignVersion" where="execute" size="3"><title>Assigned .dat design version</title><exec>
if DesignVersion.val is None:
    DesignVersion.val = random.randint(1,{cfg['versions']})
</exec></number>
<number label="SessionKey" where="execute" size="12"><title>Anonymous response cache key</title><exec>
if SessionKey.val is None:
    SessionKey.val = random.randint(100000000,999999999)
</exec></number>
<html label="Initialize" where="survey">Loading…</html><suspend/>''')
for f in range(1,cfg['feeds']+1):
    x.append(f'<number label="Offer{f}" where="execute" optional="1" size="6"><title>Feed {f}: assigned design metadata by display position</title>')
    for i in range(1,cfg['items']+1):x.append(f'<row label="r{i}">Position {i}</row>')
    for label,title in [('task','Feed task'),('item','Item identity'),('order','Display order'),('copy','Copy level'),('image','Image level')]:x.append(f'<col label="{label}">{title}</col>')
    x.append(f'''<exec>
for i in range(1,{cfg['items']+1}):
    a = socialDesign[(DesignVersion.val,{f},i)]
    r = Offer{f}.rows[i-1]
    r.task.val = {f}
    r.item.val = a[3]
    r.order.val = a[2]
    r.copy.val = a[0]
    r.image.val = a[1]
</exec></number>''')
    x.append(f'<html label="Header{f}" where="survey"><![CDATA[<div class="cf-config" data-feed="{f}" data-feeds="{cfg["feeds"]}" data-version="${{DesignVersion.val}}" data-session="${{SessionKey.val}}"></div>]]></html>')
    x.append(f'<radio label="Feed{f}" type="rating" optional="0" ss:questionClassNames="cf-feed" ss:accordionDisplay="0"><title>Feed {f} of {cfg["feeds"]}</title><comment>Like anything that stands out. Zero likes is valid.</comment><exec>\nfor i in range(1,{cfg["items"]+1}):\n    a = socialDesign[(DesignVersion.val,{f},i)]\n    Feed{f}.rows[i-1].text = \'&lt;p class="cf-copy"&gt;%s&lt;/p&gt;&lt;div class="cf-art"&gt;%s&lt;/div&gt;\' % (res["copy%d" % a[0]], res["image%d" % a[1]])\n</exec>')
    for i in range(1,cfg['items']+1):x.append(f'<row label="r{i}">Item {i}</row>')
    x.append('<col label="c1" value="1">Not exposed under rule</col><col label="c2" value="2">Exposed, not liked</col><col label="c3" value="3">Liked</col></radio><suspend/>')
x.append('<samplesources default="0"><samplesource list="0"><title>Open survey</title><completed>You have already completed this study.</completed><exit cond="qualified">Your responses have been recorded.</exit></samplesource></samplesources></survey>')
(ROOT/'survey.xml').write_text('\n'.join(x))
print('Built',cfg,len(lines)-1,'design rows')
