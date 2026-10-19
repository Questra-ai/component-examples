"""Build a Questra transfer-format export from the deployed native source."""
from pathlib import Path
import base64,hashlib,json,re
ROOT=Path(__file__).resolve().parent
xml=(ROOT/'survey.xml').read_text()
cfg=json.loads((ROOT/'config.json').read_text())
blocks=re.findall(r'<number label="Offer\d+"[\s\S]*?</radio><suspend/>',xml)
assert len(blocks)==cfg['feeds']
component=blocks[0].replace('Offer1','Offer@{task}').replace('Time1','Time@{task}').replace('Header1','Header@{task}').replace('Feed1','Feed@{task}').replace('Feed 1:', 'Feed @{task}:').replace('Feed 1 of','Feed @{task} of').replace('data-feed="1"','data-feed="@{task}"').replace('DesignVersion.val,1,i','DesignVersion.val,@{task},i').replace('r.task.val = 1','r.task.val = @{task}')
for n,block in enumerate(blocks,1):
    assert component.replace('@{task}',str(n))==block, 'Feed component differs from live XML'
start=xml.index(blocks[0]);end=xml.index(blocks[-1])+len(blocks[-1])
skeleton=xml[:start]+'{{slot:main}}'+xml[end:]
reconstructed=skeleton.replace('{{slot:main}}','\n'.join(component.replace('@{task}',str(n)) for n in range(1,cfg['feeds']+1)))
assert reconstructed==xml
blob=(ROOT/'social-design.dat').read_bytes()
export={
 'format':'questra-fine-tuning-template','version':1,'exported_at':'2026-10-19T00:00:00.000Z',
 'template':{
  'name':'Social feed — Decipher',
  'description':'Native ad-testing feed with likes, numeric visible time and measurement quality states, assigned from a tab-delimited design file.',
  'platform':'decipher',
  'instructions':f'Use SocialFeed for each task of this {cfg["feeds"]}-feed, {cfg["items"]}-post design. Put tasks 1 through {cfg["feeds"]} once each, in order, in main. Each component includes its own suspend: one component per page. The base owns the single shared CSS/JS pair (including the timing engine), .dat loader, original text/image resources, persistent assignment questions and automatic initialization step. Preserve all of these. Upload the bundled social-design.dat as a root/system file before compiling XML. Never replace it with browser randomization. Keep native Feed/task and Offer/task labels, fixed response codes 1/2/3, native Continue, zero-like validity and the revision-2 timing rule, Time/task numeric fields, availability states and creative/context metadata. Visible time is not attention. Retain sponsored/organic source labels. Do not add marketing headers, footers, welcome pages, review pages, marketing copy or extra substantive questions. Keep the concise question/instructions and neutral Continue. Do not duplicate task numbers or place other visible questions on feed pages. The only input is task; other designs, counts, copy/image resources or schema changes require regeneration and native verification. Treat the provided design as a synthetic example, not a statistically optimized experiment.',
  'skeleton_source':skeleton,
  'slots':[{'id':'main','name':'Social feed tasks','description':f'Render SocialFeed tasks 1–{cfg["feeds"]}, one per page. Each component supplies its suspend.'}],
  'template_format_version':2,'template_blueprint_json':None
 },
 'components':[{
  'name':'SocialFeed','description':'One native ad-testing feed/task, including offer metadata, numeric visible-time/quality fields, 30 fixed display positions, Like controls and a page break. Uses the shared base and its .dat design.',
  'input_schema':{'type':'object','additionalProperties':False,'required':['task'],'properties':{'task':{'type':'string','enum':[str(n) for n in range(1,cfg['feeds']+1)],'description':'Task number in the bundled design. Use each once in order; it determines native labels and offer lookup.'}}},
  'template':component,'output_mode':'xml'
 }],
 'files':[{'name':'social-design.dat','content_type':'text/plain; charset=utf-8','visibility':'private','content_hash':hashlib.sha256(blob).hexdigest(),'data_base64':base64.b64encode(blob).decode()}]
}
(ROOT/'questra-template.json').write_text(json.dumps(export,ensure_ascii=False,indent=2)+'\n')
print('Export built: shared base + reusable feed component + exact .dat file; full XML reconstruction matches')
