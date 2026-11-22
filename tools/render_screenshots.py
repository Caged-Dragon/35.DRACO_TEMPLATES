import json, sys, asyncio
from playwright.async_api import async_playwright
REPO=sys.argv[1]; entries=json.load(open(sys.argv[2]))
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        sem=asyncio.Semaphore(6); problems=[]
        async def one(e):
            async with sem:
                ctx=await b.new_context(viewport={'width':1280,'height':800})
                pg=await ctx.new_page()
                errs=[]
                pg.on('pageerror',lambda x:errs.append('pageerror:'+str(x)))
                pg.on('console',lambda m:errs.append('console:'+m.text) if m.type=='error' and 'ERR_' not in m.text and 'Failed to load' not in m.text else None)
                await pg.route('**/*',lambda r: r.continue_() if r.request.url.startswith('file:') else r.abort())
                await pg.goto(f"file://{REPO}/{e['live']}?palette={e['palette']}")
                await pg.wait_for_selector('html.ready',state='attached',timeout=5000); await pg.wait_for_timeout(120)
                # horizontal overflow check
                ov=await pg.evaluate("document.documentElement.scrollWidth-document.documentElement.clientWidth")
                if ov>2: errs.append(f'h-overflow {ov}')
                await pg.screenshot(path=f"{REPO}/{e['preview']}")
                await ctx.close()
                if errs: problems.append((e['id'],errs))
        await asyncio.gather(*[one(e) for e in entries])
        await b.close()
        print('problems',len(problems))
        for x in problems[:20]: print(x)
asyncio.run(main())
