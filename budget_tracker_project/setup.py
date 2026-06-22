from setuptools import setup, find_packages

setup(
    name="budget_tracker",
    version="0.1.0",
    author="엄윤성",
    author_email="email@example.com",
    description="수입/지출을 기록하고 통계를 계산하는 간단한 가계부 패키지",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=[],
    python_requires=">=3.8",
)
