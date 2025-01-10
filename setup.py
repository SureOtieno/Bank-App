from setuptools import setup, find_packages

setup(
    name="bank_app",
    version="0.1.0",
    description="A command-line bank account management application",
    author="Suleiman",
    author_email="stsureotieno@gmail.com",
    url="https://github.com/SureOtieno/Bank-App",  # Update with your GitHub repo
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "bcrypt",  # Add other dependencies here
    ],
    entry_points={
        "console_scripts": [
            "bank-app=bank_app.main:main",  # Replace with your entry point
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
