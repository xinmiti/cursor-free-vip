# view_accounts.py
# 用于查看已创建的Cursor账号信息

import os
import re
from colorama import Fore, Style, init

# 初始化colorama
init()

# 定义emoji常量
EMOJI = {
    'FILE': '📄',
    'ACCOUNTS': '👤',
    'ERROR': '❌',
    'INFO': 'ℹ️',
    'SUCCESS': '✅',
    'EMPTY': '📭',
    'BACK': '🔙'
}

def read_accounts_file():
    """读取账号信息文件"""
    accounts = []
    try:
        # 检查文件是否存在
        if not os.path.exists('cursor_accounts.txt'):
            return []
            
        with open('cursor_accounts.txt', 'r', encoding='utf-8') as f:
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
        print(f"{Fore.RED}{EMOJI['ERROR']} 读取账号文件时出错: {str(e)}{Style.RESET_ALL}")
        return []

def display_accounts(accounts, translator):
    """显示账号信息"""
    if not accounts:
        print(f"\n{Fore.YELLOW}{EMOJI['EMPTY']} {translator.get('accounts.no_accounts')}{Style.RESET_ALL}")
        return
        
    print(f"\n{Fore.CYAN}{EMOJI['ACCOUNTS']} {translator.get('accounts.total_count', count=len(accounts))}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'─' * 60}{Style.RESET_ALL}")
    
    for i, account in enumerate(accounts, 1):
        print(f"{Fore.GREEN}[{i}]{Style.RESET_ALL} {Fore.CYAN}{translator.get('accounts.account_info')}:{Style.RESET_ALL}")
        print(f"  {Fore.YELLOW}Email:{Style.RESET_ALL} {account.get('email', 'N/A')}")
        print(f"  {Fore.YELLOW}{translator.get('accounts.password')}:{Style.RESET_ALL} {account.get('password', 'N/A')}")
        
        # 显示Token的前10个字符和后5个字符，中间用...替代
        token = account.get('token', 'N/A')
        if token != 'N/A' and len(token) > 15:
            token = f"{token[:10]}...{token[-5:]}"
        print(f"  {Fore.YELLOW}Token:{Style.RESET_ALL} {token}")
        
        print(f"  {Fore.YELLOW}{translator.get('accounts.usage_limit')}:{Style.RESET_ALL} {account.get('usage_limit', 'N/A')}")
        print(f"{Fore.YELLOW}{'─' * 60}{Style.RESET_ALL}")

def main(translator):
    """主函数"""
    print(f"\n{Fore.CYAN}{'═' * 60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{EMOJI['FILE']} {translator.get('accounts.title')}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'═' * 60}{Style.RESET_ALL}")
    
    accounts = read_accounts_file()
    display_accounts(accounts, translator)
    
    print(f"\n{Fore.CYAN}{'═' * 60}{Style.RESET_ALL}")
    input(f"{EMOJI['BACK']} {translator.get('accounts.press_enter')}...")
    
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
                'accounts.press_enter': '按Enter键返回主菜单...'
            }
            result = translations.get(key, key)
            return result.format(**kwargs) if kwargs else result
            
    main(SimpleTranslator())