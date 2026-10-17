"""Headless flow tests for The Phish Store. Run: python3 tests/flow_test.py
Needs: pip install playwright && playwright install chromium
Uses a fake window.claude so no network or Claude account is needed.
"""
import asyncio, json, sys
from playwright.async_api import async_playwright
import pathlib
F=str(pathlib.Path(__file__).resolve().parent.parent/"index.html")
SHOTS=pathlib.Path(__file__).resolve().parent/"shots"; SHOTS.mkdir(exist_ok=True)
MOCK="""
window.__fail=false; window.__db={};
const reply=()=>JSON.stringify({reply:'Hi, this is Dana. Who is this?',suspicion_delta:3,hangup:false,flag_leaked:false});
const sample=async(input,opts)=>{ if(window.__fail) throw {code:'upstream_error',message:'x'}; return {text:reply(),truncated:false}; };
sample.json=async(input,opts)=>{ if(window.__fail) throw {code:'upstream_error',message:'x'};
  return {click_rate:34,report_rate:12,segments:[{name:'Call center',clicked:50,note:'busy'}],weakest_segment:'IT',dominant_lever:'urgency',analyst_note:'ok'}; };
const db={doc:(p)=>({get:async()=>({exists:p in window.__db,data:()=>window.__db[p]}),set:async(d)=>{window.__db[p]=d;}})};
window.claude={use:async(n)=>n==='sample'?sample:n==='db'?db:null};
"""
ok=True
def check(name,cond,extra=""):
    global ok
    print(("PASS " if cond else "FAIL ")+name+(" "+str(extra) if extra and not cond else ""))
    if not cond: ok=False
async def run(b,tag,w,h):
    pg=await b.new_page(viewport={"width":w,"height":h})
    errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.add_init_script(MOCK)
    await pg.route("**/fonts.googleapis.com/**",lambda r:r.abort())
    await pg.goto("file://"+F); await pg.wait_for_timeout(700)
    ev=pg.evaluate
    await pg.fill("input","Derrick"); await ev("confirmCallsign()"); await pg.wait_for_timeout(400); await ev("endOnboarding()")
    # 1 home mode click lands on single page with that mode chosen
    await pg.click("text=Spear Phishing >> nth=0"); await pg.wait_for_timeout(500)
    check(tag+" home->select keeps mode", await ev("ui.screen")=="select" and await ev("ui.selMode")=="phishing")
    check(tag+" no second mode prompt (all 3 sections visible)", await pg.locator(".mode-btn").count()==3 and await pg.locator(".case-row").count()==3 and await pg.locator(".diff-card").count()==5)
    await pg.screenshot(path=f"{SHOTS}/{tag}_select.png",full_page=(tag=="m"))
    await pg.click(".mode-btn >> nth=0"); await pg.wait_for_timeout(300)
    check(tag+" mode switch resets case", await ev("ui.selMode")=="vishing" and await ev("ui.selCaseId")=="VSH-01")
    await pg.click(".case-row >> nth=2"); await pg.click(".diff-card >> nth=1"); await pg.wait_for_timeout(300)
    check(tag+" case+diff pick", await ev("ui.selCaseId")=="VSH-03" and await ev("ui.selDiffId")=="medium")
    check(tag+" launch bar summarizes", "Exec Assistant" in await pg.inner_text(".launch-bar"))
    # 2 launch + timer pauses while loading
    await pg.click(".launch-btn"); await pg.wait_for_timeout(900)
    check(tag+" call screen", await ev("ui.screen")=="call")
    s0=await ev("call.seconds"); await ev("call.loading=true"); await pg.wait_for_timeout(2200); s1=await ev("call.seconds"); await ev("call.loading=false")
    check(tag+" timer paused while loading", s0==s1,(s0,s1))
    # 3 hints failure not counted; success counted
    await ev("window.__fail=true"); await ev("setTool('hints')"); await ev("requestHint()"); await pg.wait_for_timeout(600)
    check(tag+" failed hint not counted", await ev("call.assisted")==False and await ev("call.hints.length")==0)
    await ev("window.__fail=false"); await ev("requestHint()"); await pg.wait_for_timeout(600)
    check(tag+" good hint counted", await ev("call.assisted")==True and await ev("call.hints.length")==1)
    # hint requested then tab switched: transcript survives
    await pg.fill("#composer-input","Hello"); await pg.keyboard.press("Enter"); await pg.wait_for_timeout(700)
    n0=await pg.locator("#msgs .msg").count()
    await ev("requestHint()"); await ev("setTool('notes')"); await pg.wait_for_timeout(700)
    check(tag+" transcript survives hint on other tab", await pg.locator("#msgs .msg").count()==n0)
    # 4 End needs two clicks
    await pg.click(".dock-btn.danger"); await pg.wait_for_timeout(200)
    check(tag+" End first click only arms", await ev("ui.screen")=="call")
    await pg.click(".dock-btn.danger"); await pg.wait_for_timeout(400)
    check(tag+" End second click ends", await ev("ui.screen")=="end")
    # 5 end screen actions
    await ev("changeDifficulty()"); await pg.wait_for_timeout(300)
    check(tag+" change difficulty -> select", await ev("ui.screen")=="select")
    # 6 callsign change returns to profile
    await ev("goProfile()"); await ev("changeCallsign()"); await pg.wait_for_timeout(200)
    check(tag+" gate has site chrome", await pg.locator(".site-header").count()==1)
    await pg.click("text=Cancel"); await pg.wait_for_timeout(200)
    check(tag+" cancel -> profile", await ev("ui.screen")=="profile")
    await ev("changeCallsign()"); await pg.fill("#gate-input","Derrick2"); await ev("confirmCallsign()"); await pg.wait_for_timeout(300)
    check(tag+" save -> profile", await ev("ui.screen")=="profile")
    # 7 campaign: empty send, failure keeps draft, success lands on results
    await ev("ui.selMode='mass';ui.selCaseId='MSS-01';ui.selDiffId='easy';launchCall()"); await pg.wait_for_timeout(400)
    await ev("setCampTool('compose')"); await ev("launchRound()"); await pg.wait_for_timeout(200)
    check(tag+" empty lure blocked", await ev("campaign.round")==0)
    await pg.fill("#camp-body","Please review the attached policy update."); 
    await ev("window.__fail=true"); await ev("launchRound()"); await pg.wait_for_timeout(500)
    check(tag+" failed send keeps draft", await ev("campaign.lure.body")!="" and await ev("campaign.round")==0)
    await ev("window.__fail=false"); await ev("launchRound()"); await pg.wait_for_timeout(700)
    check(tag+" good send -> results tab", await ev("campaign.round")==1 and await ev("campaign.activeTool")=="results" and await pg.locator("#camp-feed").count()==1)
    await pg.screenshot(path=f"{SHOTS}/{tag}_camp_results.png")
    check(tag+" dock highlight matches tool", "results" in (await pg.inner_text(".dock-btn.active")).lower())
    # 8 nav guard in mission
    await ev("navAway('goHome')"); check(tag+" nav guard first click stays", await ev("ui.screen")=="campaign")
    await ev("navAway('goHome')"); await pg.wait_for_timeout(200); check(tag+" nav guard second click leaves", await ev("ui.screen")=="home")
    print(tag,"page errors",errs); 
    if errs: globals()['ok']=False
    await pg.close()
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        await run(b,"d",1280,800); await run(b,"m",390,844)
        await b.close()
    print("ALL OK" if ok else "FAILURES")
asyncio.run(main())
