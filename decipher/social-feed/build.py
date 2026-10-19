from pathlib import Path
import random,html,json
ROOT=Path(__file__).parent
cfg={'feeds':5,'items':30,'versions':8}
(ROOT/'config.json').write_text(json.dumps(cfg,indent=2)) if not (ROOT/'config.json').exists() else None
cfg=json.loads((ROOT/'config.json').read_text())
assert 1 <= cfg['feeds'] <= 12 and 1 <= cfg['items'] <= 60 and 1 <= cfg['versions'] <= 99, 'Use feeds 1-12, items 1-60, versions 1-99'

# Original organic posts and fictional advertising copy; no borrowed social content.
organic=[
('Kitchen notes','A tray of tomatoes, garlic and chickpeas: roast until the edges catch, then spoon over toast.',9),
('Trail journal','The switchback looks steep from below. From the ridge, the whole valley opens up.',2),
('Around the block','Three painted front doors from a walk with no destination. The yellow one wins today.',3),
('Coastal notebook','Low tide leaves little channels in the sand. Every walk along this shore takes a different route.',4),
('Growing things','Basil cuttings rooted in a glass of water this week. Time to find them a bigger home.',5),
('Reading corner','A short story collection is ideal for the ten minutes between dinner and doing the dishes.',6),
('Studio notes','Try painting the same view with just three colors. The missing colors make you look harder.',7),
('Weekend table','The picnic plan: pears, sharp cheese, a blanket and a place under the trees.',8),
('Kitchen notes','The best part of baking bread is the first slice, still warm enough to melt the butter.',9),
('City rides','A quiet back street can turn a routine bike ride into the nicest part of the day.',10),
('Morning ritual','Today’s coffee experiment: a slightly coarser grind and a slower pour. A softer cup.',1),
('Trail journal','Pack an extra layer for the ridge. The sheltered start tells you very little about the wind above.',2),
('Around the block','A tiny front garden can hold a lot: rosemary by the gate, marigolds along the path.',3),
('Coastal notebook','Sketching boats is mostly an exercise in looking at the spaces between the ropes.',4),
('Growing things','Turn a windowsill pot a quarter turn each week to help the stems grow evenly.',5),
('Reading corner','A book swap idea: tuck a handwritten, spoiler-free recommendation inside the cover.',6),
('Studio notes','A scrap of cardboard makes a surprisingly good paint scraper. These hills started as one broad stroke.',7),
('Weekend table','Cloudy picnic weather has one advantage: the good patch of grass is usually empty.',8),
('Kitchen notes','Save the heel of the loaf. Tomorrow it becomes crunchy crumbs for a bowl of pasta.',9),
('City rides','A short check before leaving: tires firm, brakes responsive, lights working.',10),
('Morning ritual','A favorite mug, a sunny table, and five quiet minutes before the first meeting.',1),
('Trail journal','The long route follows the stream. The short route goes straight up. Today feels like a stream day.',2),
('Around the block','Look up on your next neighborhood walk. There are small architectural details above almost every shop.',3),
('Coastal notebook','The horizon is a useful reminder to leave a little empty space in a drawing.',4),
('Growing things','A finger in the soil is a better watering reminder than a fixed day on the calendar.',5),
('Reading corner','Reading two very different books at once means there is always something for the mood you are in.',6),
('Studio notes','Mix a little of yesterday’s color into today’s palette. A series starts to feel connected.',7),
('Weekend table','An ordinary lunch tastes different outside. Even the nearest patch of green will do.',8),
('Kitchen notes','A small bowl of herby yogurt makes roasted vegetables feel like a complete meal.',9),
('City rides','The route with fewer junctions is sometimes more relaxing than the route with fewer miles.',10)
]
adcopy=[
('Aster Trail','Room for the essentials. The Aster Trail daypack keeps your everyday carry simple.',2,1),
('Aster Trail','From the morning train to the afternoon trail. One daypack, plenty of possibilities.',10,1),
('Aster Trail','Take the scenic route. Carry a lighter plan with the Aster Trail daypack.',2,1),
('Aster Trail','A place for your bottle, your book and whatever the day becomes. Meet the Aster Trail daypack.',8,1),
('Kettle & Kind','Make a little room for the morning. Discover the Kettle & Kind coffee collection.',1,2),
('Kettle & Kind','Your favorite mug deserves a new ritual. Meet the Kettle & Kind morning blend.',9,2),
('Kettle & Kind','A quiet start, one cup at a time. Explore coffee from Kettle & Kind.',1,2),
('Kettle & Kind','Coffee for the moments between plans. Find your next cup with Kettle & Kind.',8,2),
('Leafline Studio','Bring a little green indoors. Meet the windowsill planters from Leafline Studio.',5,3),
('Leafline Studio','A small home for something growing. Discover Leafline Studio planters.',3,3),
('Leafline Studio','Give your favorite corner a fresh start with a Leafline Studio planter.',5,3),
('Leafline Studio','Simple shapes, room to grow. Explore the Leafline Studio planter collection.',7,3)
]
copy=[p[1] for p in organic]+[p[1] for p in adcopy]
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
# Six original product illustrations, two image levels per fictional campaign.
for campaign in range(1,4):
    for variant in range(2):
        bg=['#e8eee4','#d9e6e7','#eee1cb','#e4d2bd','#e4e9d9','#eaded2'][(campaign-1)*2+variant]
        ink=['#557666','#547d8a','#8d5f43','#b77e4f','#69875c','#b17b5d'][(campaign-1)*2+variant]
        start=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 400" role="img" aria-label="Original illustration: '+['Aster Trail daypack','Kettle and Kind coffee','Leafline Studio planter'][campaign-1]+f'"><rect width="800" height="400" fill="{bg}"/><circle cx="630" cy="90" r="110" fill="#fff" opacity=".3"/><ellipse cx="400" cy="345" rx="175" ry="22" fill="{ink}" opacity=".15"/>'
        if campaign==1:
            art=f'<path d="M330 105v-20q0-35 70-35t70 35v20" fill="none" stroke="{ink}" stroke-width="17"/><rect x="290" y="85" width="220" height="255" rx="55" fill="{ink}"/><rect x="315" y="200" width="170" height="108" rx="25" fill="#fff" opacity=".22"/><path d="M330 225h140m-70-125v60" stroke="#eaddbb" stroke-width="7"/><path d="M270 130q-50 50-15 160m275-160q50 50 15 160" fill="none" stroke="{ink}" stroke-width="18"/><path d="M390 145l10-18 10 18" fill="none" stroke="#eaddbb" stroke-width="4"/>'
        elif campaign==2:
            art=f'<path d="M280 70h180l15 260H265Z" fill="{ink}"/><path d="M280 70h180l-10 28H290Z" fill="#fff" opacity=".25"/><rect x="290" y="145" width="150" height="100" rx="5" fill="#fff6e5"/><text x="365" y="188" text-anchor="middle" font-family="Georgia,serif" font-size="21" fill="{ink}">KETTLE</text><text x="365" y="219" text-anchor="middle" font-family="Georgia,serif" font-size="21" fill="{ink}">&amp; KIND</text><path d="M505 235h115v60q0 40-58 40t-57-40z" fill="#fff6e5"/><path d="M620 245q55-8 40 35-7 20-40 10" fill="none" stroke="#fff6e5" stroke-width="14"/><ellipse cx="562" cy="235" rx="57" ry="12" fill="#694836"/>'
        else:
            art=f'<path d="M290 220h220l-30 120H320Z" fill="{ink}"/><path d="M400 225V75m0 100-70-55m70 80 65-50" fill="none" stroke="#526e42" stroke-width="10"/><ellipse cx="338" cy="115" rx="55" ry="27" transform="rotate(30 338 115)" fill="#708c53"/><ellipse cx="455" cy="135" rx="58" ry="28" transform="rotate(-30 455 135)" fill="#8ba16b"/><ellipse cx="400" cy="70" rx="27" ry="50" transform="rotate(15 400 70)" fill="#607c49"/><path d="M325 260h150m-140 25h130" stroke="#fff" opacity=".25" stroke-width="7"/>'
        scenes.append(start+art+'</svg>')
