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
  'description':'Facebook-style native ad-testing feed with original photo assets, fictional profiles, likes, numeric legacy visible time plus 1%/50% full-card cumulative exposure and quality states, assigned from a tab-delimited design file.',
  'platform':'decipher',
  'instructions':f'Use SocialFeed for each task of this {cfg["feeds"]}-feed, {cfg["items"]}-post design. Put tasks 1 through {cfg["feeds"]} once each, in order, in main. Each component includes its own suspend: one component per page. The base owns the single shared CSS/JS pair (including the timing engine), .dat loader, original text/image references, persistent assignment questions and automatic initialization step. Photos load progressively from survey static files with reserved media space; do not embed repeated base64 photos or wait for all images. Preserve all of these. Upload the bundled social-design.dat as a root/system file and all public JPEG files to the survey static folder before compiling XML. Never replace it with browser randomization. Keep native Feed/task and Offer/task labels, fixed response codes 1/2/3, native Continue, zero-like validity and the legacy revision-4 timing rule plus ExposureRevision 1 full-card 1%/50% fields (anyms, halfms, exposurestate), Time/task numeric fields, availability states and creative/context metadata. Visible time is not attention. Retain fictional author/avatar/timestamp rows, Sponsored labels, photo assets, clear ad offers and the blue thumb Like control. Require photo readiness before timing. Do not add real social accounts or dead comment/share/shop controls. Do not add a marketing shell, welcome/review pages, comment/share/composer controls or extra substantive questions. Keep the concise question/instructions and neutral Continue. Do not duplicate task numbers. The universal Questra theme owns the survey frame and common controls; feed styles and placeholders stay scoped to the component. Preserve native navigation; the shared theme intentionally omits progress visualization. Existing native questions can share a feed page when deliberately placed before its suspend; do not add questions to the demo without authorization. The only input is task; other designs, counts, copy/image resources or schema changes require regeneration and native verification. Treat the provided design as a synthetic example, not a statistically optimized experiment.',
  'skeleton_source':skeleton,
  'slots':[{'id':'main','name':'Social feed tasks','description':f'Render SocialFeed tasks 1–{cfg["feeds"]}, one per page. Each component supplies its suspend.'}],
  'template_format_version':2,'template_blueprint_json':None
 },
 'components':[{
  'name':'SocialFeed','description':f'One native ad-testing feed/task, including offer metadata, numeric visible-time/quality fields, {cfg["items"]} fixed display positions, Like controls and a page break. Uses the shared base and its .dat design.',
  'input_schema':{'type':'object','additionalProperties':False,'required':['task'],'properties':{'task':{'type':'string','enum':[str(n) for n in range(1,cfg['feeds']+1)],'description':'Task number in the bundled design. Use each once in order; it determines native labels and offer lookup.'}}},
  'template':component,'output_mode':'xml'
 }],
 'files':[{'name':'social-design.dat','content_type':'text/plain; charset=utf-8','visibility':'private','content_hash':hashlib.sha256(blob).hexdigest(),'data_base64':base64.b64encode(blob).decode()}]
}
for photo in sorted((ROOT/'assets/images').glob('*.jpg')):
    blob=photo.read_bytes()
    export['files'].append({'name':photo.name,'content_type':'image/jpeg','visibility':'public','content_hash':hashlib.sha256(blob).hexdigest(),'data_base64':base64.b64encode(blob).decode()})
(ROOT/'questra-template.json').write_text(json.dumps(export,ensure_ascii=False,indent=2)+'\n')
print('Export built: shared base + reusable feed component + exact .dat file; full XML reconstruction matches')
