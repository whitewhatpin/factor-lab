"""冒烟测试：验证包结构可导入。"""


def test_import() -> None:
    """验证包可以正常导入。"""
    import ashare_factor_lab

    assert ashare_factor_lab.__version__ == "0.1.0"


def test_submodules_importable() -> None:
    """验证所有子模块可以导入。"""
    import ashare_factor_lab.data
    import ashare_factor_lab.evaluation
    import ashare_factor_lab.factor
    import ashare_factor_lab.pit


def test_cli_runs() -> None:
    """验证 CLI 入口可以执行。"""
    from ashare_factor_lab.cli import main

    main()  # 不应抛出异常
