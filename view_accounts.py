# view_accounts.py
# 用于查看已创建的Cursor账号信息

import os
import re
import sys
from colorama import Fore, Style, init

# 初始化colorama
init()

# 定义ASCII字符替代emoji，解决Windows下显示问题
ASCII_EMOJI = {
    'FILE': '[F]',
    'ACCOUNTS': '[A]',
    'ERROR': '[X]',
    'INFO': '[i]',
    'SUCCESS': '[√]',
    'EMPTY': '[E]',
    'BACK': '[<]'
}

class AccountsViewer:
    def __init__(self, translator=None):
        self.translator = translator
        self.accounts_file = 'cursor_accounts.txt'
        
        # 设置控制台编码为UTF-8
        try:
            if sys.platform == 'win32':
                import ctypes
                kernel32 = ctypes.windll.kernel32
                kernel32.SetConsoleOutputCP(65001)  # 设置为UTF-8编码
        except Exception:
            pass
            
    def read_accounts_file(self):
        """读取账号信息文件"""
        accounts = []
        try:
            # 检查文件是否存在
            if not os.path.exists(self.accounts_file):
                return []
                
            with open(self.accounts_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 使用正则表达式提取账号信息块
            account_blocks = re.split(r'\n={50}\n', content)
            
            for block in account_blocks:
                if not block.strip():
                    continue
                    
                account = {}
                # 提取邮箱
                email_match = re.search(r'Email: (.+)', block)
                if email_match:
                    account['email'] = email_match.group(1).strip()
                    
                # 提取密码
                password_match = re.search(r'Password: (.+)', block)
                if password_match:
                    account['password'] = password_match.group(1).strip()
                    
                # 提取Token
                token_match = re.search(r'Token: (.+)', block)
                if token_match:
                    account['token'] = token_match.group(1).strip()
                    
                # 提取使用限制
                usage_match = re.search(r'Usage Limit: (.+)', block)
                if usage_match:
                    account['usage_limit'] = usage_match.group(1).strip()
                    
                if account:
                    accounts.append(account)
                    
            return accounts
        except Exception as e:
            print(f"{Fore.RED}{ASCII_EMOJI['ERROR']} {self.translator.get('accounts.read_error', error=str(e))}{Style.RESET_ALL}")
            return []

    def display_accounts(self, accounts):
        """显示账号信息"""
        if not accounts:
            print(f"\n{Fore.YELLOW}{ASCII_EMOJI['EMPTY']} {self.translator.get('accounts.no_accounts')}{Style.RESET_ALL}")
            return
            
        print(f"\n{Fore.CYAN}{ASCII_EMOJI['ACCOUNTS']} {self.translator.get('accounts.total_count', count=len(accounts))}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'─' * 60}{Style.RESET_ALL}")
        
        for i, account in enumerate(accounts, 1):
            print(f"{Fore.GREEN}[{i}]{Style.RESET_ALL} {Fore.CYAN}{self.translator.get('accounts.account_info')}:{Style.RESET_ALL}")
            print(f"  {Fore.YELLOW}Email:{Style.RESET_ALL} {account.get('email', 'N/A')}")
            print(f"  {Fore.YELLOW}{self.translator.get('accounts.password')}:{Style.RESET_ALL} {account.get('password', 'N/A')}")
            
            # 显示Token的前10个字符和后5个字符，中间用...替代
            token = account.get('token', 'N/A')
            if token != 'N/A' and len(token) > 15:
                token = f"{token[:10]}...{token[-5:]}"
            print(f"  {Fore.YELLOW}Token:{Style.RESET_ALL} {token}")
            
            print(f"  {Fore.YELLOW}{self.translator.get('accounts.usage_limit')}:{Style.RESET_ALL} {account.get('usage_limit', 'N/A')}")
            print(f"{Fore.YELLOW}{'─' * 60}{Style.RESET_ALL}")

    def start(self):
        """启动查看账号信息流程"""
        print(f"\n{Fore.CYAN}{'═' * 60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{ASCII_EMOJI['FILE']} {self.translator.get('accounts.title')}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'═' * 60}{Style.RESET_ALL}")
        
        accounts = self.read_accounts_file()
        self.display_accounts(accounts)
        
        print(f"\n{Fore.CYAN}{'═' * 60}{Style.RESET_ALL}")
        input(f"{ASCII_EMOJI['BACK']} {self.translator.get('accounts.press_enter')}...")
        return True

def main(translator=None):
    """主函数，供main.py调用"""
    viewer = AccountsViewer(translator)
    return viewer.start()
    
if __name__ == "__main__":
    # 如果直接运行此脚本，创建一个简单的翻译器
    class SimpleTranslator:
        def get(self, key, **kwargs):
            translations = {
                'accounts.title': '查看Cursor账号信息',
                'accounts.no_accounts': '没有找到任何账号信息',
                'accounts.total_count': '共找到 {count} 个账号',
                'accounts.account_info': '账号信息',
                'accounts.password': '密码',
                'accounts.usage_limit': '使用限制',
                'accounts.press_enter': '按Enter键返回主菜单...',
                'accounts.read_error': '读取账号文件时出错: {error}'
            }
            result = translations.get(key, key)
            return result.format(**kwargs) if kwargs else result
            
    main(SimpleTranslator())