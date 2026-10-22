from pathlib import Path
import random,html,json
ROOT=Path(__file__).parent
cfg={'feeds':5,'items':20,'versions':8}
(ROOT/'config.json').write_text(json.dumps(cfg,indent=2)) if not (ROOT/'config.json').exists() else None
cfg=json.loads((ROOT/'config.json').read_text())
assert 1 <= cfg['feeds'] <= 12 and 1 <= cfg['items'] <= 60 and 1 <= cfg['versions'] <= 99, 'Use feeds 1-12, items 1-60, versions 1-99'

# Original fictional content and AI-generated photos live in a portable registry.
import base64
content=json.loads((ROOT/'content.json').read_text())
organic=content['organic'];adcopy=content['ads']
copy=[p['copy'] for p in organic]+[p['copy'] for p in adcopy]
assert len(organic)==30 and len(adcopy)==12 and len(content['images'])==16
images=[]
for level,description in enumerate(content['images'],1):
    images.append(f'<img data-src="[rel image-{level:02d}.jpg]" alt="{html.escape(description,quote=True)}" width="800" height="600" decoding="async"/>')
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
                combination=creatives[ai%24];ai+=1;creative=combination//2;c=31+creative;campaign=adcopy[creative]['campaign'];im=11+(campaign-1)*2+combination%2;creative=10000+c*100+im
            else:
                c=copies[oi%30];oi+=1;im=organic[c-1]['image'];creative=0;campaign=0
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
globe='<svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="6.3" fill="currentColor"/><path d="M5 2.8l.8 2.4-1.4 2.1 2.5.9.8 3.3 1.4 1.2 1.4-2.3-.5-2.4 2.4-1.5-2.1-1.3L9 2" fill="white"/></svg>'
for i,c in enumerate(copy,1):
    x.append(f'<res label="copy{i}">{html.escape(c)}</res>')
    record=organic[i-1] if i<=30 else adcopy[i-31]
    name=record['author'] if i<=30 else record['brand']
    if i<=30:
        avatarfile=f"avatar-{record['image']:02d}.jpg"
        avatarhtml=f'<img class="cf-avatar" data-src="[rel {avatarfile}]" width="40" height="40" alt=""/>'
        sub=record['time'];offer=''
    else:
        initials=['AT','K&amp;K','L'][record['campaign']-1]
        avatarhtml=f'<span class="cf-avatar cf-brand-avatar cf-brand-{record["campaign"]}" aria-hidden="true">{initials}</span>'
        sub='Sponsored'
        offer=f'<div class="cf-offer"><div class="cf-domain">{record["domain"]}</div><div class="cf-offer-title">{html.escape(record["headline"])}</div><div class="cf-offer-detail">{html.escape(record["offer"])}</div></div>'
    byline=f'<div class="cf-author-row">{avatarhtml}<div class="cf-author-details"><div class="cf-source">{html.escape(name)}</div><div class="cf-post-meta"><span>{sub}</span><span aria-hidden="true"> · </span>{globe}</div></div></div>'
    x.append(f'<res label="byline{i}"><![CDATA[{byline}]]></res>')
    x.append(f'<res label="offer{i}"><![CDATA[{offer}]]></res>')
for i,photo in enumerate(images,1):x.append(f'<res label="image{i}"><![CDATA[{photo}]]></res>')
x.append(f'''<number label="DesignVersion" where="execute" size="3"><title>Assigned .dat design version</title><exec>
if DesignVersion.val is None:
    DesignVersion.val = random.randint(1,{cfg['versions']})
</exec></number>
<number label="DesignRevision" where="execute" size="2"><title>Design and timing schema revision</title><exec>DesignRevision.val = 5</exec></number>
<number label="ExposureRevision" where="execute" size="2"><title>Full-card exposure schema revision</title><exec>ExposureRevision.val = 1</exec></number>
<number label="SessionKey" where="execute" size="12"><title>Anonymous response cache key</title><exec>
if SessionKey.val is None:
    SessionKey.val = random.randint(100000000,999999999)
</exec></number>
<html label="Initialize" where="survey"><![CDATA[<div class="cf-init" role="status"><div class="cf-round">Feed 1 of {cfg['feeds']}</div><h2>Like the posts that stand out to you</h2><p>Browse the feed and tap Like, or double-tap an image. Tap again to undo. It’s fine to leave a feed without liking anything.</p><div class="cf-skeleton" aria-label="Preparing feed"></div></div>]]></html><suspend/>''')
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
    x.append('<col label="ms">Visible milliseconds</col><col label="state">Legacy measurement state</col><col label="anyms">Cumulative milliseconds at least 1 percent full card visible</col><col label="halfms">Cumulative milliseconds at least 50 percent full card visible</col><col label="exposurestate">Full-card exposure measurement state</col>')
    x.append(f'''<exec>
for r in Time{f}.rows:
    if r.ms.val is None: r.ms.val = -1
    if r.state.val is None: r.state.val = 0
    if r.anyms.val is None: r.anyms.val = -1
    if r.halfms.val is None: r.halfms.val = -1
    if r.exposurestate.val is None: r.exposurestate.val = 0
</exec></number>''')
    x.append(f'<html label="Header{f}" where="survey"><![CDATA[<div class="cf-config" data-revision="5" data-feed="{f}" data-feeds="{cfg["feeds"]}" data-version="${{DesignVersion.val}}" data-session="${{SessionKey.val}}"></div>]]></html>')
    x.append(f'<radio label="Feed{f}" type="rating" optional="0" ss:questionClassNames="cf-feed" ss:accordionDisplay="0"><title><![CDATA[<span class="cf-round">Feed {f} of {cfg["feeds"]}</span>Like the posts that stand out to you]]></title><comment>Browse the feed and tap Like, or double-tap an image. Tap again to undo. It’s fine to leave a feed without liking anything.</comment><exec>\nfor i in range(1,{cfg["items"]+1}):\n    a = socialDesign[(DesignVersion.val,{f},i)]\n    Feed{f}.rows[i-1].text = \'%s&lt;p class="cf-copy"&gt;%s&lt;/p&gt;&lt;div class="cf-art"&gt;%s&lt;/div&gt;%s\' % (res["byline%d" % a[0]], res["copy%d" % a[0]], res["image%d" % a[1]], res["offer%d" % a[0]])\n</exec>')
    for i in range(1,cfg['items']+1):x.append(f'<row label="r{i}">Item {i}</row>')
    x.append('<col label="c1" value="1">Not exposed under rule</col><col label="c2" value="2">Exposed, not liked</col><col label="c3" value="3">Liked</col></radio><suspend/>')
x.append('<samplesources default="0"><samplesource list="0"><title>Open survey</title><completed>You have already completed this study.</completed><exit cond="qualified">Your responses have been recorded.</exit></samplesource></samplesources></survey>')
xml='\n'.join(x)
# Preserve the existing deployed shell without requiring another example's build.
head=(ROOT/'src/theme-head.html').read_text()
footer=(ROOT/'src/theme-footer.xml').read_text()
xml=xml.replace('<![CDATA[\n<style>', '<![CDATA[\n'+head+'\n<style>', 1)
xml=xml.replace('</survey>',footer+'\n</survey>')
(ROOT/'survey.xml').write_text(xml)
print('Built',cfg,len(lines)-1,'design rows')

# Apply shared page theme after component generation.
import runpy
theme = runpy.run_path(str(ROOT.parent / "theme" / "build.py"))
(ROOT / "survey.xml").write_text(theme["apply"]((ROOT / "survey.xml").read_text()))
