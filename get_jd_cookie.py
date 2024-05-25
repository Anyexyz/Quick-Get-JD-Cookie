import asyncio
from socket import timeout
import os
import pyperclip
from playwright.async_api import async_playwright

def find_cookie(cookies):   # 从 cookie 中提取 pt_pin 和 pt_key
    """从cookie中提取pt_pin和pt_key
    """
    for item in cookies.split('; '):
        if 'pt_pin' in item:
            pt_pin = item
        if 'pt_key' in item:
            pt_key = item
    jd_cookie = pt_pin+';'+pt_key+';'
    pyperclip.copy(jd_cookie)
    print("Cookie:", jd_cookie)
    print("已拷贝Cookie到剪切板.")
    os.system('pause')  # 按任意键继续

async def main():   # 使用Playwright库来登录京东、并获取cookie
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path = 'C:\\Users\\Anye\\AppData\\Local\\Chromium\\Application\\chrome.exe', headless=False, args=['--no-sandbox', '--window-size=1000,800', '--disable-infobars'])
        context = await browser.new_context()
        page = await context.new_page()           # 打开新的标签页
        await page.set_viewport_size({'width': 404, 'height': 678})      # 页面大小一致
        await page.goto('https://my.m.jd.com/',timeout=1000*60)
        # 等待页面加载完成
        await page.wait_for_load_state('domcontentloaded')
        # 检查页面是否跳转到登录页面
        if 'plogin.m.jd.com' in page.url:
            print("Redirected to login page. Logging in...")
            # 等待页面加载完成
            await page.wait_for_load_state('domcontentloaded')
            # 点击 已阅读并同意
            await page.click('.policy_tip-checkbox')
        try:
            await page.wait_for_timeout(1000)
            elm = await page.wait_for_selector('//*[@id="myHeader"]', timeout=0)
            if elm:
                cookie = await context.cookies()
                cookies_temp = []
                for i in cookie:
                    cookies_temp.append('{}={}'.format(i["name"], i["value"]))
                cookies = '; '.join(cookies_temp)
                find_cookie(cookies)
        except Exception as e:
            print(f"Error during cookie retrieval: {e}")
            return False, f"Error during cookie retrieval: {str(e)}"
        finally:
            await browser.close()  # 确保无论如何都关闭浏览器

if __name__== "__main__":
    asyncio.run(main())