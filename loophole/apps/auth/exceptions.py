# _*_ coding: utf-8 _*_
# @FileName : exceptions.py
# @Author   : sjl
# @CreatedAt     :  2021/03/24 11:18:56
# @UpdatedAt     :  2021/03/24 11:18:56
# @description: xxxx
# @Software : VSCode


class BaseAuthError(Exception):
    pass


class AccountError(BaseAuthError):
    pass


class PasswordError(BaseAuthError):
    pass