# A real version/task/concept .dat design: all content/creative choices are fixed here.
lines=['Version\tTask\tConcept\tCopy\tImage\tOrder\tItem\tKind\tCreative\tCampaign\tContext']
for v in range(1,cfg['versions']+1):
    rng=random.Random(78131+v)
    for f in range(1,cfg['feeds']+1):
        copies=list(range(1,31));rng.shuffle(copies)
        # One sponsored placement per five positions; positions vary by assigned version/task.
        ads={start+rng.randrange(min(5,cfg['items']-start))+1 for start in range(0,cfg['items'],5)}
        creatives=list(range(24));rng.shuffle(creatives)
        oi=0;ai=0
        for i in range(1,cfg['items']+1):
            kind=int(i in ads)
            if kind:
                combination=creatives[ai%24];ai+=1;creative=combination//2;c=31+creative;campaign=adcopy[creative][3];im=11+(campaign-1)*2+combination%2;creative=10000+c*100+im
            else:
                c=copies[oi%30];oi+=1;im=organic[c-1][2];creative=0;campaign=0
            lines.append('\t'.join(map(str,[v,f,i,c,im,i,(f-1)*cfg['items']+i,kind,creative,campaign,f])))
(ROOT/'social-design.dat').write_text('\n'.join(lines)+'\n')
css=(ROOT/'src/feed.css').read_text().replace('@','\\@')
js=(ROOT/'src/timing.js').read_text()+'\n'+(ROOT/'src/feed.js').read_text()
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
for i,c in enumerate(copy,1):
    x.append(f'<res label="copy{i}">{html.escape(c)}</res>')
    label=organic[i-1][0] if i<=30 else 'Sponsored · '+adcopy[i-31][0]
    x.append(f'<res label="byline{i}">{html.escape(label)}</res>')
for i,svg in enumerate(scenes,1):x.append(f'<res label="image{i}"><![CDATA[{svg}]]></res>')
x.append(f'''<number label="DesignVersion" where="execute" size="3"><title>Assigned .dat design version</title><exec>
if DesignVersion.val is None:
    DesignVersion.val = random.randint(1,{cfg['versions']})
</exec></number>
<number label="DesignRevision" where="execute" size="2"><title>Design and timing schema revision</title><exec>DesignRevision.val = 2</exec></number>
<number label="SessionKey" where="execute" size="12"><title>Anonymous response cache key</title><exec>
if SessionKey.val is None:
    SessionKey.val = random.randint(100000000,999999999)
</exec></number>
<html label="Initialize" where="survey">Loading…</html><suspend/>''')
for f in range(1,cfg['feeds']+1):
    x.append(f'<number label="Offer{f}" where="execute" optional="1" size="6"><title>Feed {f}: assigned design metadata by display position</title>')
    for i in range(1,cfg['items']+1):x.append(f'<row label="r{i}">Position {i}</row>')
    for label,title in [('task','Feed task'),('item','Item identity'),('order','Display order'),('copy','Copy level'),('image','Image level'),('kind','0 organic; 1 sponsored'),('creative','Creative identity; 0 organic'),('campaign','Campaign identity; 0 organic'),('context','Feed context identity')]:x.append(f'<col label="{label}">{title}</col>')
    x.append(f'''<exec>
for i in range(1,{cfg['items']+1}):
    a = socialDesign[(DesignVersion.val,{f},i)]
    r = Offer{f}.rows[i-1]
    r.task.val = {f}
    r.item.val = a[3]
    r.order.val = a[2]
    r.copy.val = a[0]
    r.image.val = a[1]
    r.kind.val = a[4]
    r.creative.val = a[5]
    r.campaign.val = a[6]
    r.context.val = a[7]
</exec></number>''')
    x.append(f'<number label="Time{f}" optional="1" size="12" ss:questionClassNames="cf-timing"><title>Visible time measurement</title>')
    for i in range(1,cfg['items']+1):x.append(f'<row label="r{i}">Position {i}</row>')
    x.append('<col label="ms">Visible milliseconds</col><col label="state">Measurement state</col>')
    x.append(f'''<exec>
for r in Time{f}.rows:
    if r.ms.val is None: r.ms.val = -1
    if r.state.val is None: r.state.val = 0
</exec></number>''')
    x.append(f'<html label="Header{f}" where="survey"><![CDATA[<div class="cf-config" data-revision="2" data-feed="{f}" data-feeds="{cfg["feeds"]}" data-version="${{DesignVersion.val}}" data-session="${{SessionKey.val}}"></div>]]></html>')
    x.append(f'<radio label="Feed{f}" type="rating" optional="0" ss:questionClassNames="cf-feed" ss:accordionDisplay="0"><title>Feed {f} of {cfg["feeds"]}</title><comment>Like anything that stands out. Zero likes is valid.</comment><exec>\nfor i in range(1,{cfg["items"]+1}):\n    a = socialDesign[(DesignVersion.val,{f},i)]\n    Feed{f}.rows[i-1].text = \'&lt;div class="cf-source"&gt;%s&lt;/div&gt;&lt;p class="cf-copy"&gt;%s&lt;/p&gt;&lt;div class="cf-art"&gt;%s&lt;/div&gt;\' % (res["byline%d" % a[0]], res["copy%d" % a[0]], res["image%d" % a[1]])\n</exec>')
    for i in range(1,cfg['items']+1):x.append(f'<row label="r{i}">Item {i}</row>')
    x.append('<col label="c1" value="1">Not exposed under rule</col><col label="c2" value="2">Exposed, not liked</col><col label="c3" value="3">Liked</col></radio><suspend/>')
x.append('<samplesources default="0"><samplesource list="0"><title>Open survey</title><completed>You have already completed this study.</completed><exit cond="qualified">Your responses have been recorded.</exit></samplesource></samplesources></survey>')
(ROOT/'survey.xml').write_text('\n'.join(x))
print('Built',cfg,len(lines)-1,'design rows')
